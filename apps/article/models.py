from django.db import models
from uuid import uuid4

from account.models import Account


class Article(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=100)
    content = models.TextField()
