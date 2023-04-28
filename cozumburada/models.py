from django.db import models, migrations
from django.utils import timezone
from django.contrib.auth.models import User


# class Complaints(models.Model):
#     test = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     def __str__(self):
#         return self.test



class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    complaint = models.TextField()
    complaintDate = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=False, blank=True)

    def __str__(self):
        return self.title

class Image(models.Model):
    file = models.ImageField(upload_to='complaints/')



complaints = Complaint.objects.all()




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', default='default.png', null=True, blank=True)

    def __str__(self):
        return self.user.username
