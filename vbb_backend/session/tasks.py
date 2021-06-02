import datetime
from config.celery_app import app
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from vbb_backend.session.models import Session
from vbb_backend.program.models import Slot


schedule, created = IntervalSchedule.objects.get_or_create(
    every=30,
    period=IntervalSchedule.MINUTES,
)

PeriodicTask.objects.get_or_create(
    interval=schedule,
    name="get_sessions",
    task='vbb_backend.session.tasks.get_sessions',
)

@app.task
def get_sessions():
    queryset = Session.objects.all()
    qs = queryset.filter(slot__isnull=False)

    now = datetime.datetime.now()

    todays_time = Slot.DEAFULT_INIT_DATE + datetime.timedelta(
            days=int(now.weekday()), hours=int(now.hour), minutes=int(now.minute)
        )

    for session in qs:
        if session.slot.schedule_start < todays_time.replace(tzinfo=datetime.timezone.utc):
            print('session passed for this week')
        else:
            print('session will come')
