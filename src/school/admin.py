from django.contrib import admin
from .models import School, Teacher, ClassRoom, Student, StudentCard

admin.site.register(School)
admin.site.register(Teacher)
admin.site.register(ClassRoom)
admin.site.register(Student)
admin.site.register(StudentCard)
