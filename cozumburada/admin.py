from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Complaint


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'complaintDate']
    list_display_links = ['title', 'complaintDate']
    list_filter = ['complaintDate']
    search_fields = ['title']

    class Meta:
        model = Complaint


admin.site.register(Complaint, ComplaintAdmin)
