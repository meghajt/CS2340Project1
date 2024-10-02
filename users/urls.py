from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import CustomPasswordResetConfirmView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('landing/', views.landing, name='landing'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
         name='password_reset_complete'),
    path('add-favorite/', views.add_favorite, name='add_favorite'),
    path('list-favorites/', views.list_favorites, name='list_favorites'),
    path('write-review/', views.write_review, name='write_review'),
    path('list-reviews/', views.list_reviews, name='list_reviews'),
    path('all-reviews/', views.all_reviews, name='all_reviews'),
    path('password-reset/', views.password_reset_custom_view, name='password_reset'),
    path('profile/', views.profile, name='profile'),  # Add this path for the landing page
]