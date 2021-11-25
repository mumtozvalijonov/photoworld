from rest_framework import viewsets, filters
import django_filters

from apps.photo.models import Comment
from apps.photo.serializers import CommentSerializer
from apps.photo.permissions import IsCommentAuthor
from apps.photo.serializers.comment import CommentUpdateSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsCommentAuthor]
    
    filter_backends = (filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('photo',)
    ordering_fields = ('created_at',)
    ordering = ('-created_at',)

    search_fields = (
        '@text',
        '=author__username'
    )

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return CommentUpdateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
