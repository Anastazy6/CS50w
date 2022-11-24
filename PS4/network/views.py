from ctypes import sizeof
from itertools import count
import json
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .forms import *
from .util import *

########################################################
############## Login. logout. register #################
########################################################

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

##################################################
################# Display views ##################
##################################################

def index(request):
    content = paginate(Post.objects.all().order_by('-timestamp'),
                            request.GET.get('page'),
                            user=logged_in_user(request))
    
    return render(request, "network/index.html", {
        "new_post_form": NewPostForm,
        "paginator"    : content['paginator'],    
        "page_obj"     : content['page_obj']
    })


def profile(request, profile_id):
    profile = User.objects.get(pk=profile_id)
    content = paginate(Post.objects.filter(author=profile_id).order_by('-timestamp'),
                            request.GET.get('page'),
                            user=logged_in_user(request))
    
    return render(request, "network/profile.html", {
        'paginator'    : content['paginator'],
        'page_obj'     : content['page_obj'],
        "new_post_form": NewPostForm,
        'profile'      : profile,
        'followers'    : Follower.objects.filter(followed=profile).count(),
        'following'    : Follower.objects.filter(following=profile).count(),
        'follow_method': "Unfollow" if is_following(request.user, profile) else "Follow"
    })


@login_required
def following(request):
    followed = []
    for person in Follower.objects.filter(following=request.user):
        followed.append(person.followed.id)

    content = paginate(Post.objects.filter(author__in=followed).order_by('-timestamp'),
                            request.GET.get('page'),
                            user=logged_in_user(request))

    return render(request, "network/following.html", {
        'paginator'    : content['paginator'],
        'page_obj'     : content['page_obj'],
    })

##################################################
######## Data creation and modification ##########
##################################################

@login_required
def new_post(request):
    require_method(request, 'POST')

    data  = json.loads(request.body)
    title = data.get("title", "")
    body  = data.get("body",  "")

    if body == None:
        return JsonResponse(
            {   'error': "Post body required."
            },  status = 400)
    
    Post(
        title  = title,
        body   = body,
        author = request.user
    ).save()
    
    return JsonResponse(   {'message': "Post created successfully!",
                            'success': True},
                            status   = 200)



@login_required
def follow(request):
    require_method(request, ['GET', 'POST'])

    if request.method == 'POST':
        data     = json.loads(request.body)
        follower = User.objects.get(pk=data.get("follower", ""))
        followed = User.objects.get(pk=data.get("followed", ""))

        if not follower == request.user:
            return JsonResponse(
                {   "error": "Unauthorized access"
                },  status = 403)
        
        # Ensure the user cannot follow themselves
        if follower == followed:
            print("The user tried to follow themselves")
            return JsonResponse(
                {   "error": "You cannot follow yourself!"
                },  status = 400)
        
        relation = Follower.objects.filter(following=follower, followed=followed)
        if len(relation) == 0:
            Follower(following=follower, followed=followed).save()
        else:
            relation.delete()
        
        return JsonResponse(
            {   'data'   : data,
                'success': True
            },  status   = 200)

    # GET
    else:    
        return JsonResponse(
            {   'followers'    : Follower.objects.filter(followed= request.GET['followed']).count(),
                'following'    : Follower.objects.filter(following=request.GET['followed']).count(),
                'follow_method': "Unfollow" if is_following(request.user,
                                        request.GET['followed']) else "Follow"
            },  status=200)



@login_required
def edit_post(request, post_id):
    require_method(request, 'POST')

    data = json.loads(request.body)
    post = Post.objects.get(pk=post_id)

    if not post.author == request.user:
        return JsonResponse({"error": "Unauthorized access. One does not simply\
                            edit other users' posts!"}, status=403)

    if not int(data['post_id']) == int(post_id):
        return JsonResponse({"warning": "Post ID in form action and input field named 'post-id'\
                            don't match. Client-side modification detected. Note: even properly\
                            modifying both values won't let you edit other users' posts.\
                            This security measure only exists to make it less probable for you\
                            to accidentally edit your other post if you were playing with dev tools."},
                            status=418)

    post.title = data['title']
    post.body  = data['body']
    post.save()

    return JsonResponse({
        "new_title": post.title,
        "new_body" : post.body 
    },  status     = 200)



@login_required
def like_post(request, post_id):
    require_method(request, 'POST')

    post = Post.objects.get(pk=post_id)

    if request.user == post.author:
        return JsonResponse({
            'error': 'You cannot like your own posts! You better hate yourself too!'
        },  status = 418)

    if likes(request.user, post):
        action = "dislike"
        post.likes.remove(request.user)
    else:
        action = "like"
        post.likes.add(request.user)

    return JsonResponse({   'user'  : request.user.username,
                            'post'  : post.id,
                            'author': post.author.username,
                            'action': action,
                            'likes' : post.total_likes()
                        },  status  = 200)



def get_reactions(request, post_id):
    require_method(request, 'GET')
    
    post = get_post_if_exists(post_id)
    if not post:
        return JsonResponse(
            {   'error': f"Post with id: {post_id} does not existt"
            },  status = 400)

    return JsonResponse(post.get_reactions(user=logged_in_user(request)),
                        status=200)



def react_to_post(request, post_id):
    require_method(request, 'POST')

    post = get_post_if_exists(post_id)
    if not post:
        return JsonResponse({
            'error': f"Post with id: {post_id} does not existt"
        },  status = 400)

    if request.user == post.author:
        return JsonResponse({
            'error': 'You cannot react to your own posts!'
        },  status = 418)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required!'}, status=403)

    data         = json.loads(request.body)
    reaction     = get_reaction_if_exists(post_id=post.id, user_id=request.user.id)
    new_reaction = Reaction(post_id=post.id, user_id=request.user.id, category_id=data['id'])

    if not reaction:
        new_reaction.save()
        action = 'create'
    
    # Clicked reaction's category is different than the current reaction's category
    elif not int(reaction.category.id) == int(data['id']):
        reaction.category_id = data['id']
        reaction.save()
        action = 'change' 

    else:
        reaction.delete()
        action = 'delete'

    return JsonResponse(   {'action': action,
                            'data'  : new_reaction.serialize_short()
                        },  status  = 200)


@login_required
def get_rcategories(request):
    require_method(request, 'GET')
    
    result = {}
    for category in ReactionCategory.objects.all():
        result[category.id] = { "reaction": category.reaction,
                                "emoji"   : category.emoji }

    return JsonResponse(result, status=200)

