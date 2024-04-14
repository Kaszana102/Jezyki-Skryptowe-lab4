from django.contrib import admin
from .models import *


# Register your models here.

class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "image", "author",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "text", "user", "respondedCommentID",)


admin.site.register(Image, ImageAdmin)
admin.site.register(Comment, CommentAdmin)
