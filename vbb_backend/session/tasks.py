import datetime
import config.celery_app as app
from celery.decorators import periodic_task
from celery.schedules import crontab
from vbb_backend.session.models import Session
from vbb_backend.program.models import Slot


def get_current_time():
    now = datetime.datetime.now()
    time_now = Slot.get_slot_time(day=now.weekday(), hour=now.hour, minute=now.minute)
    return time_now


def get_all_sessions():
    return Session.objects.all()


def save_session(slot):
    Session.objects.create(
        start=slot.schedule_start,
        end=slot.schedule_end,
        slot_id=slot.pk,
        computer_id=slot.computer_id,
    )


@app.task(name="create session from slot save")
def create_session(slot_id):
    slot = Slot.objects.filter(pk=slot_id).first()
    save_session(slot)


@periodic_task(run_every=crontab(minute=0, hour=0))
def check_all_slots_for_session():
    session_qs = get_all_sessions()

    slot_qs = Slot.objects.all().exclude(pk__in=session_qs.values_list("slot_id"))

    for slot in slot_qs:
        save_session(slot)


@periodic_task(run_every=crontab(minute="*/30"))
def get_sessions_previous():
    time_now = get_current_time()
    session_qs = get_all_sessions()

    slot_qs = Slot.objects.filter(
        schedule_start__lt=time_now.replace(tzinfo=datetime.timezone.utc)
    ).exclude(pk__in=session_qs.values_list("slot_id"))

    for slot in slot_qs:
        save_session(slot)
