from django.contrib import admin
from .models import Student, Test, Question, Alternative


class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rut")


class TestAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "statement", "score", "tag_type", "test")


class AlternativeAdmin(admin.ModelAdmin):
    list_display = ("id", "content", "correct", "question")


admin.site.register(Student, StudentAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Alternative, AlternativeAdmin)
