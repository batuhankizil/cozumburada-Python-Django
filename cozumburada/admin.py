from django.contrib import admin
from .models import Complaint, Profile, Comment, ComplaintFavorite

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']

    class Meta:
        model = Profile


admin.site.register(Profile, ProfileAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment']

    class Meta:
        model = Comment


admin.site.register(Comment, CommentAdmin)


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'complaintDate']
    list_display_links = ['title', 'complaintDate']
    list_filter = ['complaintDate']
    search_fields = ['title']

    class Meta:
        model = Complaint


admin.site.register(Complaint, ComplaintAdmin)


class FavAdmin(admin.ModelAdmin):
    list_display = ['complaint']

    class Meta:
        model = ComplaintFavorite


admin.site.register(ComplaintFavorite, FavAdmin)


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_verified')

    def is_verified(self, obj):
        return obj.profile.verified  # varsayılan olarak kullanıcı profil modelinize göre ayarlayın

    is_verified.boolean = True
    is_verified.short_description = 'Onaylı Hesap'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
