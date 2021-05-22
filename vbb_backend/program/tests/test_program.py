import pytest
from vbb_backend.program.models import Program

@pytest.mark.django_db
def test_program_create(program_factory):
    newProgram1 = program_factory.create()
    newProgram2 = program_factory.create()
    assert Program.objects.count() == 2
