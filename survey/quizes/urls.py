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
    path('', include(router.urls)),
]
