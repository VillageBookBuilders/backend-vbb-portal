import factory
from factory.declarations import SubFactory
from faker import Faker
import factory
from vbb_backend.users.models import *

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda a : "{}.{}@villagebookbuilders.org".format(a.first_name, a.last_name))
    password = "password"

class MentorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Mentor
    user = factory.SubFactory(UserFactory)

class ExecutiveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Executive
    user = factory.SubFactory(UserFactory)


class HeadmasterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Headmaster
    user = factory.SubFactory(UserFactory)


class ParentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Parent
    user = factory.SubFactory(UserFactory)


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student
    user = factory.SubFactory(UserFactory)

class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teacher
    user = factory.SubFactory(UserFactory)

class ProgramManagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProgramManager
    user = factory.SubFactory(UserFactory)

class ProgramDirectorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProgramDirector
    user = factory.SubFactory(UserFactory)