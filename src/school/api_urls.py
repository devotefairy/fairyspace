from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolViewSet, CourseViewSet, TeacherViewSet, ClassRoomViewSet, StudentViewSet, StudentCardViewSet, BackpackViewSet

router = DefaultRouter()
router.register(r'schools', SchoolViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'classrooms', ClassRoomViewSet)
router.register(r'students', StudentViewSet)
router.register(r'student-cards', StudentCardViewSet)
router.register(r'backpacks', BackpackViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]