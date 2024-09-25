from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Your account has been created!')
            return redirect('home')  # Redirect to home or wherever you'd like
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def landing(request):
    return render(request, 'users/landing.html', {'username': request.user.username})
# Create your views here.

