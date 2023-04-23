"""cozumburada URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.shortcuts import render
from cozumburada import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


#
# def index(request):
#     return render(request, 'index.html')
# def register(request):
#     return render(request, 'register.html')
def complaint(request):
    return render(request, 'complaint.html')


def password_forget(request):
    return render(request, 'password-forget.html')


def complaints(request):
    return render(request, 'complaints.html')


urlpatterns = [
    path('', views.index, name='anasayfa'),
    path('anasayfa', views.index, name='anasayfa'),
    path('complaint', views.sikayet_yaz, name='complaint'),
    path('complaints.html', views.complaints, name='complaints'),
    path('password-forget.html', password_forget),
    path('edit-profile.html', views.edit_profile, name='edit_profile'),
    path('register.html', views.register_or_login, name='register_or_login'),
    path('logout/', views.logoutPage, name='logout'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
