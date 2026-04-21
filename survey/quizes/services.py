from typing import Optional
from django.utils import timezone
from users.models import User
from quizes.models import QuizSession, Quiz, QuizQuestion, QuestionAnswer, UserAnswer


class QuizService:
    def __init__(self):
        self.model = Quiz

    def get_by_id(self, id: int) -> Quiz | None:
        return self.model.objects.filter(id=id).first()


class QuestionAnswerService:
    def __init__(self):
        self.model = QuestionAnswer

    def get_by_question_id_and_session(self, question_id: int, session: QuizSession) -> Optional[QuestionAnswer]:
        return self.model.objects.filter(question_id=question_id, session=session).first()


class QuizSessionService:
    def __init__(self):
        self.quiz_question_service = QuizQuestionService()
        self.question_answer_service = QuestionAnswerService()
        self.quiz_service = QuizService()

    def get_or_create_session(self, user: User, quiz: Quiz) -> QuizSession:
        quiz_session = self.get_by_user_and_quiz(user=user, quiz=quiz)
        if not quiz_session:
            quiz_session = QuizSession.objects.create(user=user, quiz=quiz)
        return quiz_session

    def get_by_user(self, user: User) -> Optional[QuizSession]:
        return QuizSession.objects.filter(user=user).first()

    def get_by_user_and_quiz(self, user: User, quiz: Quiz) -> Optional[QuizSession]:
        return QuizSession.objects.select_related('quiz').filter(user=user, quiz=quiz).first()

    def get_current_question(self, user: User, quiz: Quiz) -> int | None:
        quiz_session = self.get_by_user_and_quiz(user=user, quiz=quiz)
        if not quiz_session:
            return None

        question_ids = self.quiz_question_service.get_ids_by_quiz(quiz_session.quiz)
        if not question_ids:
            return None

        # Ищем первый вопрос без ответа
        for question_id in question_ids:
            question_answer = self.question_answer_service.get_by_question_id_and_session(
                question_id=question_id,
                session=quiz_session
            )
            if not question_answer:  # Если ответа нет
                return question_id

        return None  # Все вопросы отвечены

    def get_completed_last_session(self, quiz_id: int, user: User) -> Optional[QuizQuestion]:
        quiz =  self.quiz_service.get_by_id(id=quiz_id)
        if not quiz:
            return None

        quiz_session = QuizSession.objects.filter(
            quiz=quiz,
            user=user,
            status=QuizSession.STATUS_COMPLETED,
        ).last()
        if not quiz_session:
            return None
        return quiz_session

    def set_completed(self, quiz_session: QuizSession)-> QuizSession:
        quiz_session.status = QuizSession.STATUS_COMPLETED
        quiz_session.ended_at = timezone.now()
        quiz_session.save()
        return quiz_session


class QuizQuestionService:
    def __init__(self):
        self.model = QuizQuestion

    def get_by_id(self, id: int) -> Optional[QuizQuestion]:
        return self.model.objects.filter(id=id).first()

    def get_ids_by_quiz(self, quiz: Quiz) -> list[int]:
        return list(self.model.objects.filter(quiz=quiz).order_by('order').values_list('id', flat=True))

    def get_next_question(self, answered_questions: list[int]) -> Optional[QuizQuestion]:
        return self.model.objects.exclude(
            id__in=answered_questions
        ).order_by('order').first()


class UserAnswerService:
    def __init__(self):
        self.model = UserAnswer

    def create(self, **kwargs) -> UserAnswer:
        return self.model.objects.create(**kwargs)