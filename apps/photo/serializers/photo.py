from rest_framework import serializers

from apps.photo import models


class PhotoSerializer(serializers.ModelSerializer):
    likes_count = serializers.ReadOnlyField()
    dislikes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    class Meta:
        model = models.Photo
        fields = '__all__'
        read_only_fields = ('author',)
