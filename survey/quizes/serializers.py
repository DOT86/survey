from rest_framework import serializers
from quizes.models import Answer, Quiz, QuizQuestion, QuestionAnswer, UserAnswer


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


class SubmitAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_type = serializers.ChoiceField(choices=UserAnswer.ANSWER_TYPE_CHOICES)
    selected_answer_id = serializers.IntegerField(required=False, allow_null=True)
    custom_answer_text = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        answer_type = data.get('answer_type')
        selected_answer_id = data.get('selected_answer_id')
        custom_answer_text = data.get('custom_answer_text')

        if answer_type == UserAnswer.PREDEFINED and not selected_answer_id:
            raise serializers.ValidationError({
                'selected_answer_id': 'This field is required for predefined answer'
            })

        if answer_type == UserAnswer.CUSTOM and not custom_answer_text:
            raise serializers.ValidationError({
                'custom_answer_text': 'This field is required for custom answer'
            })

        return data

