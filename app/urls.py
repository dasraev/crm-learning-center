from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns

router = DefaultRouter()

router.register(r'teachers', TeacherViewSet)
router.register(r'students', StudentViewSet,basename='students')
router.register(r'courses', CourseViewSet)
router.register(r'group', GroupViewSet,basename='group')
router.register(r'student_choice', StudentChoiceViewSet)
router.register(r'student_check', StudentCheckViewSet)
router.register(r'attention', AttentionViewSet)
router.register(r'lesson', LessonViewSet)
router.register(r'lesson_by_group', LessonByGroupViewSet,basename='lesson_by_group')
router.register(r'group_by_course',GroupByCourseViewSet,basename='group_by_course')
router.register(r'students_by_group',StudentByGroupViewSet)




urlpatterns = [
    path('',include(router.urls))
]
