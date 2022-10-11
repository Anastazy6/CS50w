from this import d
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):

    def has_won_auctions(self):
        if len(Auction.objects.filter(winner=self)) > 0:
            return True
        return False
    
    def __str__(self) -> str:
        return f'{self.username}'

class Category(models.Model):
    category        = models.CharField      (max_length=32, primary_key=True, default="Uncategorized")
    
    def __str__(self) -> str:
        return f'{self.category}'

class Auction(models.Model):
    active          = models.BooleanField   (default=True)
    buyout_price    = models.DecimalField   (max_digits=16, decimal_places=2)
    category        = models.ForeignKey     (Category, on_delete=models.SET_DEFAULT, related_name='categories', default="Uncategorized"   )
    creation_date   = models.DateTimeField  (auto_now_add=True)
    description     = models.CharField      (max_length=2137)
    image_url       = models.URLField       (null=True, blank=True, default=None)
    item_name       = models.CharField      (max_length=69)
    seller          = models.ForeignKey     (User,     on_delete=models.PROTECT,     related_name="sellers")
    starting_price  = models.DecimalField   (max_digits=16, decimal_places=2)
    winner          = models.ForeignKey     (User, null=True, blank=True, on_delete=models.CASCADE, related_name='winners', default=None)

    def is_biddable(self):
        if float(self.buyout_price) == float(self.starting_price):
            return False
        return True

    def buyout_to_f(self):
        return float(self.buyout_price)

    def starting_to_f(self):
        return float(self.starting_price)

    def __str__(self):
        return f'"{self.item_name}" posted by "{self.seller}". Price range: {self.starting_price} --- {self.buyout_price}.'

class Bid(models.Model):
    auction         = models.ForeignKey     (Auction,  on_delete=models.CASCADE,     related_name='items')
    bidder          = models.ForeignKey     (User,     on_delete=models.CASCADE,     related_name='bidders')
    bid_value       = models.DecimalField   (max_digits=16, decimal_places=2)
    bid_date        = models.DateTimeField  (auto_now_add=True)

    def to_f(self):
        return float(self.bid_value)

    def __str__(self) -> str:
        return f'A bid on "{self.auction}" by "{self.bidder}" for {self.bid_value}. Bidded on {self.bid_date}.'

class Comment(models.Model):
    author          = models.ForeignKey     (User,     on_delete=models.CASCADE,     related_name='commentor')
    auction         = models.ForeignKey     (Auction,  on_delete=models.CASCADE,     related_name='auctions')
    creation_date   = models.DateTimeField  (auto_now_add=True)
    value           = models.CharField      (max_length=2137)

    def __str__(self) -> str:
        return f'A comment on "{self.auction}" by "{self.author}".'

class Watchlist(models.Model):
    watcher         = models.ForeignKey     (User,     on_delete=models.CASCADE,      related_name='watchers')
    auction         = models.ForeignKey     (Auction,  on_delete=models.CASCADE,      related_name='watched')

    def __str__(self) -> str:
        return f'{self.auction.item_name} is on {self.watcher.username}\'s watchlist.'
