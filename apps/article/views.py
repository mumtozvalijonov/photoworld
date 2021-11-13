from rest_framework import viewsets
from rest_framework import permissions

from apps.article.models import Article
from apps.article.serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
