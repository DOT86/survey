from rest_framework import serializers
from quizes.models import Answer, Quiz, QuizQuestion, QuestionAnswer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text']


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
        read_only_fields = ['answer']


class QuizQuestionSerializer(serializers.ModelSerializer):
    answers = QuestionAnswerSerializer(many=True, read_only=True)
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question', 'order', 'answers', ]


class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = ['id', 'name', 'order', 'description', 'status', 'questions', ]