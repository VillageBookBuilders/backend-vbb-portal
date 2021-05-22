import pytest
from vbb_backend.program.models import Computer

@pytest.mark.django_db
def test_computer_create(computer_factory):
    newComputer1 = computer_factory.create()
    newComputer2 = computer_factory.create()
    assert Computer.objects.count() == 2
