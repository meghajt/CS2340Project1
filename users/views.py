from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .forms import UserRegisterForm, CustomUserCreationForm, FavoriteRestaurantForm, ReviewForm, CustomPasswordResetForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import FavoriteRestaurant, Review, UserProfile
from django.http import JsonResponse
import json
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.models import User

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

def password_reset_custom_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        security_question = request.POST.get('security_question')
        security_answer = request.POST.get('security_answer')

        try:
            user = User.objects.get(email=email, first_name=first_name, last_name=last_name)
            user_profile = UserProfile.objects.get(user=user)

            if (user_profile.security_question == security_question and
                user_profile.security_answer.lower() == security_answer.lower()):

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                return redirect('password_reset_confirm', uidb64=uidb64, token=token)

            else:
                messages.error(request, "Details don't match our records. Please try again.")
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            messages.error(request, "Details don't match our records. Please try again.")

    return render(request, 'users/password_reset.html')

class CustomPasswordResetView(auth_views.PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('password_reset_done')

def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                security_question=form.cleaned_data.get('security_question'),
                security_answer=form.cleaned_data.get('security_answer')
            )
            return redirect('login')
    else:
        form = CustomUserCreationForm()

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

@login_required
def write_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('list_reviews')
    else:
        form = ReviewForm()

    return render(request, 'users/write_review.html', {'form': form})

@login_required
def list_reviews(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'users/list_reviews.html', {'reviews': reviews})

def all_reviews(request):
    reviews = Review.objects.all()  # Get all reviews from all users
    return render(request, 'users/all_reviews.html', {'reviews': reviews})

@login_required
def profile(request):
    user = request.user
    reviews_count = Review.objects.filter(user=user).count()
    favorites_count = FavoriteRestaurant.objects.filter(user=user).count()

    context = {
        'user': user,
        'reviews_count': reviews_count,
        'favorites_count': favorites_count,
    }
    return render(request, 'users/profile.html', context)

