from django.contrib import admin
from userprofile.models import (
    Profile,
    Post,
    Comment,
    Reply,
    PostLike,
    CommentLike,
    ReplyLike,
    UserContact,
    PostImage,
    UserExperience)

admin.site.register(Profile)


class PostImageAdmin(admin.StackedInline):
    model = PostImage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin]

    class Meta:
        model = Post


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(ReplyLike)
admin.site.register(UserContact)
admin.site.register(UserExperience)
# Register your models here.
