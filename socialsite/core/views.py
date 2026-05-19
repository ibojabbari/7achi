from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Post


# login 
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "core/login.html", {"form": form})


# register acc
def register(request):
    print("REQUEST METHOD:", request.method)

    form = UserCreationForm(request.POST or None) #code to let browser know user will submit data eventually

    if request.method == "POST":
        print("POST RECEIVED") 

        if form.is_valid():
            form.save()
            return redirect("login")

    return render(request, "core/register.html", {"form": form}) #tell html to tell user know his password is problematic

# logout
def logout_view(request):
    logout(request)
    return redirect("login")



@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')

    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("home")

    return render(request, "core/home.html", {
        "posts": posts,
        "form": form
    })