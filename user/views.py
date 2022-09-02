from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate
from .forms import LoginForm, RegisterForm
from django.shortcuts import render, redirect


def index(request):
    return render(request, "index.html", {"user": request.user})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            # TODO: 회원 관리 기능-2. login 할 때 form을 활용해주세요
            form = LoginForm(request.POST)
            # TODO: 회원 관리 기능-1. /login로 접근하면 로그인 페이지를 통해 로그인이 되면서 / 경로로 redirect 시켜주세요
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/')
        else:
            form = LoginForm()
        return render(request, "login.html", {"form": form})
    else:
        return render(request, "index.html", {"user": request.user})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        # TODO: 회원 관리 기능-3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


def user_list_view(request):
    # TODO: 유저 리스트 페이지-8. user 목록은 로그인 유저만 접근 가능하게 해주세요
    if request.user.is_authenticated:
        # TODO: 유저 리스트 페이지-7. /users 에 user 목록을 출력해주세요
        user_objs = get_user_model().objects.all()
        # TODO: 유저 리스트 페이지-9. user 목록은 pagination이 되게 해주세요
        user_paginator = Paginator(user_objs, 5)
        user_page = request.GET.get('page')
        users = user_paginator.get_page(user_page)
        return render(request, "users.html", {"users": users})
    else:
        return HttpResponseRedirect('/login')
