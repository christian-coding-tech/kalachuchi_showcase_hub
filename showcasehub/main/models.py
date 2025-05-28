from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.
CATEGORY_CHOICES = [
    ('bags', 'Bags'),
    ('top', 'Top'),
    ('dress', 'Dress'),
    ('bottom', 'Bottom'),
]

class TeaserItem(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='teasers/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    Available = models.DateTimeField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    seller_name = models.CharField(max_length=100, default="Unknown Seller")
    store_name = models.CharField(max_length=100, default="Unknown Store")
    store_location = models.CharField(max_length=200, default="Unknown Location")
    store_link = models.URLField(default="https://example.com")

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return self.title

class CatalogItem(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='catalog/')
    description = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def is_new(self):
        return timezone.now() - self.added_at <= timedelta(days=1)

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username if self.user else 'Anonymous'}"