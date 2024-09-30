from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FavoriteRestaurant
from .models import Review

class FavoriteRestaurantForm(forms.ModelForm):
    class Meta:
        model = FavoriteRestaurant
        fields = ['restaurant_name', 'restaurant_address']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['restaurant_name', 'rating', 'review_text']

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    security_question = forms.CharField(max_length=255)
    security_answer = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'security_question', 'security_answer']

