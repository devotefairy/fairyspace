from django.db import models


class School(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    established_year = models.IntegerField()

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers')
    subject = models.CharField(max_length=100)
    hire_date = models.DateField()
    # 老师和课程的多对多关系，定义 related_name
    courses = models.ManyToManyField(Course, related_name='teachers', blank=True)

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    name = models.CharField(max_length=50)
    # ❎ 班级和学校的一对多关系，不定义 related_name
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='classrooms')
    grade = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.school.name} - {self.name}"


class Student(models.Model):
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='students')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    enrollment_date = models.DateField()
    #  ❎ 学生和老师的多对多关系，不定义 related_name
    teachers = models.ManyToManyField(Teacher, blank=True)

    def __str__(self):
        return self.name


class StudentCard(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='card')
    card_number = models.CharField(max_length=30, unique=True)
    issued_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.name} - {self.card_number}"


class Backpack(models.Model):
    # ❎ 学生和书包的一对一关系，不定义 related_name
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    size = models.CharField(
        max_length=20,
        choices=[
            ('S', 'Small'),
            ('M', 'Medium'),
            ('L', 'Large'),
            ('XL', 'Extra Large'),
        ],
    )
    purchase_date = models.DateField()
    is_damaged = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name}'s {self.brand} backpack"
