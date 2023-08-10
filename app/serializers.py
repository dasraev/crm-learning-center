from rest_framework import serializers
from .models import *


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class AttentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attention
        fields = '__all__'

class StudentChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_choice
        fields = '__all__'

class StudentCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_check
        fields = ['id','student','lesson','absence','freezed']

