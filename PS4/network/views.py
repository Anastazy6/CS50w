from ctypes import sizeof
from itertools import count
import json
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .forms import *
from . import util

def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    
    paginator   = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)

    print(f"Page {page_number}, has previous: {page_obj.has_previous()}, has next: {page_obj.has_next()}")

    return render(request, "network/index.html", {
        "new_post_form": NewPostForm,
        "paginator"    : paginator,    
        "page_obj"     : page_obj
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

@login_required
def new_post(request):
    if not request.method == 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    
    title = data.get("title", "")
    body  = data.get("body",  "")

    if body == None:
        return JsonResponse({'error': "Post body required."}, status=400)
    
    new_post = Post(
        title  = title,
        body   = body,
        author = request.user
    )
    new_post.save()
    
    return JsonResponse(   {'message': "Post created successfully!",
                            'success': True},
                            status=200)

def profile(request, profile_id):
    profile = User.objects.get(pk=profile_id)
    posts = Post.objects.filter(author=profile_id).order_by('-timestamp')

    paginator   = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)
    
    return render(request, "network/profile.html", {
        'paginator'    : paginator,
        'page_obj'     : page_obj,
        "new_post_form": NewPostForm,
        'posts'        : posts,
        'profile'      : profile,
        'followers'    : Follower.objects.filter(followed=profile).count(),
        'following'    : Follower.objects.filter(following=profile).count(),
        'follow_button': "Unfollow" if util.is_following(request.user, profile) else "Follow"
    })

@login_required
def follow(request):
    if not request.method == 'POST':
        return JsonResponse({"error": "POST request required"}, status=400)

    data = json.loads(request.body)

    print(data)

    follower = User.objects.get(pk=data.get("follower", ""))
    followed = User.objects.get(pk=data.get("followed", ""))

    if not follower == request.user:
        return JsonResponse({"error": "Unauthorized access"}, status=403)
    
    # Ensure the user cannot follow themselves
    if follower == followed:
        print("The user tried to follow themselves")
        return JsonResponse({"error": "You cannot follow yourself!"}, status=400)
    
    relation = Follower.objects.filter(following=follower, followed=followed)
    print(relation)
    if len(relation) == 0:
        Follower(following=follower, followed=followed).save()
    else:
        relation.delete()
    
    return JsonResponse({'data': data}, status=200)
    

@login_required
def following(request):
    followed = []
    for person in Follower.objects.filter(following=request.user):
        followed.append(person.followed.id)
        print(followed)
    
    posts = Post.objects.filter(author__in=followed)

    paginator   = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        'posts'    : posts,
        'paginator': paginator,
        'page_obj' : page_obj,
    })
    posts