from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import CustomPostForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Author
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings


@login_required
def create_post(request):
    if request.method == 'POST':
        form = CustomPostForm(request.POST)
        if form.is_valid():
            Post.objects.create(
                author=request.user,
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content']
            )
            return redirect('user_posts')
    else:
        form = CustomPostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def user_posts(request):
    posts = Post.objects.filter(author=request.user, is_deleted=False)
    return render(request, 'user_posts.html', {'posts': posts})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user, is_deleted=False)
    if request.method == 'POST':
        form = CustomPostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.save()
            return redirect('user_posts')
    else:
        form = CustomPostForm(initial={'title': post.title, 'content': post.content})
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.is_deleted = True
    post.save()
    return redirect('user_posts')


def User_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                Author.objects.create(user=user)  # Link to Author model
                messages.success(request, "Registration successful!")
                return redirect('login')  # Change to your login URL name
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful!")
            return redirect('register')  # Change to your login URL name
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if request.POST.get('terms') != 'on':
            messages.error(request, 'You must agree to the terms and conditions.')
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('login')
    return render(request, 'login.html')


@login_required(login_url='login')
def dashboard(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'dashboard.html', {'posts': posts})


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')

def subscription_plans(request):
    return render(request, 'subscription.html')  

import razorpay # type: ignore

def payment_page(request, plan):
    price_map = {'basic': 99, 'standard': 199, 'premium': 299}
    price = price_map.get(plan.lower(), 99)
    return render(request, 'payment.html', {'price': price})

def payment_success(request):
    send_mail(
        subject="Subscription Confirmation",
        message="Your subscription has been successfully activated!",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],  
    )
    return render(request, 'email_success.html')