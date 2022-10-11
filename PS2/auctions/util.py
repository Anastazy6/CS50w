from .models import *
from .modelforms import *
from django.core.exceptions import ObjectDoesNotExist


def save_new_auction(request, form):
    new_auction        = form.save(commit=False)
    new_auction.seller = request.user
    new_auction.save()
    form.save_m2m()


def save_new_bid(bidder, auction, form):
    new_bid = form.save(commit=False)
    new_bid.auction = auction
    new_bid.bidder  = bidder
    new_bid.save()
    form.save_m2m()


def auction_is_on_watchlist(user, auction):
    try:
        Watchlist.objects.get(watcher=user, auction=auction)
    except ObjectDoesNotExist:
        return False
    return True


def get_highest_bid(auction):
    '''
    Gets the highest bid on the auction, returning it as a float.
    This method INCLUDES starting price so that it works for freshly
    created (and even unbiddable) auctions as well. In such cases,
    starting price is the highest bid.
    UPDATE: now returns a tuple, where the first element is the bid value
    and the second element is the bidder.
    Return: (Float bid_value, User bidder or None if no bids were made)
    '''
    bids = Bid.objects.filter(auction=auction)
    bid_values = [(auction.starting_to_f(), None)]
    for bid in bids:
        bid_values.append((bid.to_f(), bid.bidder))
    return max(bid_values, key=lambda x:x[0])


def include_highest_bids(auctions_list):
    '''
    Gets the highest bid for each auction in the auctions_list,
    adding it as a .highest_bid property.
    '''
    for auction in auctions_list:
        auction.highest_bid = get_highest_bid(auction)
    return auctions_list


def get_auction_if_exists(auction_id):
    '''
    Checks if an auction with given ID exists, returns the auction object if so, otherwise returns None.
    ''' 
    try:
        auction = Auction.objects.get(pk=auction_id)
    except ObjectDoesNotExist:
        return None
    return auction


def switch_watchlist_status(request, auction):
    '''
    Adds an auction with given ID to the user's watchlist if it isn't there, otherwise removes it from the list.
    Gets an user - auction pair (as a list, where len == 0 means it doesn't exist), where the user is going to add
    or remove the auction from their watchlist.
    If such a pair doesn't exit (i.e. the user doesn't watch the auction), adds the auction to the user's watchlist
    as long as the auction is STILL ACTIVE. If such a pair does exist (i.e. the user has the auction on their
    watchlist) then removes it from the watchlist.
    '''
    pair = Watchlist.objects.filter(watcher=request.user, auction=auction)
    if auction.active == True and len(pair) == 0:
        Watchlist(watcher=request.user, auction=auction).save()
    elif len(pair) > 0:
        pair.delete()


def get_watchlist(user):
    '''
    Gets all auctions that are in the user's watchlist, returning them in a list.
    '''
    auctions = []
    for watchlist_instance in Watchlist.objects.filter(watcher=user):
        auctions.append(watchlist_instance.auction)
    return auctions


def process_bid(request, auction, highest_bid):
    '''
    Processess the bid.\n
    If the BidForm is valid and the bid value is correct (i.e. higher than
    the highest bid so far (or the starting price if there are no bids) and EXCLUSIVELY lower
    than buyout price (since bidding at the buyout price makes no practical sense, as there
    is a separate buyout button for that)), it saves the bid and returns True (success state).
    Otherwise returns False (failure state).\n
    Depending on success/failure state, different resolutions may take place.
    '''
    form = BidForm(request.POST)
    if form.is_valid():
        bid = float(form.cleaned_data['bid_value'])
        if bid > highest_bid[0] and bid < auction.buyout_to_f():
            save_new_bid(request.user, auction, form)
            return True
    return False


def close_auction(request, auction):
    if request.user == auction.seller:
        highest_bid = get_highest_bid(auction)
        auction.active = False
        auction.winner = highest_bid[1]
        auction.save(force_update=True)
        return True
    return False


def process_buyout(request, auction):
    if not request.user == auction.seller:
        auction.active = False
        auction.winner = request.user
        auction.save(force_update=True)
        return True
    return False


def submit_comment(request, auction):
    if request.user.is_authenticated:
        form                = CommentForm(request.POST)
        new_comment         = form.save(commit=False)
        new_comment.author  = request.user
        new_comment.auction = auction
        new_comment.save()
        form.save_m2m()
        return True
    return False