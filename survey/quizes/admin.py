from django.contrib import admin
from quizes.models import Quiz, QuizQuestion, QuestionAnswer, UserAnswer, QuizSession, QuizStatistics, Answer

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'status')
    list_filter = ('status',)
    ordering = ('order',)

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'order', 'question')
    list_filter = ('quiz',)
    ordering = ('order',)

@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'answer', 'is_right')
    list_filter = ('question',)
    ordering = ('order',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text',)
    ordering = ('text',)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('session', 'question', 'selected_answer', 'answer_type')
    list_filter = ('session', 'question', 'answer_type')
    ordering = ('session', 'question', 'answer_type')

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'status')
    list_filter = ('quiz', 'user', 'status')
    ordering = ('quiz', 'user', 'status')

@admin.register(QuizStatistics)
class QuizStatisticsAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'questions_count', 'answers_count', 'correct_answers_count', 'incorrect_answers_count')
    list_filter = ('quiz',)
    ordering = ('quiz',)
