from rest_framework import viewsets, filters
import django_filters

from apps.photo.models import Comment
from apps.photo.serializers import CommentSerializer



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    
    filter_backends = (filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('photo',)
    ordering_fields = ('created_at',)
    ordering = ('-created_at',)

    search_fields = (
        '@text',
        '=author__username'
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
