import factory
from django.utils import timezone
from vbb_backend.program.models import *

from vbb_backend.users.tests.factories import *
from faker import Faker
from datetime import timedelta
fake = Faker()

class ProgramFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Program

    name = factory.Faker("name")
    latitude = factory.Faker("latitude")
    longitude = factory.Faker("longitude")
    program_director = factory.SubFactory(ProgramDirectorFactory)
  

class ComputerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Computer
    program = factory.SubFactory(ProgramFactory)


class SlotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Slot
    computer = factory.SubFactory(ComputerFactory)
    schedule_start= Slot.DEAFULT_INIT_DATE + fake.time_delta()
    schedule_end= Slot.DEAFULT_INIT_DATE + fake.time_delta()
    

class StudentSlotAssociationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StudentSlotAssociation

    student = factory.SubFactory(StudentFactory)
    slot = factory.SubFactory(SlotFactory)


class StudentWithSlotFactory(StudentSlotAssociationFactory):
    student_slot = factory.RelatedFactory(
        StudentSlotAssociationFactory,
        related_name="student_slot"
    )


class MentorSlotAssociationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MentorSlotAssociation

    mentor = factory.SubFactory(MentorFactory)
    slot = factory.SubFactory(SlotFactory)
 

class MentorWithSlotFactory(MentorSlotAssociationFactory):
    mentor_slot = factory.RelatedFactory(
        MentorSlotAssociationFactory,
        related_name="mentor_slot"
    )



# class HeadmastersProgramAssociationFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = HeadmastersProgramAssociation

#     headmaster = factory.SubFactory(HeadmasterFactory)
#     program = factory.SubFactory(ProgramFactory)


# class HeadmasterWithProgramFactory(HeadmastersProgramAssociationFactory):
#     headmaster_with_program = factory.RelatedFactory(
#         HeadmastersProgramAssociationFactory,
#         factory_related_name="program_headmaster",
#     )


# class TeachersProgramAssociationFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = TeachersProgramAssociation
        
#     teacher = factory.SubFactory(TeacherFactory)
#     program = factory.SubFactory(ProgramFactory)


# class TeacherWithProgramFactory(TeachersProgramAssociationFactory):
#     teacher_with_program = factory.RelatedFactory(
#         TeachersProgramAssociationFactory,
#         factory_related_name="program_teacher",
#     )


# class ManagersProgramAssociationFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = ManagersProgramAssociation
        
#     program_manager = factory.SubFactory(ProgramManagerFactory)
#     program = factory.SubFactory(ProgramFactory)


# class ManagerWithProgramFactory(ManagersProgramAssociationFactory):
#     manager_with_program = factory.RelatedFactory(
#         ManagersProgramAssociationFactory,
#         related_name="program_manager"
#     )
