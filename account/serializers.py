from rest_framework import serializers

from account import models

class AccountSerializer(serializers.ModelSerializer):
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    class Meta:
        model = models.Account
        fields = (
            'username', 'last_login', 'email',
            'bio', 'profile_photo', 'followers_count',
            'following_count'
        )
