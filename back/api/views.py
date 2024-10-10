from rest_framework import viewsets, status
from .serializer import StudentSerializer
from .models import Student, Test, Question, Alternative

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError


# Viewset is used to create the four CRUD operations 
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
# Create test
@api_view(['POST'])
def create_test(request):
    data = request.data
    try:
        # Create the test
        test = Test.objects.create(name=data['name'])
        
        # Create questions and answers
        for question_data in data['questions']:
            question = Question.objects.create(
                statement=question_data['statement'],
                explanation=question_data['explanation'],
                score=float(question_data['score']),
                tag_type=question_data['axisType'],
                test=test  # Associate the question with the test
            )
            
            # Create the alternatives
            for alternative_data in question_data['alternatives']:
                Alternative.objects.create(
                    content=alternative_data['content'],
                    correct=alternative_data['correct'],
                    question=question  # Associate the alternative with the question
                )

        return Response({"message": "Test created successfully."}, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)