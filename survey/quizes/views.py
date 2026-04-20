from rest_framework import permissions, viewsets
from quizes.models import Quiz
from quizes.serializers import QuizSerializer

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]
