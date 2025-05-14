from django.core.management.base import BaseCommand
from django.db import transaction
import random
from school.factories import (
    SchoolFactory,
    TeacherFactory,
    ClassRoomFactory,
    StudentFactory,
    StudentCardFactory,
)


class Command(BaseCommand):
    help = 'Generates test data for the school application'

    def add_arguments(self, parser):
        parser.add_argument('--schools', type=int, default=2, help='Number of schools to create')
        parser.add_argument('--teachers-per-school', type=int, default=5, help='Number of teachers per school')
        parser.add_argument('--classrooms-per-school', type=int, default=6, help='Number of classrooms per school')
        parser.add_argument('--students-per-classroom', type=int, default=30, help='Number of students per classroom')

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write('Creating test data...')

            # Create schools
            schools = []
            for _ in range(options['schools']):
                school = SchoolFactory()
                schools.append(school)
                self.stdout.write(f'Created school: {school.name}')

                # Create teachers for this school
                teachers = []
                for _ in range(options['teachers_per_school']):
                    teacher = TeacherFactory(school=school)
                    teachers.append(teacher)
                    self.stdout.write(f'Created teacher: {teacher.name} at {school.name}')

                # Create classrooms for this school
                for _ in range(options['classrooms_per_school']):
                    # Assign a random teacher from the school's teachers
                    classroom = ClassRoomFactory(school=school, teacher=random.choice(teachers) if teachers else None)
                    self.stdout.write(f'Created classroom: {classroom.name} at {school.name}')

                    # Create students for this classroom
                    for _ in range(options['students_per_classroom']):
                        student = StudentFactory(classroom=classroom, school=school)
                        # Create student card
                        student_card = StudentCardFactory(student=student)
                        self.stdout.write(f'Created student: {student.name} with card: {student_card.card_number}')

            self.stdout.write(self.style.SUCCESS('Successfully created test data'))
