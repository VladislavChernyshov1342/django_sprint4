from django.urls import path
from .views import index, post_detail, category_posts, profile
from . import views

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('<int:post_id>/', post_detail, name='post_detail'),
    path('<slug:post_category>/', category_posts, name='category_posts'),
    path('profile/<username>/', profile, name='profile'),
    path(
        'posts/<post_id>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<post_id>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post'
    ),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('posts/<post_id>/comment/', views.add_comment, name='add_comment'),
]
