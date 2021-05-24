import pytest
import json
from rest_framework import response
from rest_framework.test import force_authenticate
from vbb_backend.program.models import Program, Slot
from vbb_backend.program.api.viewsets.slot import ReadOnlySlotViewSet
from vbb_backend.program.api.serializers.program import MinimalProgramSerializer

def test_slot_create(slot_factory):
    newSlot1 = slot_factory.create()
    newSlot2 = slot_factory.create()
    assert Slot.objects.count() == 5

@pytest.fixture(autouse=True)
def setup_test_get_unique_programs_from_slot(slot_factory, computer_factory, program_factory):
    p1 = program_factory.create(name="program1")
    p2 = program_factory.create(name="program2")
    c1 = computer_factory.create(program=p1)
    c2 = computer_factory.create(program=p1)
    c3 = computer_factory.create(program=p2)
    slot_factory.create(computer=c1)
    slot_factory.create(computer=c2)
    slot_factory.create(computer=c3)

def test_get_unique_programs_from_slot(rf, admin_user):
    request = rf.get('/slot/get_unique_programs')
    force_authenticate(request, user=admin_user)
    view = ReadOnlySlotViewSet.as_view({'get' : 'get_unique_programs'})
    
    response = view(request).render()
    responseJSON = json.loads(response.content.decode('utf-8'))
    for obj in responseJSON:
        assert obj['name'] == 'program1' or obj['name'] == 'program2'
    assert len(responseJSON) == 2