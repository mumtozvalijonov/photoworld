from django.db import models

from uuid import uuid4

from account.models import Account


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/')

    @property
    def likes_count(self):
        return self.likes.count()


class Reaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Like(Reaction):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='likes')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes')

    def save(self, *args, **kwargs):
        if self.__class__.objects.filter(author=self.author, photo=self.photo).exists():
            return
        Dislike.objects.filter(author=self.author, photo=self.photo).delete()
        super().save(*args, **kwargs)


class Dislike(Reaction):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='dislikes')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='dislikes')


class Comment(Reaction):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='comments')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    text = models.TextField()