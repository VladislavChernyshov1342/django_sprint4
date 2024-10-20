from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from core.constants import ORDERBY
from core.utils import filter_post
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, PostForm, UserForm
from django.core.paginator import Paginator
from datetime import date
from django.db.models import Count


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        post = get_object_or_404(
            filtered_posts(Post.objects),
            pk=post_id,
        )
    comments = Comment.objects.filter(post=post)
    form = CommentForm()
    return render(request,
                  'blog/detail.html',
                  context={'post': post,
                           'comments': comments,
                           'form': form})


def filtered_posts(posts):
    return posts.select_related(
        'category',
        'location',
        'author',
    ).annotate(
        comment_count=Count('comments')
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=date.today(),
    ).order_by('-pub_date')


def category_posts(request, post_category):
    template = 'blog/category.html'
    post_list = Post.objects.filter(category__slug=post_category)
    posts_filter = filter_post(post_list)
    paginator = Paginator(posts_filter, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'category': get_object_or_404(
            Category,
            slug=post_category,
            is_published=True
        )
    }
    return render(request, template, context)


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.all().annotate(
        comment_count=Count('comments')
    )
    posts_filter = filter_post(post_list)
    posts_filter = posts_filter.order_by("-pub_date")
    paginator = Paginator(posts_filter, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, template, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
<<<<<<< HEAD

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user
        return reverse_lazy('blog:profile', kwargs={'username': username})
=======
>>>>>>> 5f8589108cda31f140d44f060126dc1459a2c46a

    def form_valid(self, form):
       form.instance.author = self.request.user
       return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user
        return reverse_lazy('blog:profile', kwargs={'username': username})

def profile(request, username):
    template = 'blog/profile.html'
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author__username=username).order_by("-pub_date").annotate(
        comment_count=Count('comments')
    )
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'profile': user, 'page_obj': page_obj}
    return render(request, template, context)


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_object = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        if self.post_object.author == self.request.user:
            return True
        if not self.request.user.is_authenticated:
            return False
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        post_id = self.post_object.id
        return redirect('blog:post_detail', post_id=post_id)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        post_id = self.object.id
        return reverse_lazy('blog:post_detail', kwargs={'post_id': post_id})


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def get_login_url(self):
        object = self.get_object()
        return reverse_lazy('blog:post_detail', kwargs={'post_id': object.pk})


#@login_required
#def add_comment(request, post_id):
#    post = get_object_or_404(Post, pk=post_id)
#    form = CommentForm(request.POST)
#    if form.is_valid():
#        comment = form.save(commit=False)
#        comment.author = request.user
#        comment.post = post
#        comment.save()
#    return redirect('blog:post_detail', post_id=post_id)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        return self.request.user


class CommentCreateView(LoginRequiredMixin, CreateView):
    post_object = None
    model = Comment
    form_class = CommentForm
    template_name = 'includes/comments.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_object = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_object
        return super().form_valid(form)

    def get_success_url(self):
        post_id = self.object.post_id
        return reverse_lazy('blog:post_detail', kwargs={'post_id': post_id})


class CommentUpdateView(UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_object = get_object_or_404(Comment, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        if self.post_object.author == self.request.user:
            return True
        if not self.request.user.is_authenticated:
            return False
        object = self.get_object()
        return object.author == self.request.user

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.object.post
        return super().form_valid(form)

    def get_success_url(self):
        post_id = self.object.post_id
        return reverse_lazy('blog:post_detail', kwargs={'post_id': post_id})


class CommentDeleteView(UserPassesTestMixin, DeleteView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.object.post
        return super().form_valid(form)

    def get_success_url(self):
        post_id = self.object.post_id
        return reverse_lazy('blog:post_detail', kwargs={'post_id': post_id})
