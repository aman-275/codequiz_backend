from rest_framework import serializers
from .models import Question, Answer, Comment
# from users.serializers import UserSerializer
# from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import NestedCreateMixin, NestedUpdateMixin


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["answer", "correct", "id"]
        extra_kwargs = {
            "correct": {"write_only": True},
           
        }


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["question", "comment", "user", "username"]


class QuestionSerializer(
    NestedCreateMixin, NestedUpdateMixin, serializers.ModelSerializer
):

    answers = AnswerSerializer(many=True)
    author_name = serializers.CharField(source="author.username", read_only=True)
    comments = CommentSerializer(many=True,read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "description",
            "created_at",
            "author",
            "answers",
            "author_name",
            "comments",
        ]
        extra_kwargs = {
            "author": {"read_only": True},
            "author_name": {"read_only": True},
            "comments": {"read_only": True},
        }

    def validate_answers(self, value):
        """
        answer field is realted with questions and 4
        choices are needed so in the case of update as well follow the same rule

        """
        if len(value) != 4:
            raise serializers.ValidationError(" 4 answers are required")

        counter = 0
        for data in value:
            if data.get("correct") == True:
                counter += 1

        if counter != 1:
            raise serializers.ValidationError("question can only have one right answer")

        return value
