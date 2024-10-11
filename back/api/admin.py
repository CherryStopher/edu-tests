from django.contrib import admin
from .models import Student, StudentTest, Test, Question, Alternative


class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rut")


class TestAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "statement", "score", "tag_type", "test")


class AlternativeAdmin(admin.ModelAdmin):
    list_display = ("id", "answer_number", "content", "correct", "question")


class StudentTestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "test",
        "score",
        "correct_answers",
        "wrong_answers",
        "skipped_questions",
    )


admin.site.register(Student, StudentAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Alternative, AlternativeAdmin)
admin.site.register(StudentTest, StudentTestAdmin)
