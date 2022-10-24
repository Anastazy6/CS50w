from .models import *

def is_following(follower, followed):
    '''
    Checks if a user (arg: follower) is following another user (arg: followed).
    Returns True if so, otherwise returns False.
    '''
    if len(Follower.objects.filter(following=follower, followed=followed)) > 0:
        return True
    return False

    