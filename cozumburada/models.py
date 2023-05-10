from django.conf import settings
from django.db import models, migrations
from django.utils import timezone
from django.contrib.auth.models import User


# class Complaints(models.Model):
#     test = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     def __str__(self):
#         return self.test


class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='complaints')
    title = models.CharField(max_length=255)
    complaint = models.TextField()
    complaintDate = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='complaints/', null=True, blank=True)
    favorites = models.ManyToManyField(User, related_name='favorite_complaints', blank=True)



    def __str__(self):
        return self.title


complaints = Complaint.objects.all()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', default='default.png', null=True, blank=True)

    def __str__(self):
        return self.user.username


# class Comment(models.Model):
#     complaint = models.ForeignKey('cozumburada.Complaint', on_delete=models.CASCADE)
#     content = models.TextField(verbose_name='Yorum')
#     created_date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    commentDate = models.DateTimeField(auto_now_add=True)

comments = Comment.objects.all()



class ComplaintFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    complaint_title = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

