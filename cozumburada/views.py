from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ComplaintForm, UserUpdateForm, ProfileForm

from cozumburada.models import Complaint, Profile

import re


# @login_required(login_url='register_or_login')
def index(request):
    username = None
    user_count = User.objects.filter(is_superuser=False).count()
    complaint = Complaint.objects.all()
    complaint_count = Complaint.objects.count()
    if request.user.is_authenticated:
        username = request.user.username
    context = {
        'username': username,
        'user_count': user_count,
        'complaints': complaint,
        'complaint_count': complaint_count
    }
    return render(request, 'index.html', context)



def is_valid_email(email):
    regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(regex, email) is not None

email = "example@example.com"
if is_valid_email(email):
    print(f"{email} is a valid email address")
else:
    print(f"{email} is not a valid email address")


def register_or_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if 'name' in request.POST:
            name = request.POST.get('name')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password_again = request.POST.get('password-again')
            if not name or not email or not password or not first_name or not last_name or not password_again:
                messages.error(request, 'Lütfen tüm alanları doldurunuz.')
                return render(request, 'register.html')

            if not is_valid_email(email):
                messages.error(request, 'Geçersiz bir email adresi girdiniz.')
                return render(request, 'register.html')

            if password == password_again:
                user = User.objects.create_user(username=name, email=email, password=password, first_name=first_name,
                                                last_name=last_name)
                user.save()
                login(request, user)
                return redirect('anasayfa')
            else:
                # Burada şifrelerin eşleşmediğini belirten bir hata mesajı gösterilebilir.
                messages.error(request, 'Şifreler eşleşmiyor.')
                return render(request, 'register.html')
                pass
        else:
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not email and not password:
                messages.error(request, 'Lütfen bilgilerinizi girin.')
                return redirect('register_or_login')

            user = authenticate(request, username=email, password=password)
            print(email, password)
            if user is not None:
                login(request, user)
                return redirect('anasayfa')
            else:
                # Burada giriş başarısız olduğunda gösterilecek bir hata mesajı gösterilebilir.
                messages.error(request, 'Hatalı kullanıcı adı veya şifre.', extra_tags='danger')
                pass
    return render(request, 'register.html')


@login_required(login_url='register_or_login')
def sikayet_yaz(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Şikayetiniz alınmıştır. En kısa sürede incelenecektir.')
            return redirect('complaint')
    else:
        form = ComplaintForm(user=request.user)

    context = {
        'form': form
    }
    return render(request, 'complaint.html', context)


def complaints(request):
    complaints = Complaint.objects.all()
    complaints_sorted = sorted(complaints, key=lambda c: c.complaintDate, reverse=True)
    return render(request, 'complaints.html', {'complaints': complaints, 'complaints_sorted': complaints_sorted})


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('register_or_login')

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UserUpdateForm(request.POST, instance=request.user)
            formp = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

            email = request.POST.get('email')
            password = request.POST.get('password')
            name = request.POST.get('name')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password_again = request.POST.get('password_again')

            if not password and not password_again:
                messages.error(request, 'Lütfen şifrenizi giriniz.')
                return redirect('edit_profile')
            elif not password or not password_again:
                messages.error(request, 'Her iki şifreyi de giriniz.')
                return redirect('edit_profile')
            elif password != password_again:
                messages.error(request, 'Girilen şifreler birbirleriyle uyuşmuyor.')

            elif form.is_valid() and formp.is_valid():
                form.save()
                profile = formp.save(commit=False)
                if request.FILES.get('profile'):
                    profile.profile_picture = request.FILES.get('profile')
                profile.save()
                messages.success(request, 'Profil bilgileriniz başarıyla güncellendi.')
        else:
            form = UserUpdateForm(instance=request.user)
            formp = ProfileForm(instance=request.user.profile)
        return render(request, 'edit-profile.html', {'form': form, 'formp': formp})
    else:
        return render(request, 'index.html')


def logoutPage(request):
    logout(request)
    return redirect('anasayfa')
