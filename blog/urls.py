from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

app_name = 'blog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post-list/<str:title>/', views.PostListView.as_view(),
         name='post_list'),
    path('post-detail/<slug:slug>/',
         views.PostDetailView.as_view(), name='post_detail'),
    path('create-post/<str:title>/',
         views.PostCreationView.as_view(), name='create_post'),
    path('update-post/<slug:slug>/', views.PostUpdationView.as_view(),
         name='update_post'),
    path('delete-post/<slug:slug>/', views.PostDeletionView.as_view(),
         name='delete_post'),
    path('create-comment/<slug:slug>/', views.CommentCreationView.as_view(),
         name='create_comment'),
    path('signup/', views.SignUpView.as_view(
        template_name='blog/signup.html'), name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='blog/logout.html'), name='logout'),
    ]