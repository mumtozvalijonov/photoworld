from rest_framework import serializers

from apps.photo import models


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = '__all__'
        read_only_fields = ('author',)