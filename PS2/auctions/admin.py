from logging.handlers import WatchedFileHandler
from django.contrib import admin

from .models import *

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'description', 'seller', 'category',\
                    'starting_price', 'buyout_price', 'creation_date',\
                    'active', 'winner')

class BidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'bidder', 'bid_value', 'bid_date')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'auction', 'value')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',\
                    'date_joined', 'last_login', 'is_active',\
                    'is_staff', 'is_superuser')

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('watcher', 'auction')

# Register your models here.
admin.site.register(Auction,   AuctionAdmin)
admin.site.register(Bid,       BidAdmin)
admin.site.register(Category)
admin.site.register(Comment,   CommentAdmin)
admin.site.register(User,      UserAdmin)
admin.site.register(Watchlist, WatchlistAdmin)