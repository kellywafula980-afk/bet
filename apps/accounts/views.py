from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from .forms import RegisterForm, LoginForm
from apps.wallet.models import Wallet
from django.contrib.auth import get_user_model

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Wallet.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, "Registration successful! Your wallet has been created.")
            return redirect('games:wheel')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            return redirect('games:wheel')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

def create_admin(request, key):
    # Check if the key is exactly 'candy'
    if key != 'candy':
        return HttpResponse("Invalid key", status=401)
    if User.objects.filter(is_superuser=True).exists():
        return HttpResponse("Admin already exists", status=400)
    # Hardcoded admin credentials
    phone_number = "0702872541"
    pin = "1234"
    user = User.objects.create_superuser(
        phone_number=phone_number,
        password=pin
    )
    Wallet.objects.get_or_create(user=user)
    return HttpResponse(f"Admin user with phone {phone_number} created successfully.")
