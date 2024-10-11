from rest_framework import viewsets, status
from .serializer import StudentSerializer, TestSerializer
from .models import Question, Student, StudentTest, Test

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db import transaction


# Viewset is used to create the four CRUD operations
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# Get all tests
@api_view(["GET"])
def get_tests(request):
    try:
        tests = Test.objects.all()  # Get all tests
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"status": "Error", "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Get single test by ID
@api_view(["GET"])
def get_test_by_id(request, test_id):
    try:
        test = Test.objects.get(id=test_id)  # Search by id
        serializer = TestSerializer(test)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Test.DoesNotExist:
        return Response(
            {"status": "Error", "message": "Test not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"status": "Error", "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Create test
@api_view(["POST"])
def create_test(request):
    serializer = TestSerializer(data=request.data)

    if serializer.is_valid():
        # Validate the entire test, including questions and alternatives
        try:
            with transaction.atomic():  # Transaction to ensure rollback if something fails
                serializer.save()  # Save the test, questions and alternatives automatically
            return Response(
                {
                    "status": "Ok",
                    "id": str(serializer.data["id"]),  # Convert ID to string
                    "message": "",
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            return Response(
                {
                    "status": "Error",
                    "message": str(e),
                    "id": "",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:  # Catch any other unexpected exceptions
            return Response(
                {
                    "status": "Error",
                    "message": f"An unexpected error occurred: {str(e)}",
                    "id": "",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return Response(
            {
                "status": "Error",
                "message": "Validation error.",
                "id": "",
                "errors": serializer.errors,  # Include the validation errors
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# Assign test
@api_view(["POST"])
def assign_test(request, test_id):
    test = Test.objects.get(id=test_id)
    students_data = request.data.get("students", [])  # [] if there are no students

    # Query the DB to get the students with that ID
    students = Student.objects.filter(id__in=students_data)

    # IDs of existing students (the elements must be strings)
    existing_student_ids = list(map(str, students.values_list("id", flat=True)))
    # IDs of students that don't exist
    not_found_ids = list(set(students_data) - set(existing_student_ids))

    # If students data is empty, the json fields are incorrect or all students don't exist
    if not students_data or not existing_student_ids:
        return Response(
            {
                "status": "Error",
                "message": "No students provided.",
                "success": [],
                "error": [],
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        with transaction.atomic():
            for student in students:
                StudentTest.objects.get_or_create(student=student, test=test)

        # Custom messagge if there is an error
        messagge = "Some students don't exist." if not_found_ids else ""

        return Response(
            {
                "status": "Ok",
                "messagge": messagge,
                "success": existing_student_ids,
                "error": not_found_ids,
            },
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return Response(
            {
                "status": "Error",
                "message": str(e),
                "success": existing_student_ids,
                "error": not_found_ids,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# Submit students answers and get scores
@api_view(["POST", "GET"])
def manage_test_scores(request, test_id):
    if request.method == "POST":
        students_data = request.data.get("students", [])  # [] if there are no students

        success_ids = []
        error_ids = []

        # Get the questions asociated to the test
        test_questions = Question.objects.filter(test_id=test_id).values_list(
            "id", flat=True
        )

        for student_data in students_data:
            student_id = student_data.get("id")
            student_questions = student_data.get(
                "questions", []
            )  # [] if there are no questions

            answered_question_ids = {
                question.get("id") for question in student_questions
            }  # Set of answered question IDs

            try:
                student = Student.objects.get(id=student_id)
                test = Test.objects.get(id=test_id)

                # get_or_create returns a tuple, the second variable tells us if it was created (true) or if it already existed (false)
                student_test, _ = StudentTest.objects.get_or_create(
                    student=student, test=test
                )

                correct_answers = 0
                wrong_answers = 0
                skipped_questions = 0
                total_score = 0

                for question_id in test_questions:  # Iterate through the test questions
                    # Check if the question was answered
                    if str(question_id) not in answered_question_ids:
                        skipped_questions += 1
                        continue  # Skip to the next question if not answered

                    # Get the student's answer for the current question
                    for student_question in student_questions:
                        if student_question.get("id") == str(question_id):
                            student_answer = student_question.get("answer")
                            break

                    # Get the question from DB and the correct answer
                    question_instance = Question.objects.get(id=question_id)
                    correct_alternative = question_instance.alternatives.filter(
                        correct=True
                    ).first()

                    # Check if the student's answer is correct or wrong
                    if (
                        correct_alternative
                        and correct_alternative.answer_number == int(student_answer)
                    ):
                        correct_answers += 1
                        total_score += question_instance.score  # Add score
                    else:
                        wrong_answers += 1

                # Save the results on StudentTest
                student_test.correct_answers = correct_answers
                student_test.wrong_answers = wrong_answers
                student_test.skipped_questions = skipped_questions
                student_test.score = total_score
                student_test.save()

                success_ids.append(student_id)

            except Student.DoesNotExist:
                error_ids.append(student_id)
            except Exception as e:
                error_ids.append(student_id)

        if error_ids:
            return Response(
                {
                    "status": "Error",
                    "message": "Some students don't exist.",
                    "success": success_ids,
                    "error": error_ids,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "status": "Ok",
                "success": success_ids,
                "error": [],
            },
            status=status.HTTP_200_OK,
        )

    elif request.method == "GET":
        try:
            test = Test.objects.get(id=test_id)
            # Filter the results by the test
            student_tests = StudentTest.objects.filter(test=test)

            students_data = []
            for student_test in student_tests:
                students_data.append(
                    {
                        "id": str(student_test.student.id),
                        "name": student_test.student.name,
                        "score": str(student_test.score),
                        "stats": {
                            "correct": str(student_test.correct_answers),
                            "wrong": str(student_test.wrong_answers),
                            "skip": str(student_test.skipped_questions),
                        },
                    }
                )

            return Response(
                {"id": str(test.id), "name": test.name, "students": students_data},
                status=status.HTTP_200_OK,
            )

        except Test.DoesNotExist:
            return Response(
                {"status": "Error", "message": "Test not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"status": "Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
