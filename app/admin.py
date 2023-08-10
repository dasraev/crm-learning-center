from django.contrib import admin
from .models import Teacher,Course,Group,Student,Lesson,Attention,Student_check,Student_choice

admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Lesson)
admin.site.register(Attention)
admin.site.register(Student_check)
admin.site.register(Student_choice)


