from django.db import models
from django.contrib.auth.models import User

class FavoriteRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=255)
    restaurant_address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.restaurant_name} ({self.user.username})"
