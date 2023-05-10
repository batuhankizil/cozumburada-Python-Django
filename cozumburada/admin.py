from django.contrib import admin
from .models import Complaint, Profile, Comment, ComplaintFavorite


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
