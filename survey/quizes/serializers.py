from rest_framework import serializers
from quizes.models import Answer, Quiz, QuizQuestion, QuestionAnswer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text']


class QuizQuestionSerializer(serializers.ModelSerializer):
    quiz_id = serializers.PrimaryKeyRelatedField(
        queryset=Quiz.objects.all(),
        source='quiz',
        write_only=True,
        required=False
    )

    class Meta:
        model = QuizQuestion
        fields = ['id', 'question', 'order',]


class QuestionAnswerSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(read_only=True)
    answer_id = serializers.PrimaryKeyRelatedField(
        queryset=Answer.objects.all(),
        source='answer',
        write_only=True,
        required=False
    )

    class Meta:
        model = QuestionAnswer
        fields = ['id', 'order', 'answer', 'answer_id', 'is_right']

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'