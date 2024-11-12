# serializers.py
from rest_framework import serializers
from .models import TwitterStatus
from .models import UserQuery


class TwitterStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterStatus
        fields = ['url', 'created_by_user']

class UserQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuery
        fields = ['id', 'created_date', 'username', 'question', 'reasoning', 'response', 'connanicall_action_text']