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
    path('current-question/', views.CurrentQuestionView.as_view(), name='current-question'),
    path('', include(router.urls)),
]
