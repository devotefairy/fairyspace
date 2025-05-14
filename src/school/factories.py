import factory
from factory.django import DjangoModelFactory
from django.utils import timezone
from .models import School, Teacher, ClassRoom, Student, StudentCard


class SchoolFactory(DjangoModelFactory):
    class Meta:
        model = School

    name = factory.Faker('company')
    address = factory.Faker('address')
    established_year = factory.Faker('year')


class TeacherFactory(DjangoModelFactory):
    class Meta:
        model = Teacher

    name = factory.Faker('name')
    school = factory.SubFactory(SchoolFactory)
    subject = factory.Faker('word')
    hire_date = factory.Faker('date_this_decade')


class ClassRoomFactory(DjangoModelFactory):
    class Meta:
        model = ClassRoom

    name = factory.Faker('bothify', text='Class ??')
    school = factory.SubFactory(SchoolFactory)
    teacher = factory.SubFactory(TeacherFactory)
    grade = factory.Faker('bothify', text='Grade ?')


class StudentFactory(DjangoModelFactory):
    class Meta:
        model = Student

    name = factory.Faker('name')
    classroom = factory.SubFactory(ClassRoomFactory)
    school = factory.SelfAttribute('classroom.school')
    enrollment_date = factory.Faker('date_this_year')


class StudentCardFactory(DjangoModelFactory):
    class Meta:
        model = StudentCard

    student = factory.SubFactory(StudentFactory)
    card_number = factory.Faker('uuid4')
    issued_date = factory.Faker('date_this_year')
    is_active = True
