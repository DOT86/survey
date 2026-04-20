from rest_framework import permissions, viewsets, views, status
from quizes.models import Quiz
from quizes.serializers import QuizSerializer, QuizQuestionSerializer
from quizes.services import QuizSessionService, QuizQuestionService
from rest_framework.response import Response


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]


class CurrentQuestionView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        quiz_id = request.query_params.get('quiz_id')
        quiz_session_service = QuizSessionService()
        quiz_question_service = QuizQuestionService()
        if not quiz_id:
            return Response({'error': 'Quiz ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

        quiz = Quiz.objects.filter(id=quiz_id).first()
        if not quiz:
            return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

        quiz_session = quiz_session_service.get_by_user_and_quiz(user=user, quiz=quiz)
        if not quiz_session:
            return Response({'error': 'Quiz session not found'}, status=status.HTTP_404_NOT_FOUND)
        question_id = quiz_session_service.get_current_question(user=user, quiz=quiz)
        if not question_id:
            return Response({'Error': 'No more questions'}, status=status.HTTP_404_NOT_FOUND)
        question = quiz_question_service.get_by_id(question_id)
        if not question:
            return Response({'Error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuizQuestionSerializer(question)

        return Response(serializer.data, status=status.HTTP_200_OK)