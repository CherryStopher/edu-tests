from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=200)
    rut = models.CharField(max_length=20)
    
class TagEnum(models.TextChoices):
    NUMBERS = 'Numeros', 'Numeros'
    GEOMETRY = 'Geometria', 'Geometria'
    ALGEBRA_FUNCTIONS = 'Algebra y Funciones', 'Álgebra y Funciones'
    PROBABILITY_STATISTICS = 'Probabilidad y Estadisticas', 'Probabilidad y Estadísticas'

class Test(models.Model):
    name = models.CharField(max_length=200)
    
class Question(models.Model):
    statement = models.TextField() 
    explanation = models.TextField(blank=True, null=True)
    score = models.FloatField()
    tag_type = models.CharField(max_length=50, choices=TagEnum.choices)
    test = models.ForeignKey(Test, on_delete=models.CASCADE) # One to many
    
    
class Alternative(models.Model):
    content = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # One to many
    

