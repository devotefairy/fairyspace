from django.db import models


class School(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    established_year = models.IntegerField()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers')
    subject = models.CharField(max_length=100)
    hire_date = models.DateField()

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    name = models.CharField(max_length=50)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classrooms')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='classrooms')
    grade = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.school.name} - {self.name}"


class Student(models.Model):
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='students')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    enrollment_date = models.DateField()

    def __str__(self):
        return self.name


class StudentCard(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='card')
    card_number = models.CharField(max_length=30, unique=True)
    issued_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.name} - {self.card_number}"
