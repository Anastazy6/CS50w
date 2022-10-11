from ctypes.wintypes import HACCEL
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util, modelforms

from .models import *

def index(request):
    return render(request, "auctions/index.html", {
        "auctions": util.include_highest_bids(Auction.objects.filter(active=True))
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_auction(request):
    if request.method == "POST":
        form = modelforms.NewAuctionForm(request.POST)
        
        if form.is_valid():
            if float(form['starting_price'].data) > float(form['buyout_price'].data):
                return render(request, "auctions/create-auction.html", {
                    'form':    form,
                    'message': "Buyout price must not lower than starting price."
                })
            util.save_new_auction(request, form)
            return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, "auctions/create-auction.html", {
            'form': modelforms.NewAuctionForm,
        })

def auction_view(request, auction_id):
    # Ensure that an auction with the ID exists.
    auction = util.get_auction_if_exists(auction_id)
    if not auction:
        return render(request, "auctions/404error.html", {
            "message": f"Sorry, auction with ID: {auction_id} does not exist."
    })
    
    # Initializing variables for both GET and POST requests.
    if 'last_method' in request.session.keys()      and \
            request.session['last_method'] == 'GET' or \
            not 'message' in request.session.keys():
        request.session['message'] = None
    
    highest_bid = util.get_highest_bid(auction)
    if request.user.is_authenticated:
        auction.on_watchlist = util.auction_is_on_watchlist(request.user, auction)

    # POST section
    if request.method == 'POST':
        request.session['last_method'] = 'POST'

        if 'watchlist-switch' in request.POST:
            util.switch_watchlist_status(request, auction) # No message

        elif 'submit-close'   in request.POST:
            if util.close_auction(request, auction):
                request.session['message'] = 'Auction closed successfully!'
            else:
                request.session['message'] = "Couldn't close the auction."

        elif 'submit-bid'     in request.POST:
            if util.process_bid(request, auction, highest_bid):
                request.session['message'] = "Bid successful!"
            else:
                request.session['message'] = "Damn it! Bid unsuccessful!"

        elif 'submit-buyout'  in request.POST:
            if util.process_buyout(request, auction):
                request.session['message'] = "Buyout successful!"
            else:
                request.session['message'] = "Crap! Buyout unsuccessful!"

        elif 'submit-comment' in request.POST:
            if util.submit_comment(request, auction):
                request.session['message'] = "Comment added successfully!"
            else:
                request.session['message'] = "Comment couldn't be added."
        # Return for POST.
        return HttpResponseRedirect(reverse('view-auction', args=(auction_id,)))
    # GET section
    else:
        request.session['last_method'] = 'GET'
        return render(request, "auctions/auction.html", {
            "auction":          auction,
            "bid_form":         modelforms.BidForm,
            "comment_form":     modelforms.CommentForm,
            "comments":         Comment.objects.filter(auction=auction),
            "highest_bid":      highest_bid,
            "watchlist_switch": modelforms.WatchlistForm,
            "message":          request.session['message']
        })

def watchlist_view(request):
    return render(request, "auctions/watchlist.html", {
        'watchlist':   util.include_highest_bids(
                            util.get_watchlist(request.user))
    })

def category_view(request, category):
    return render(request, "auctions/category.html", {
        'auctions':    util.include_highest_bids(
                            Auction.objects.filter(category=category, active=True)),
        'category': category
    })

def won_auctions_view(request):
    return render(request, "auctions/won-auctions.html", {
        'auctions':    util.include_highest_bids(
                            Auction.objects.filter(winner=request.user)),
        'page_name':   '- won auctions'
    })