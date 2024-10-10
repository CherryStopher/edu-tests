from rest_framework import viewsets, status
from .serializer import StudentSerializer, TestSerializer
from .models import Student

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
    serializer = TestSerializer(data=request.data)
    
    if serializer.is_valid():  # Validate the entire test, including questions and alternatives
        try:
            with transaction.atomic():  # Transaction to ensure rollback if something fails
                serializer.save()  # Save the test, questions and alternatives automatically
            return Response({"message": f"Test created successfully. Test ID {serializer.data['id']}"}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:  # Catch any other unexpected exceptions
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)