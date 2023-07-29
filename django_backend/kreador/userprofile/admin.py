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
    UserExperience, Poll, PollOption, Voter)

admin.site.register(Profile)

#PostImage inline Post admin panel
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

#PollOptions inline Poll admin panel
class PollOptionAdmin(admin.StackedInline):
    model = PollOption

class VoterAdmin(admin.StackedInline):
    model = Voter

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = [PollOptionAdmin]

    class Meta:
        model = Poll

@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    inlines = [VoterAdmin]

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(ReplyLike)
admin.site.register(UserContact)
admin.site.register(UserExperience)
# Register your models here.
