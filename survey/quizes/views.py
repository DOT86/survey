from django.views.generic import ListView, TemplateView
from django.shortcuts import redirect
from rest_framework import permissions, viewsets, views, status
from quizes.models import Quiz
from quizes.serializers import QuizSerializer, QuizQuestionSerializer, SubmitAnswerSerializer
from quizes.services import QuizSessionService, QuizQuestionService, QuizService, UserAnswerService
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.AllowAny]


class CurrentQuestionView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Текущий вопрос опроса",
        description="Возвращает следующий вопрос для активной сессии пользователя",
        parameters=[
            OpenApiParameter(
                name="quiz_id",
                type=int,
                location=OpenApiParameter.QUERY,
                description="ID опроса",
                required=True,
            ),
        ],
        responses={
            200: QuizQuestionSerializer,
            400: {"description": "Quiz ID not provided"},
            401: {"description": "Unauthorized"},
            404: {"description": "Quiz not found / Session not found / No more questions"},
        },
        tags=["Quiz"],
    )

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


class SubmitAnswerView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Отправить ответ",
        description="Отправляет ответ пользователя на вопрос",
        parameters=[
            OpenApiParameter(
                name="quiz_id",
                type=int,
                location=OpenApiParameter.QUERY,
                description="ID опроса",
                required=True,
            ),
        ],
        request=SubmitAnswerSerializer,
        responses={
            201: {"description": "Answer submitted"},
            400: {"description": "Bad request"},
            401: {"description": "Unauthorized"},
            404: {"description": "Not found/Quiz not found"},
        },
        tags=["Quiz"],
    )
    def post(self, request):
        quiz_id = request.query_params.get('quiz_id')
        if not quiz_id:
            return Response(
                {'error': 'Quiz ID not provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        quiz_service = QuizService()
        quiz = quiz_service.get_by_id(id=int(quiz_id))
        if not quiz:
            return Response(
                {'error': 'Quiz not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SubmitAnswerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        quiz_session_service = QuizSessionService()
        quiz_session = quiz_session_service.get_by_user_and_quiz(
            user=request.user,
            quiz=quiz
        )

        if not quiz_session:
            return Response(
                {'error': 'Could not create or retrieve session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Сохраняем ответ
        data = serializer.validated_data
        user_answer_service = UserAnswerService()
        user_answer = user_answer_service.create(
            **{
                'session': quiz_session,
                'question_id': data.get('question_id'),
                'answer_type': data.get('answer_type'),
                'selected_answer_id': data.get('selected_answer_id'),
                'custom_answer_text': data.get('custom_answer_text'),
                'is_right': False,
            }
        )

        # Проверяем, завершен ли опрос
        next_question_id = quiz_session_service.get_current_question(
            user=request.user,
            quiz=quiz
        )

        is_completed = next_question_id is None

        if is_completed:
            quiz_session_service.set_completed(quiz_session=quiz_session)


        return Response({
            'message': 'Answer submitted successfully',
        }, status=status.HTTP_201_CREATED)


class StartQuizSessionView(views.APIView):
    permission_classes = [permissions.AllowAny]


    def post(self, request):
        quiz_id = request.query_params.get('quiz_id')
        if not quiz_id:
            return Response({'error': 'Quiz ID required'}, status=status.HTTP_400_BAD_REQUEST)

        quiz_service = QuizService()
        quiz = quiz_service.get_by_id(quiz_id)

        if not quiz:
            return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

        session_service = QuizSessionService()
        session = session_service.get_or_create_session(
            user=request.user,
            quiz=quiz
        )

        return Response({'session_id': session.id, 'status': 'created'})


###############################################################################
class QuizListView(ListView):
    model = Quiz
    template_name = 'quizzes/list.html'
    context_object_name = 'quizzes'

    def get_queryset(self):
        return Quiz.objects.filter(status='active')


class QuizStartView(TemplateView):
    template_name = 'quizzes/start.html'

    def get(self, request, *args, **kwargs):
        quiz_id = self.kwargs['quiz_id']
        return redirect(f'/quiz/take/{quiz_id}/')


class TakeQuizView(TemplateView):
    template_name = 'quizzes/take_quiz.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz_id'] = self.kwargs['quiz_id']
        return context


class QuizResultView(TemplateView):
    template_name = 'quizzes/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz_id'] = self.kwargs['quiz_id']
        return context
