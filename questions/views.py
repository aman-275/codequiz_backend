from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from .serializers import QuestionSerializer
from .models import Question, Answer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class QuestionViewSet(viewsets.ModelViewSet):

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


    def get_queryset(self):
        return Question.objects.prefetch_related('answers','comments').all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def check_answer(self,request,pk=None):
        answer = get_object_or_404(Answer,pk=pk)
        return Response({"key":answer.correct},status=status.HTTP_200_OK)