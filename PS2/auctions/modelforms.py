from django import forms
from django.forms import Textarea
from .models import *

class NewAuctionForm(forms.ModelForm):
    class Meta:
        model   =  Auction
        fields  =  ['item_name', 'description', 'image_url',
                    'category', 'starting_price', 'buyout_price']
        widgets =  {'description': Textarea(attrs={'cols': 80, 'rows': 20})}

class WatchlistForm(forms.ModelForm):
    class Meta:
        model   =  Watchlist
        exclude =  ['watcher', 'auction']

class BidForm(forms.ModelForm):
    class Meta:
        model   =  Bid
        fields  =  ['bid_value']

class CommentForm(forms.ModelForm):
    class Meta:
        model   =  Comment
        fields  =  ['value']
        widgets =  {'value': Textarea(attrs={   'cols': 80,
                                                'rows': 4,
                                                'placeholder': "Type your comment here.",
                                                })}
        labels  =  {'value': ''}