from pyexpat import model
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    category = models.CharField(max_length=50)
    price = models.IntegerField()
    fixed_bid = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    current_bid = models.IntegerField(null=True, blank= True)
    active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='images/')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='winning_list')

    def __str__(self):
        return f"{self.title} by {self.seller.username}"

class Bid(models.Model):
    bidder = models.ForeignKey(User,on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE,related_name="bid_list")
    bid_amount = models.IntegerField(null=True, blank= True)
    bid_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"bid of {self.bid_amount} by {self.bidder.user} on {self.listing.title}"


class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    comment_time = models.DateField(auto_now_add=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE,related_name="comment_list")

    def __str__(self):
        return f"{self.content} by {self.commenter.username} on {self.listing.title}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE,related_name="watch_list")

    def __str__(self):
        return f"{self.user}'s Watchlist"

