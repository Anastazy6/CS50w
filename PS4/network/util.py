from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

def is_following(follower, followed):
    '''
    Checks if a user (arg: follower) is following another user (arg: followed).
    Returns True if so, otherwise returns False.
    '''
    if len(Follower.objects.filter(following=follower, followed=followed)) > 0:
        return True
    return False

# It only exists because it's easier to read and understand what "likes(request.user, post)" means 
#   rather than "post.likes.all() and request.user in post.likes.all()" and why there are two
#   conditions (well, it's pointless to check if something is in a list if the list's length is 0
#   AND doing so regardless results in an error...)
def likes(user, post):
    '''
    Checks if a post has any likes at all adn then checks if a user likes the post.
    Returns True if so, otherwise returns False.
    '''
    if post.likes.all() and user in post.likes.all():
        return True
    return False

def paginate(content, page_number, paginate_by=10, user=None):
    '''
    Paginates content and prepares requested page to be displayed in the browser.
    Required arguments: 
        content: database entries which are to be displayed
        page_number: number of the page to be displated
    Optional arguments:
        paginate_by (keyworded): sets the number of entries to be displayed
                on a single page (default is 10)
    Returns a dictionary with two elements:
        "paginator": the whole, paginated content
        "page_obj": the page to be displayed
    '''
    
    paginator = Paginator(content, paginate_by)
    page_obj  = paginator.get_page(page_number)
    
    print(f"Logged in user is {user}")
    
    for page_item in page_obj:
        if hasattr(page_item, 'get_reactions'):
            page_item.reactions_data = page_item.get_reactions(user)
        #    print(f"\n{page_item.reactions_data}\n")
    
    return {
        "paginator": paginator,    
        "page_obj" : page_obj
    }

def require_method(request, method, status=400):
    '''
    Checks if the request's method matches the function's second argument.
    Returns negative JSON response, including the status code (default: 400) if the
    method is wrong. Otherwise does nothing, allowing the code execution to continue.
    Method may be a list of accepted methods. 
    '''
    if (type(method) is list) and (not request.method in method):
        return JsonResponse({"error": f"Request method must be one of the following:\
                            {', '.join(method)}."},
                            status=status)
    
    if not request.method == method:
        return JsonResponse({"error": f"{method} request required"},
                            status=status)

def logged_in_user(request):
    '''
    Returns the user if they are logged in. Otherwise returns None
    '''
    return request.user if request.user.is_authenticated else None

def get_object_if_exists(model, id):
    '''
    Returns an instance of model with given id if exists. Else returns False.
    Parametres: 
        model: specifies the database table from which you want to get the object
        id:    primary key of the object
    '''
    try:
        object = model.objects.get(pk=id)
    except ObjectDoesNotExist:
        return False
    return object
    
def get_reaction_if_exists(post_id=None, user_id=None):
    try: 
        reaction = Reaction.objects.get(post_id=post_id, user_id=user_id)
    except ObjectDoesNotExist:
        return False
    return reaction

def filter_shadowbans(request, posts):
    '''
    Prevents loading posts from shadowbanned users as long as the logged in user
    is not a superuser (e.g. admin). Superusers get to see shadobanned users' posts
    for the sake of moderation, unbanning etc.
    '''
    if request.user.is_superuser:
        return posts
    return posts.filter(Q(author__shadowbanned=False) | Q(author=request.user.id))