from rest_framework import serializers
from .models import School, Course, Teacher, ClassRoom, Student, StudentCard, Backpack

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCard
        fields = '__all__'

class BackpackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backpack
        fields = '__all__'