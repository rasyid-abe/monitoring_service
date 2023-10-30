from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.shortcuts import redirect
from apps.home.views import index

def login_view(request):

    if not request.user.is_anonymous:
        return redirect(index)
        
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
        
    return render(request, "accounts/login.html", {"form": form, "msg": msg})

def inactive_page(request):
    
    return render(request, "defaults/page-401.html", {})
