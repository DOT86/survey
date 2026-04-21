from django.urls import include, path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register(
    r'quizzes',
    views.QuizViewSet,
    basename='quizzes',
)

urlpatterns = [
    path('', views.QuizListView.as_view(), name='quiz_list'),
    path('start/<int:quiz_id>/', views.QuizStartView.as_view(), name='quiz_start'),
    path('take/<int:quiz_id>/', views.TakeQuizView.as_view(), name='quiz_take'),
    path('result/<int:quiz_id>/', views.QuizResultView.as_view(), name='quiz_result'),

    path('api/', include(router.urls)),
    path('api/current-question/', views.CurrentQuestionView.as_view(), name='current-question'),
    path('api/submit-answer/', views.SubmitAnswerView.as_view(), name='submit-answer'),
    path('api/start-session/', views.StartQuizSessionView.as_view(), name='start-session'),
]