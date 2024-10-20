from django.urls import path
from .views import index, post_detail, category_posts, profile
from . import views

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('category/<slug:post_category>/', category_posts, name='category_posts'),
    path('profile/<username>/', profile, name='profile'),
    path(
        'posts/<int:pk>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:pk>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post'
    ),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('posts/<post_id>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    path(
        'edit_profile/',
        views.ProfileUpdateView.as_view(),
        name='edit_profile'
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:pk>/',
        views.CommentUpdateView.as_view(),
        name='edit_comment'
    ),
    path(
        'posts/<post_id>/delete_comment/<int:pk>/',
        views.CommentDeleteView.as_view(),
        name='delete_comment'
    ),
]
