from django.contrib import admin

from apps.article.models import Article

# Register your models here.
@admin.register(Article)
class AccountAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = ('id', 'title', 'author')

    readonly_fields = ('id',)
