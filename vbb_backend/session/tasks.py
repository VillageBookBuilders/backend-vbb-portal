import datetime
from celery.decorators import periodic_task
from celery.schedules import crontab
from vbb_backend.session.models import Session
from vbb_backend.program.models import Slot

    # don't create a session without a slot
    # loook through slots taht have been passed
    # ex. monday 7:45 look for all these slots created for this day
    # create session for next week
    # get list of all the slots before current time and check if there is a session instance for next week
    # need to create slot for next week
    # is there a session in the future connected to that slot
    #
    # what's the criteria for the list of slots we're iterating over
    # have sessions that happen once a month
    # cancel 2 weeks out or reschedule for 3 weeks out? (create another model for outages then check against that)
    # cancellation is a future feature
    # if mentor cannot meet mentee create materials and send to mentee
    # allow mentors to say 2wks from now...
    # when we save 2wks data, for that slot not available
    # build out MVP first
    #
    # every time we save a slot create a session through a task
    # every 2 hrs check every slot
def get_schedule_time():


@periodic_task(run_every=crontab(minute="*/120"))
def get_sessions_future():
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

@periodic_task(run_every=crontab(minute="*/30"))
def get_sessions_previous():
    noe = datetime.datetime.now()
    schedule_start = Slot.get_slot_time(start_day_of_week, start_hour, start_minute)
