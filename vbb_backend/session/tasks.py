import datetime
from celery.decorators import periodic_task
from celery.schedules import crontab
from vbb_backend.session.models import Session
from vbb_backend.program.models import Slot


@periodic_task(run_every=crontab(minute="*/1"))
def get_sessions():
    now = datetime.datetime.now()
    schedule_start = Slot.DEAFULT_INIT_DATE + datetime.timedelta(
        days=now.weekday(), hours=now.hour, minutes=now.minute
    )
    print(schedule_start)
    session_qs = Session.objects.filter(slot__isnull=False)
    slot_qs = Slot.objects.filter(
        schedule_start__gt=schedule_start.replace(tzinfo=datetime.timezone.utc)
    ).exclude(pk__in=session_qs)
    print(len(slot_qs))

    for session in slot_qs:
        print(f"create session: {session}")
