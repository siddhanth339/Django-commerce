from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    my_items = models.ManyToManyField('Auction_Listings', blank = True, related_name="users")

class Auction_Listings(models.Model):
    title = models.CharField(max_length = 20)
    description = models.TextField(max_length = 300)
    starting_bid = models.IntegerField()
    image_url = models.URLField(default = "https://media.sproutsocial.com/uploads/2017/02/10x-featured-social-media-image-size.png")

    CHOICES = [
        ("FA", 'Fashion'),
        ("EL", 'Electronics'),
        ("HO", 'Home'),
        ("MU", 'Music'),
        ("BO", 'Books')
    ]
    
    category = models.CharField(max_length = 20, choices = CHOICES, default = "FA")
    date = models.DateTimeField(auto_now_add=True)
    current_bid = models.IntegerField()
    owner = models.ForeignKey(User, on_delete = models.CASCADE, default = 1)

