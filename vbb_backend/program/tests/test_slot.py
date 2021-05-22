import pytest
from vbb_backend.program.models import Slot

@pytest.mark.django_db
def test_slot_create(slot_factory):
    newSlot1 = slot_factory.create()
    newSlot2 = slot_factory.create()
    assert Slot.objects.count() == 2

