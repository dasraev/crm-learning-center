from django.db import models
import datetime
from django.contrib.auth.models import User
from datetime import timedelta,datetime,date


class Teacher(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.name}'



class Course(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='groups',null=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name='groups',null=True)
    start_date = models.DateField(null=True)
    time = models.TimeField(null=True)
    def make_attention(self):
        attention1 = Attention.objects.create(group=self,start_date=self.start_date)
        attention1.make_lessons()
        attention1.save()
    def __str__(self):
        return self.name

class Attention(models.Model):
    group = models.ForeignKey('Group',on_delete=models.CASCADE)
    month_num = models.IntegerField(default=1)
    start_date = models.DateField(null=True)
    def make_lessons(self):
        if self.month_num==1:
            start_date = Group.objects.get(id=self.group.id).start_date
            one_day=timedelta(days=1)
            odd_days = ['Mon','Wed','Fri']
            even_days = ['Tue','Thu','Sat']
            if start_date.strftime('%a') in odd_days:
                days = odd_days.copy()
            else:
                days = even_days.copy()
            x = 0
            while x<12:
                start_date+=one_day
                if start_date.strftime('%a') in days:
                    lesson = Lesson.objects.create(attention=self,date=start_date,day_num=x+1)
                    lesson.save()
                    x+=1

        elif self.month_num>1:
            if self.start_date:
                start_date = self.start_date
                one_day = timedelta(days=1)
                odd_days = ['Mon', 'Wed', 'Fri']
                even_days = ['Tue', 'Thu', 'Sat']
                if start_date.strftime('%a') in odd_days:
                    days = odd_days.copy()
                else:
                    days = even_days.copy()
                x = 0
                while x < 12:

                    if start_date.strftime('%a') in days:
                        lesson = Lesson.objects.create(attention=self, date=start_date, day_num=x + 1)
                        lesson.make_student_check()
                        lesson.save()
                        x += 1
                    start_date += one_day

            # else:
            #     print('hellllloooooo')
            #     l = len(Attention.objects.filter(group=self.group))
            #     attention = Attention.objects.filter(group=self.group)[l-2]
            #     print(attention)
            #     last_day = Lesson.objects.filter(attention=attention).last().date
            #     print(last_day)
            #     start_date = last_day
            #     one_day = timedelta(days=1)
            #     odd_days = ['Mon', 'Wed', 'Fri']
            #     even_days = ['Tue', 'Thu', 'Sat']
            #     if start_date.strftime('%a') in odd_days:
            #         days = odd_days.copy()
            #     else:
            #         days = even_days.copy()
            #     x = 0
            #     while x < 12:
            #         start_date += one_day
            #
            #         if start_date.strftime('%a') in days:
            #             lesson = Lesson.objects.create(attention=self, date=start_date, day_num=x + 1)
            #             lesson.save()
            #             x += 1



    def __str__(self):
        return f'{self.group} | {self.month_num}'




class Lesson(models.Model):
    attention = models.ForeignKey('Attention',on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(null=True)
    day_num = models.IntegerField(null=True)
    freezed = models.BooleanField(default=False)

    def make_student_check(self):
        attention = Attention.objects.get(id=self.attention.id)
        group = Group.objects.get(id = attention.group.id)
        choices = Student_choice.objects.filter(group=group)
        for choice in choices:
            s=Student_check.objects.create(student=choice.student,lesson=self)
            s.save()
    def make_all_freezed(self):
        attention = self.attention
        freezed=self.freezed
        print(freezed)
        print(attention)
        lessons = Lesson.objects.filter(attention=attention)
        for lesson in lessons:
            lesson.freezed=self.freezed
            lesson.save()
            absence_ss = Student_check.objects.filter(lesson=lesson)
            for absence_s in absence_ss:
                if self.freezed:
                    absence_s.absence='freezed'
                else:
                    absence_s.absence='None'
                absence_s.save()

    def __str__(self):
        return f'{self.attention} | day_number:{self.day_num}'



class Student_choice(models.Model):
    student = models.ForeignKey('Student',on_delete=models.CASCADE)
    course = models.ForeignKey('Course',on_delete=models.CASCADE,null=True)
    group = models.ForeignKey('Group',on_delete=models.CASCADE)


    def make_student_check(self):
        attentions = Attention.objects.filter(group=self.group)
        for attention in attentions:
            lessons = Lesson.objects.filter(attention=attention)
            for lesson in lessons:
                student_check = Student_check.objects.create(student=self.student,lesson=lesson)
                student_check.save()
    def update_check(self):
        attentions = Attention.objects.filter(group=self.group)
        for attention in attentions:
            lessons = Lesson.objects.filter(attention=attention)


    def __str__(self):
        return f'{self.student} || {self.group}'

class Student_check(models.Model):
    student = models.ForeignKey('Student',on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson',on_delete=models.CASCADE)
    absence = models.CharField(max_length=255,default='None')
    freezed = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.student} | {self.lesson} | {self.absence}'


