from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# @login_required(login_url='register_or_login')
def index(request):
    username = None
    user_count = User.objects.filter(is_superuser=False).count()
    if request.user.is_authenticated:
        username = request.user.username
    context = {
        'username': username,
        'user_count': user_count
    }
    return render(request, 'index.html', context)


def register_or_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if 'name' in request.POST:
            name = request.POST.get('name')
            password_again = request.POST.get('password-again')
            if password == password_again:
                user = User.objects.create_user(name, email, password)
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


# @login_required(login_url='register_or_login')
# def shikayet_yaz(request):
#     # burada şikayet yazma işlemleri yapılır
#     return render(request, 'complaint.html')

@login_required(login_url='register_or_login')
def sikayet_yaz(request):
    if request.user.is_authenticated:
        return render(request, 'complaint.html')
    else:
        return redirect('register_or_login')



def logoutPage(request):
    logout(request)
    return redirect('anasayfa')
