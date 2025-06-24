from rest_framework import viewsets
from .models import School, Course, Teacher, ClassRoom, Student, StudentCard, Backpack
from .serializers import SchoolSerializer, CourseSerializer, TeacherSerializer, ClassRoomSerializer, StudentSerializer, StudentCardSerializer, BackpackSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentCardViewSet(viewsets.ModelViewSet):
    queryset = StudentCard.objects.all()
    serializer_class = StudentCardSerializer

class BackpackViewSet(viewsets.ModelViewSet):
    queryset = Backpack.objects.all()
    serializer_class = BackpackSerializer