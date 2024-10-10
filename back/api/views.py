from rest_framework import viewsets, status
from .serializer import StudentSerializer
from .models import Student, Test, Question, Alternative

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db import transaction


# Viewset is used to create the four CRUD operations 
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
# Create test
@api_view(['POST'])
def create_test(request):
    data = request.data
    try:
         with transaction.atomic(): # Transaction for rollback if something fails
            # The test is created, but not yet saved
            test = Test(name=data['name'])
            try:
                test.full_clean()  # Validate the test data
                test.save()
            except ValidationError as e:
                raise ValidationError(f"Error validating the test. Please check the test data: {e}")
            
            # Create questions
            questions = []
            for question_data in data['questions']:
                question = Question(
                    statement=question_data['statement'],
                    explanation=question_data.get('explanation', ''),
                    score=float(question_data['score']),
                    tag_type=question_data['tagType'],
                    test=test  # Asociate to the test
                )
                try:
                    question.full_clean()  # Validate that the fields are correct
                    question.save()
                except ValidationError as e: # We use ValidationError for the correct transaction rollback 
                    raise ValidationError(f"Error validating question with ID {question_data.get('id', 'unknown')}: {e}")  # unknown if id doesn't exist
                
                
                # Create the alternatives
                alternatives = question_data['alternatives']
                
                 # Validate number of alternatives
                if len(alternatives) > 5:
                    raise ValidationError(f"Question with ID: {question_data.get('id', 'unknown')} has more than 5 alternatives.")
                
                # Count correct alternatives
                correct_count = sum(1 for alt in alternatives if alt.get('correct', False))
                if correct_count != 1:
                    raise ValidationError(f"Question with ID: {question_data.get('id', 'unknown')} must have exactly 1 correct alternative.")
                
                for alternative_data in alternatives:
                    alternative = Alternative(
                        content=alternative_data['content'],
                        correct=alternative_data['correct'],
                        question=question  # Associate the alternative with the question
                    )
                    try:
                        alternative.full_clean()  # Validate the alternative fields
                        alternative.save()
                    except ValidationError as e:
                        raise ValidationError(f"Error validating alternative with ID {alternative_data.get('id', 'unknown')}: {e}")  # unknown if id doesn't exists
                    


            return Response({"message": f"Test created successfully. Test ID {test.id}"}, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)