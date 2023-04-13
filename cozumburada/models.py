from django.db import models

class Complaint(models.Model):
    title = models.CharField(max_length=60)
    complaint = models.TextField()
    complaintDate = models.DateTimeField()