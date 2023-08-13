from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.contrib.auth.decorators import login_required
from .models import User, Post, Follow, Like


@login_required(login_url='/login')
def index(request):

    # Get the all the posts
    posts = Post.objects.all().order_by('-date')

    # Get all the Like objects
    likes = Like.objects.all()

    # Check if the user has liked any posts
    # Create an empty list to store all post that user has liked
    liked = []

    # Check by looping through each Like objects
    try:
        for like in likes:

            # if user has liked
            if like.user == request.user:

                # Append to the list
                liked.append(like.post.id)

    # Except that user did not like any post
    except:

        # list is remain empty
        liked = []

    # Create paginator
    paginator = Paginator(posts, 10)

    # Get the page number
    page_number = request.GET.get('page')

    # Get all posts in the page
    page = paginator.get_page(page_number)

    # Render index page
    return render(request, "network/index.html", {
        "page": page,
        "liked": liked
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


@login_required(login_url='/login')
def new_post(request):

    # Check the request method
    if request.method == "POST":

        # Get the data user post to server
        user = request.user
        content = request.POST['content']

        # Create new Post object
        post = Post(
            author=user,
            content=content
        )

        # Save new object
        post.save()

        # Redirect back to main page
        return HttpResponseRedirect(reverse("index"))


@login_required(login_url='/login')
def profile(request, user_id):

    # Get the current user
    current_user = User.objects.get(pk=user_id)

    # Get the all the posts
    posts = Post.objects.filter(author=current_user).order_by('-date')

    # Get the follower of current user
    followers = Follow.objects.filter(following=current_user)

    # Get the the following of current user
    following = Follow.objects.filter(follower=current_user)

    # Check if user already followed the person or not
    try:

        # Check if user in the list of followers for person's profile
        if len(followers.filter(follower=User.objects.get(pk=request.user.id))) != 0:

            # User did follow the person profile
            is_following = True

        # Otherwise
        else:

            # The user did not follow
            is_following = False

    # Error handler
    except:

        # Set the following check is False as the user did not follow
        is_following = False

    # Get all the Like objects
    likes = Like.objects.all()

    # Check if the user has liked any posts
    # Create an empty list to store all post that user has liked
    liked = []

    # Check by looping through each Like objects
    try:
        for like in likes:

            # if user has liked
            if like.user == request.user:

                # Append to the list
                liked.append(like.post.id)

    # Except that user did not like any post
    except:

        # list is remain empty
        liked = []

    # Create paginator
    paginator = Paginator(posts, 10)

    # Get the page number
    page_number = request.GET.get('page')

    # Get all posts in the page
    page = paginator.get_page(page_number)

    # Render profile page
    return render(request, "network/profile.html", {
        "page": page,
        "username": current_user.username,
        "followers": followers,
        "following": following,
        "is_following": is_following,
        "profile_owner": current_user,
        "liked": liked
    })


@login_required(login_url='/login')
def follow(request):

    # Get the owner of the profile
    profile_owner = User.objects.get(username=request.POST['profile_owner'])

    # Get the current user
    current_user = request.user

    # Create new Follow object
    f = Follow(
        follower=current_user,
        following=profile_owner
    )

    # Save the new Follow object
    f.save()

    # Redirect back to profile page
    return HttpResponseRedirect(reverse("profile", kwargs={"user_id": profile_owner.id}))


@login_required(login_url='/login')
def unfollow(request):

    # Get the owner of the profile
    profile_owner = User.objects.get(username=request.POST['profile_owner'])

    # Get the current user
    current_user = request.user

    # Create new Follow object
    f = Follow.objects.get(
        follower=current_user,
        following=profile_owner
    )

    # Save the new Follow object
    f.delete()

    # Redirect back to profile page
    return HttpResponseRedirect(reverse("profile", kwargs={"user_id": profile_owner.id}))


@login_required(login_url='/login')
def following(request):

    # Get the current user
    current_user = request.user

    # Get the list of all person that current user is following
    following_people = Follow.objects.filter(follower=current_user)

    # Get all the posts
    posts = Post.objects.all().order_by("-date")

    # Create a list to store all the posts
    following_posts = []

    # Loop through each post to check if the post was posted by person who current user is following
    for post in posts:

        # Loop through each person in following list
        for person in following_people:

            # Chek if post's author in following list of current user
            if post.author == person.following:

                # Append post to the list
                following_posts.append(post)

    # Get all the Like objects
    likes = Like.objects.all()

    # Check if the user has liked any posts
    # Create an empty list to store all post that user has liked
    liked = []

    # Check by looping through each Like objects
    try:
        for like in likes:

            # if user has liked
            if like.user == request.user:

                # Append to the list
                liked.append(like.post.id)

    # Except that user did not like any post
    except:

        # list is remain empty
        liked = []

    # Create paginator
    paginator = Paginator(following_posts, 10)

    # Get the page number
    page_number = request.GET.get('page')

    # Get all posts in the page
    page = paginator.get_page(page_number)

    # Render following page
    return render(request, "network/following.html", {
        "page": page,
        "liked": liked
    })


@login_required(login_url='/login')
def edit(request, post_id):

    # Check the request method
    if request.method == "POST":

        # Get data from user
        data = json.loads(request.body)

        # Get the post that user want to edit
        post = Post.objects.get(pk=post_id)

        # Get the content of the post
        post.content = data["content"]

        # Save the new content
        post.save(update_fields=["content"])

        # Return edited content
        return JsonResponse(data["content"], safe=False)


@login_required(login_url='/login')
def like(request, post_id):

    # Get the post user want to like
    post = Post.objects.get(pk=post_id)

    # Get the current user
    current_user = request.user

    # Create new Like object
    new_like = Like(
        user=current_user,
        post=post
    )

    # Save the new Like object
    new_like.save()

    # Get the number of likes of this post
    like_count = post.liked_post.count()

    return JsonResponse(like_count, safe=False)


@login_required(login_url='/login')
def unlike(request, post_id):

    # Get the post user want to like
    post = Post.objects.get(pk=post_id)

    # Get the current user
    current_user = request.user

    # Get the Like object
    old_like = Like.objects.filter(user=current_user, post=post)

    # Save the new Like object
    old_like.delete()

    # Get the number of likes of this post
    like_count = post.liked_post.count()

    return JsonResponse(like_count, safe=False)
