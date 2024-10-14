from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from core.constants import ORDERBY
from core.utils import filter_post
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, PostForm


def post_detail(request, post_id):
    post = Post.objects.select_related(
        'author',
        'location',
        'category',
    )
    posts_filter = filter_post(post)
    template = 'blog/detail.html'
    form = PostForm()
    context = {
        'post': get_object_or_404(posts_filter, pk=post_id),
        'form': form
    }
    return render(request, template, context)


def category_posts(request, post_category):
    template = 'blog/category.html'
    post_list = Post.objects.filter(category__slug=post_category)
    posts_filter = filter_post(post_list)
    context = {
        'post_list': posts_filter,
        'category': get_object_or_404(
            Category,
            slug=post_category,
            is_published=True
        )
    }
    return render(request, template, context)


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.all()
    posts_filter = filter_post(post_list)
    posts_filter = posts_filter.order_by("-id")[:ORDERBY]
    context = {'page_obj': posts_filter}
    return render(request, template, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
       form.instance.author = self.request.user
       return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user
        return reverse_lazy('blog:profile', kwargs={'username': username})

def profile(request, username):
    template = 'blog/profile.html'
    user = User.objects.get(username=username)
    post_list = Post.objects.filter(author__username=username)
    context = {'profile': user, 'page_obj': post_list}
    return render(request, template, context)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = '__all__'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:post_detail')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)
