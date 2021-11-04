from rest_framework import serializers

from account import models

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = '__all__'
