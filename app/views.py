from django.shortcuts import render
from rest_framework import viewsets,views,status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import permissions,status
from django.http import Http404

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            group = Group.objects.create(name = data.get('name'),
                                         start_date = data.get('start_date'),
                                         courses = data.get('courses'),
                                         teacher = data.get('teacher'),
                                         time = data.get('time')
                                         )
            group.make_attention()
            group.save()
        return Response({'status':'Group created'},status=status.HTTP_201_CREATED)


class GroupByCourseViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def retrieve(self, request, *args, **kwargs):
        id=self.kwargs['pk']
        if id:
            group = Group.objects.filter(courses=id)
            serializer = self.get_serializer(group,many=True)
            return Response(serializer.data)


    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)


class StudentChoiceViewSet(viewsets.ModelViewSet):
    queryset =Student_choice.objects.all()
    serializer_class = StudentChoiceSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        student_choice = Student_choice.objects.create(student=data['student'],
                                                       course=data['course'],
                                                       group=data['group'])
        student_choice.make_student_check()
        student_choice.save()
        return Response(serializer.data)
    def update(self, request, *args, **kwargs):
        id = kwargs['pk']
        choice = Student_choice.objects.get(id=id)
        serializer = self.get_serializer(choice,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('student_choice created')

            data=serializer.validated_data
            choice.update_check()
        print(data['student'])
        # group=choice.group
        # attentions = Attention.objects.filter(group = data['group'])
        # for attention in attentions:
        #     lessons = Lesson.objects.filter(attention=attention)
        #     for lesson in lessons:
        #         s=Student_check.objects.filter(student=data['student'])
        #         for x in s:
        #             x.lesson=lesson
        #             x.save()

class StudentCheckViewSet(viewsets.ModelViewSet):
    queryset = Student_check.objects.all().order_by('id')
    serializer_class = StudentCheckSerializer


class StudentByGroupViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        student_list=[]
        if id:
            students = Student_choice.objects.filter(group=id)
            for student in students:
                student_list.append(student.student)
            serializer = self.get_serializer(student_list,many=True)
            return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)



class AttentionViewSet(viewsets.ModelViewSet):
    queryset = Attention.objects.all()
    serializer_class = AttentionSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        if data.get('start_date'):
            start_date = data.get('start_date')
        else:
            attentions = self.get_queryset()
            l=len(attentions.filter(group=data.get('group')))
            print(l)
            attention=attentions.filter(group=data.get('group'))[l-1]
            print(attention)
            last_day = Lesson.objects.filter(attention=attention).last().date
            one_day = timedelta(days=1)
            odd_days = ['Mon', 'Wed', 'Fri']
            even_days = ['Tue', 'Thu', 'Sat']
            if last_day.strftime('%a') in odd_days:
                days = odd_days.copy()
            else:
                days = even_days.copy()
            x=0
            while x<1:
                last_day+=one_day
                if last_day.strftime('%a') in days:
                    start_date = last_day
                    x+=1



        attention = Attention.objects.create(group=data.get('group'),
                                     month_num=data.get('month_num'),
                                     start_date=start_date
                                     )

        attention.make_lessons()
        attention.save()
        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        if '-' in id:
            att_num = id.split('-')[1]
            id = id.split('-')[0]
            attention = Attention.objects.get(group_id=id,month_num=att_num)
        else:
            attention = Attention.objects.filter(group_id=id).last()

        current_month = Attention.objects.filter(group_id=id).last().month_num
        attentions = Attention.objects.filter(group_id=id)
        months = [i.month_num for i in attentions]
        lessons = Lesson.objects.filter(attention=attention)
        columns = []

        for lesson in lessons:
            d = {
                'dateuid':lesson.id,
                'key':lesson.id,
                'date':lesson.date,
                'freezed':lesson.freezed
            }
            columns.append(d)

        student_choices = Student_choice.objects.filter(group_id=id)
        ds=[]
        for student_choice in student_choices:
            checkdata = []

            data={
                'id':student_choice.student.id,
                'key':student_choice.student.id,
                'full_name':student_choice.student.name,
            }
            for lesson in lessons:
                print(Student_check.objects.filter(lesson=lesson))
                for check in Student_check.objects.filter(student=student_choice.student,lesson=lesson):
                    d={
                        'uid':check.id,
                        'student_id':student_choice.student.id,
                        'lesson_id':check.lesson.id,
                        'absence':check.absence,
                        'key':check.id
                    }

                    checkdata.append(d)
            data['checkdatas']=checkdata
            ds.append(data)


        return Response({'columns':columns,'data':ds,'months':months,'current_month':current_month})



class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().order_by('id')
    serializer_class = LessonSerializer
    def update(self, request, *args, **kwargs):
        id = kwargs['pk']
        lesson = self.get_queryset().get(id=id)
        serializer = self.get_serializer(lesson,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            lesson=Lesson.objects.get(id=id)
            lesson.make_all_freezed()
            return Response(serializer.data)
        data=serializer.validated_data

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LessonByGroupViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().order_by('id')
    serializer_class = LessonSerializer
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        if id:
            i=id.split('-')
            if len(i)==1:
                attention = Attention.objects.filter(group=i[0]).last()
            else:
                attention = Attention.objects.get(group=i[0],month_num=i[1])

            lessons = Lesson.objects.filter(attention=attention)
            serializer = self.get_serializer(lessons,many=True)
            return Response(serializer.data)

