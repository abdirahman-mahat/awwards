from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Rating)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Location)
admin.site.register(Followers)
admin.site.register(tags)
admin.site.register(technologies)
admin.site.register(Comment)
admin.site.register(Collection)
admin.site.register(PostLikes)
admin.site.register(CommentsLikes)
