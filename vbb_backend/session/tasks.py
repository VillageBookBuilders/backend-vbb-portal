import datetime
from celery.decorators import periodic_task, task
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

def get_current_time():
    now = datetime.datetime.now()
    time_now = Slot.get_slot_time(
        day=now.weekday(), hour=now.hour, minute=now.minute
    )
    return time_now

def get_all_sessions():
    return Session.objects.all()

def save_session(slot):
    print(f'\n\n\n SAVE SESSION \n\n\n')
    print(f'slot start_date: {slot.start_date}')
    Session.objects.create(
        start=slot.schedule_start,
        end=slot.schedule_end,
        slot_id=slot.pk,
        computer_id=slot.computer_id
    )

@task
def create_session(slot):
    print(f'CREATE SETTION {slot}')
    save_session(slot)

@periodic_task(run_every=crontab(minute="*/2"))
def get_sessions_future():
    time_now = get_current_time()
    session_qs = get_all_sessions()

    slot_qs = Slot.objects.filter(
        schedule_start__gt=time_now.replace(tzinfo=datetime.timezone.utc)
    ).exclude(pk__in=session_qs.values_list('slot_id'))

    for slot in slot_qs:
        print(f"create future session: {slot}")
        save_session(slot)

@periodic_task(run_every=crontab(minute="*/1"))
def get_sessions_previous():
    time_now = get_current_time()
    session_qs = get_all_sessions()

    slot_qs = Slot.objects.filter(
        schedule_start__lt=time_now.replace(tzinfo=datetime.timezone.utc)
    ).exclude(pk__in=session_qs.values_list('slot_id'))

    for slot in slot_qs:
        print(f"create past session: {slot.pk}")
        save_session(slot)
