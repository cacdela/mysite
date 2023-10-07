from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='home'),

    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<str:username>', views.post_list, name='post_list'),

    path('category/', views.category_list, name='category_list'),
    path('category/new/', views.category_create, name='category_create'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),

    path('category/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),
]