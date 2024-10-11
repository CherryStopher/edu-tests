from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=200)
    rut = models.CharField(max_length=20)


class TagEnum(models.TextChoices):
    NUMBERS = "Números", "Números"
    GEOMETRY = "Geometría", "Geometría"
    ALGEBRA_FUNCTIONS = "Álgebra y Funciones", "Álgebra y Funciones"
    PROBABILITY_STATISTICS = (
        "Probabilidad y Estadísticas",
        "Probabilidad y Estadísticas",
    )


class Test(models.Model):
    name = models.CharField(max_length=200)
    students = models.ManyToManyField(Student, through="StudentTest")  # Many to many


class Question(models.Model):
    statement = models.TextField()
    explanation = models.TextField(blank=True, null=True)
    score = models.FloatField()
    tag_type = models.CharField(max_length=50, choices=TagEnum.choices)
    # One to many
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")


class Alternative(models.Model):
    answer_number = models.IntegerField(default=1)
    content = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    # One to many
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="alternatives"
    )


class StudentTest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    skipped_questions = models.IntegerField(default=0)

    class Meta:
        unique_together = ("student", "test")  # Avoid duplicates tuples
