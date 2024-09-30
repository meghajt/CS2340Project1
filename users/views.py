from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import FavoriteRestaurantForm
from .models import FavoriteRestaurant
from django.http import JsonResponse
import json



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

@login_required
@login_required
def add_favorite(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        restaurant_name = data.get('restaurant_name')
        restaurant_address = data.get('restaurant_address')

        if restaurant_name and restaurant_address:
            favorite, created = FavoriteRestaurant.objects.get_or_create(
                user=request.user,
                restaurant_name=restaurant_name,
                restaurant_address=restaurant_address
            )
            if created:
                return JsonResponse({'message': 'Added to favorites'}, status=201)
            else:
                return JsonResponse({'message': 'Already in favorites'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def list_favorites(request):
    favorites = FavoriteRestaurant.objects.filter(user=request.user)
    return render(request, 'users/list_favorites.html', {'favorites': favorites})

