from django.db import models
from django.contrib.auth.models import User

class FavoriteRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=255)
    restaurant_address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.restaurant_name} ({self.user.username})"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=255)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    review_text = models.TextField()

    def __str__(self):
        return f"{self.restaurant_name} ({self.rating}/5 by {self.user.username})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    security_question = models.CharField(max_length=255)
    security_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username