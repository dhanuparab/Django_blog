from django.urls import path, include
from django.contrib import admin
from BlogApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-post/', views.create_post, name='create_post'),
    path('my-posts/', views.user_posts, name='user_posts'),
    path('edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('subscription/', views.subscription_plans, name='subscription'),
    path('pay/<str:plan>/', views.payment_page, name='pay'),
    path('payment_success/', views.payment_success, name='payment_success'),


]
