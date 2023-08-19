from django.contrib import admin

from .models import *

# Register your models here.


admin.site.register(Posts)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Like_comment)
admin.site.register(Like_post)
admin.site.register(Follow)
admin.site.register(Trend)
admin.site.register(Save)