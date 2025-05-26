from django.contrib import admin
from .models import School, Course, Teacher, ClassRoom, Student, StudentCard, Backpack

admin.site.register(School)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(ClassRoom)
admin.site.register(Student)
admin.site.register(StudentCard)
admin.site.register(Backpack)
