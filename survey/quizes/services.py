from typing import Optional

from users.models import User
from quizes.models import QuizSession, Quiz
from quizes.services import QuizQuestionService, QuestionAnswerService

class QuizSessionService:
    def __init__(self):
        self.quiz_question_service = QuizQuestionService()
        self.question_answer_service = QuestionAnswerService()

    def get_by_user(self, user: User) -> Optional[QuizSession]:
        return QuizSession.objects.filter(user=user).first()

    def get_by_user_and_quiz(self, user: User, quiz: Quiz) -> Optional[QuizSession]:
        return QuizSession.objects.select_related('quiz').filter(user=user, quiz=quiz).first()

    def get_current_question(self,user: User, quiz: Quiz) -> int | None:
        quiz_session = self.get_by_user_and_quiz(user=user, quiz=quiz)
        if not quiz_session:
            return None
        question_ids = self.quiz_question_service.get_ids_by_quiz(quiz_session.quiz)

        current_question_id = None

        # check answered questions
        for question_id in question_ids:
            question_answer = self.question_answer_service.get_by_question_id_and_session(
                question_id=question_id, session=quiz_session)
            if question_answer:
                continue
            current_question_id = question_id
            break
        return current_question_id


class QuizQuestionService:
    def __init__(self):
        self.model = QuizQuestion

    def get_by_id(self, id: int) -> Optional[QuizQuestion]:
        return self.model.objects.filter(id=id).first()

    def get_ids_by_quiz(self, quiz: Quiz) -> Optional[list[int]]:
        return self.model.objects.filter(quiz=quiz).order_by('order').values_list('id', flat=True)

    def get_next_question(self, answered_questions: list[int]) -> Optional[QuizQuestion]:
        return self.model.objects.exclude(
            id__in=answered_questions
        ).order_by('order').first()


class QuestionAnswerService:
    def __init__(self):
        self.model = QuestionAnswer

    def get_by_question_id_and_session(self, question_id: int, session: QuizSession) -> Optional[QuestionAnswer]:
        return self.model.objects.filter(question_id=question_id, session=session).first()



