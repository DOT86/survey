from django.db import models
from django.utils.translation import gettext_lazy as _

class Quiz(models.Model):
    ACTIVE = 'active'
    DEACTIVATE = 'deactivated'

    STATUSES = [
        (ACTIVE, _('Active')),
        (DEACTIVATE, _('Deactivated')),
    ]
    name = models.CharField(
        _('Name'),
        max_length=200,
    )
    order = models.PositiveIntegerField(
        _('Order'),
        default=0,
        db_index=True,
    )
    description = models.CharField(
        _('Description'),
        max_length=2000,
        null=True,
        blank=True,
    )
    status = models.CharField(
        _('Status'),
        max_length=30,
        choices=STATUSES,
        default=ACTIVE,
        db_index=True,
    )
    author = models.ForeignKey(
        'authors.Author',
        verbose_name=_('Author'),
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Quiz')
        verbose_name_plural = _('Quizzes')

    def __str__(self) -> str:
        return f'Quiz: {self.id}'


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(
        'quizes.Quiz',
        verbose_name=_('Quiz'),
        on_delete=models.CASCADE,
    )
    order = models.PositiveIntegerField(
        _('Order'),
        default=0,
        db_index=True,
    )
    question = models.CharField(
        _('Question'),
        max_length=200,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Quiz Question')
        verbose_name_plural = _('Quiz Questions')
        ordering = ['order']
        unique_together = [['quiz', 'order']]

    def __str__(self) -> str:
        return f'QuizQuestion: {self.id}'


class Answer(models.Model):

    text = models.CharField(
        _('Text'),
        max_length=200,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')

    def __str__(self) -> str:
        return f'Answer: {self.id}'


class QuestionAnswer(models.Model):
    order = models.PositiveIntegerField(
        _('Order'),
        default=500,
        db_index=True,
    )
    question = models.ForeignKey(
        'quizes.QuizQuestion',
        verbose_name=_('Question'),
        on_delete=models.CASCADE,
    )
    answer = models.ForeignKey(
        'quizes.Answer',
        verbose_name=_('Answer'),
        on_delete=models.CASCADE,
    )
    is_right = models.BooleanField(
        _('Is right'),
        default=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Question Answer')
        verbose_name_plural = _('Question Answers')
        ordering = ['order']

    def __str__(self) -> str:
        return f'QuestionAnswer: {self.id}'


class QuizSession(models.Model):
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_ABANDONED = 'abandoned'

    STATUSES = [
        (STATUS_IN_PROGRESS, _('In Progress')),
        (STATUS_COMPLETED, _('Completed')),
        (STATUS_ABANDONED, _('Abandoned')),
    ]

    quiz = models.ForeignKey(
        'quizes.Quiz',
        verbose_name=_('Quiz'),
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'users.User',
        verbose_name=_('User'),
        on_delete=models.CASCADE,
    )
    started_at = models.DateTimeField(
        _('Started at'),
        auto_now_add=True,
    )
    ended_at = models.DateTimeField(
        _('Ended at'),
        null=True,
        blank=True
    )
    status = models.CharField(
        _('Status'),
        max_length=30,
        choices=STATUSES,
        default=STATUS_IN_PROGRESS,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Quiz Session')
        verbose_name_plural = _('Quiz Sessions')

    def __str__(self) -> str:
        return f'QuizSession: {self.id}'


class UserAnswer(models.Model):
    PREDEFINED = 'predefined'
    CUSTOM = 'custom'

    ANSWER_TYPE_CHOICES = [
        (PREDEFINED, _('Predefined')),
        (CUSTOM, _('Custom')),
    ]


    session = models.ForeignKey(
        'QuizSession',
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        'QuizQuestion',
        on_delete=models.CASCADE,
    )
    selected_answer = models.ForeignKey(
        'Answer',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_right = models.BooleanField(
        _('Is right'),
        default=False,
    )
    custom_answer_text = models.TextField(
        _('Custom answer text'),
        max_length=1000,
        null=True,
        blank=True,
    )
    answer_type = models.CharField(
        _('Answer type'),
        max_length=20,
        choices=ANSWER_TYPE_CHOICES,
        default=PREDEFINED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User Answer')
        verbose_name_plural = _('User Answers')

    def __str__(self) -> str:
        return f'UserAnswer: {self.id}'


class QuizStatistics(models.Model):
    quiz = models.OneToOneField(
        Quiz,
        on_delete=models.CASCADE,
        related_name='statistics',
        verbose_name=_('Quiz'),
    )
    questions_count = models.PositiveIntegerField(
        _('Questions count'),
        default=0,
    )
    answers_count = models.PositiveIntegerField(
        _('Answers count'),
        default=0,
    )
    correct_answers_count = models.PositiveIntegerField(
        _('Correct answers count'),
        default=0,
    )
    incorrect_answers_count = models.PositiveIntegerField(
        _('Incorrect answers count'),
        default=0,
    )
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Quiz Statistics')
        verbose_name_plural = _('Quiz Statistics')

    def __str__(self) -> str:
        return f'QuizStatistics: {self.quiz}'
