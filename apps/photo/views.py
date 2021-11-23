from django.db import transaction
from rest_framework import serializers, viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.photo.models import Comment, Photo
from apps.photo.permissions import IsAuthor
from apps.photo.serializers import PhotoSerializer, PhotoCommentSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAuthor]

    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('uploaded_at',)
    ordering = ('-uploaded_at',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['post'], detail=True)
    def like(self, request, pk=None):
        photo = self.get_object()
        photo.likes.create(
            author=request.user
        )
        serializer = self.get_serializer(photo)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def dislike(self, request, pk=None):
        photo = self.get_object()
        photo.dislikes.create(
            author=request.user
        )
        serializer = self.get_serializer(photo)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def comment(self, request, pk=None):
        serializer = PhotoCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            photo = self.get_object()
            with transaction.atomic():
                photo.comments.create(
                    author=request.user,
                    text=serializer.data['text']
                )
                serializer = self.get_serializer(photo)
                return Response(serializer.data)

    @action(methods=['get'], detail=True, serializer_class=PhotoCommentSerializer, url_path='comments')
    def get_photo_comments(self, request, pk=None):
        photo = self.get_object()
        queryset = Comment.objects.filter(photo=photo)

        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
