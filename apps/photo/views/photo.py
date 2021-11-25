from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.photo.models import Photo
from apps.photo.permissions import IsPhotoAuthor
from apps.photo.serializers import PhotoSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    permission_classes = [IsPhotoAuthor]

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
