from django.db import models
from django.utils.translation import gettext_lazy as _


class School(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    established_year = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('学校')
        verbose_name_plural = _('学校')
        indexes = [
            models.Index(fields=['name']),
        ]


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('课程名称'))
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = _('课程')
        verbose_name_plural = _('课程')
        indexes = [
            models.Index(fields=['code']),
        ]


class Teacher(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('教师姓名'))
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers')
    subject = models.CharField(max_length=100)
    hire_date = models.DateField()
    # 老师和课程的多对多关系，定义 related_name
    courses = models.ManyToManyField(Course, related_name='teachers', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('教师')
        verbose_name_plural = _('教师')
        indexes = [
            models.Index(fields=['name']),
        ]


class ClassRoomType(models.TextChoices):
    CLASSROOM = 'CLASSROOM', _('普通教室')
    LAB = 'LAB', _('实验室')
    LIBRARY = 'LIBRARY', _('图书馆')


class ClassRoom(BaseModel):
    name = models.CharField(max_length=50, verbose_name=_('班级名称'))
    # ❎ 班级和学校的一对多关系，不定义 related_name
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='classrooms')
    grade = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.school.name} - {self.name}"

    class Meta:
        verbose_name = _('班级')
        verbose_name_plural = _('班级')
        indexes = [
            models.Index(fields=['school', 'name']),
        ]


class StudentGender(models.TextChoices):
    MALE = 'MALE', _('男')
    FEMALE = 'FEMALE', _('女')
    OTHER = 'OTHER', _('其他')


class Student(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('学生姓名'))
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

    class Meta:
        verbose_name = _('学生卡')
        verbose_name_plural = _('学生卡')


class BackpackColor(models.TextChoices):
    RED = 'RED', _('红色')
    BLUE = 'BLUE', _('蓝色')
    GREEN = 'GREEN', _('绿色')
    BLACK = 'BLACK', _('黑色')
    OTHER = 'OTHER', _('其他')


class BackpackSize(models.TextChoices):
    S = 'S', 'S'
    M = 'M', 'M'
    L = 'L', 'L'
    XL = 'XL', 'XL'


class Backpack(BaseModel):
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

    class Meta:
        verbose_name = _('书包')
        verbose_name_plural = _('书包')
