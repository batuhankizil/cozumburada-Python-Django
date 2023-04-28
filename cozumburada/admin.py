from django.contrib import admin
from .models import Complaint, Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']

    class Meta:
        model = Profile


admin.site.register(Profile, ProfileAdmin)


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'complaintDate']
    list_display_links = ['title', 'complaintDate']
    list_filter = ['complaintDate']
    search_fields = ['title']


    class Meta:
        model = Complaint


admin.site.register(Complaint, ComplaintAdmin)
