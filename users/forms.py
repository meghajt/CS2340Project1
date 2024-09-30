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

class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    security_question = forms.CharField(max_length=255)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        security_question = cleaned_data.get('security_question')

        # Check if the user with the provided email exists
        try:
            user = User.objects.get(email=email)
            if user.first_name != first_name or user.last_name != last_name:
                raise forms.ValidationError("Name details don't match our records.")
            if not hasattr(user, 'profile') or user.profile.security_question != security_question:
                raise forms.ValidationError("Security question doesn't match.")
        except User.DoesNotExist:
            raise forms.ValidationError("User with this email does not exist.")
        
        return cleaned_data

