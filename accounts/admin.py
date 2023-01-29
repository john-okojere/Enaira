from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Image, Transfer, User

admin.site.register(Image)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'image_tag', 'uid']

    def image_tag(self, obj):
        return mark_safe(f'<img src="/media/{obj.image}" width="50" height="50"/>')

admin.site.register(Transfer)
