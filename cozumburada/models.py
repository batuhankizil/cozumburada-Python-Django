from django.db import models, migrations
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


# class Complaints(models.Model):
#     test = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     def __str__(self):
#         return self.test

class Complaint(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    complaint = models.TextField()
    complaintDate = models.DateTimeField()

    def __str__(self):
        return self.title


complaints = Complaint.objects.all()

for complaint in complaints:
    print(complaint)
