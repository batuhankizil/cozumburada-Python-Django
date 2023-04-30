import os

from django.conf import settings
from django.contrib.auth.forms import UserChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import ComplaintForm, UserUpdateForm, ProfileForm, SignupForm

from cozumburada.models import Complaint, Profile

import re

from .tokens import account_activation_token



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
        form = SignupForm(request.POST)
        if 'name' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password')
            password_again = request.POST.get('password-again')
            if not name or not email or not password or not first_name or not last_name or not password_again:
                messages.error(request, 'Lütfen tüm alanları doldurunuz.')
                return render(request, 'register.html')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email adresi kullanılıyor.')
                return render(request, 'register.html')

            if User.objects.filter(username=name).exists():
                messages.error(request, 'Kullanıcı adı kullanılıyor.')
                return render(request, 'register.html')

            if not is_valid_email(email):
                messages.error(request, 'Geçersiz bir email adresi girdiniz.')
                return render(request, 'register.html')

            if password == password_again:
                user = User.objects.create_user(username=name, email=email, password=password, first_name=first_name,
                                                last_name=last_name)
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                mail_subject = 'Hesabınızı Doğrulayın - Çözüm Burada'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return render(request, 'Email.html',
                              {'msg': 'Please confirm your email address to complete the registration',
                               'login_page': True})

            else:
                messages.error(request, 'Şifreler eşleşmiyor.')
                return render(request, 'register.html')
        else:
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not email and not password:
                messages.error(request, 'Lütfen bilgilerinizi girin.')
                return redirect('register_or_login')

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('anasayfa')

            if user is not activate:
                messages.error(request, 'Emailinizi doğrulayın.', extra_tags='danger')

            else:
                messages.error(request, 'Hatalı kullanıcı adı veya şifre.', extra_tags='danger')
                pass
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form': form})



def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'Email.html', {'msg': 'Email adresinizi doğruladınız. Giriş yaparak şikayet yazmaya başlayabilirsiniz'})
    else:
        return render(request, 'Email.html', {'msg': 'Hesap doğrulama bağlantısı artık aktif değil.'})



def sikayet_yaz(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, user=request.user)
        if form.is_valid():
            complaint = form.save()

            if request.FILES.get('image'):
                complaint.image = request.FILES.get('image')
            complaint.save()


            # Resimlerin kaydedileceği dizinin yolu
            save_path = os.path.join(settings.MEDIA_ROOT, 'complaints', str(complaint.id))

            # Resimlerin kaydedileceği dizini oluştur
            os.makedirs(save_path, exist_ok=True)

            # Formdan gelen resimleri tek tek kaydet
            for image in request.FILES.getlist('image'):
                fs = FileSystemStorage(location=save_path)
                filename = fs.save(image.name, image)

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
    complaints_footer = Complaint.objects.order_by('-complaintDate')[:5]
    return render(request, 'complaints.html', {'complaints': complaints, 'complaints_sorted': complaints_sorted, 'complaints_footer': complaints_footer})


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
