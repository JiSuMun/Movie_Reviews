from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from reviews.models import Review

# Create your views here.
@login_required
def profile(request, account_pk):
    # user = request.user
    # reviews = Review.objects.filter(user=user)
    reviews = Review.objects.filter(user_id=account_pk)
    # review_count = Review.objects.filter(pk__lte=review.pk).count()
    context = {
        'reviews': reviews,
        # 'review': review,
        # 'user': user,
        # 'review_count': review_count,
    }
    return render(request, 'accounts/profile.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('reviews:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('reviews:index')
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('reviews:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('reviews:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('reviews:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def delete(request):
    request.user.delete()
    return redirect('reviews:index')


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('reviews:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form':form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('reviews:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form':form,
    }
    return render(request, 'accounts/change_password.html', context)
