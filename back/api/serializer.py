from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Student, StudentTest, Test, Question, Alternative


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name", "rut"]


class AlternativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternative
        fields = ["id", "answer_number", "content", "correct"]


class QuestionSerializer(serializers.ModelSerializer):
    # Includes alternatives such as nested serializers
    alternatives = AlternativeSerializer(many=True)
    # Maps tagType (json) to tag_type (model)
    tagType = serializers.CharField(source="tag_type")

    class Meta:
        model = Question
        fields = ["id", "statement", "explanation", "score", "tagType", "alternatives"]

    def validate_alternatives(self, value):
        # Ensure the question has between 1 and 5 alternatives
        if not (1 <= len(value) <= 5):
            raise ValidationError(
                "Each question must have between 1 and 5 alternatives."
            )

        # Ensure exactly one correct alternative
        correct_count = sum([alternative["correct"] for alternative in value])
        if correct_count != 1:
            raise ValidationError(
                "Each question must have exactly one correct alternative."
            )

        return value


class TestSerializer(serializers.ModelSerializer):
    # Include the questions as nested serializers
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ["id", "name", "questions"]

    def create(self, validated_data):
        """
        Creates the Test with questions and alternatives, since they are nested.
        """
        questions_data = validated_data.pop("questions")
        test = Test.objects.create(**validated_data)

        for question_data in questions_data:
            alternatives_data = question_data.pop("alternatives")
            question = Question.objects.create(test=test, **question_data)

            for alternative_data in alternatives_data:
                Alternative.objects.create(question=question, **alternative_data)

        return test


class StudentTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentTest
        fields = [
            "id",
            "student",
            "test",
            "score",
            "correct_answers",
            "wrong_answers",
            "skipped_questions",
        ]
