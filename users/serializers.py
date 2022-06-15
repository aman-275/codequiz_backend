from dataclasses import field
from django.contrib.auth import get_user_model
from rest_framework import exceptions, serializers
from rest_framework.settings import api_settings
from djoser.conf import settings
from djoser.compat import get_user_email, get_user_email_field_name

User = get_user_model()
from .models import *


class UserSerializer(serializers.ModelSerializer):

    following = serializers.IntegerField(source="following_count")
    followers = serializers.IntegerField(source="followers_count")

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "following", "followers") + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
        )
        read_only_fields = (settings.LOGIN_FIELD,)
        extra_kwargs = {"password": {"write_only": True}}

    def update(self, instance, validated_data):
        email_field = get_user_email_field_name(User)
        instance.email_changed = False
        if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
            instance_email = get_user_email(instance)
            if instance_email != validated_data[email_field]:
                instance.is_active = False
                instance.email_changed = True
                instance.save(update_fields=["is_active"])
        return super().update(instance, validated_data)


class FollowingSerializer(serializers.ModelSerializer):
    following_user_id = UserSerializer()

    class Meta:
        model = UserFollowing
        fields = ("id", "following_user_id", "created")


class FollowersSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()

    class Meta:
        model = UserFollowing
        fields = ("id", "user_id", "created")
