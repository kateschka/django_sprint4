"""Views for the blog app."""

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import PostForm, CommentForm, ProfileForm
from .models import Category, Post, Comment, User
from .constants import POSTS_PER_PAGE


def index(request: HttpRequest) -> HttpResponse:
    """Display the index page."""
    posts = Post.published_objects.all().prefetch_related('comments')
    return render(
        request,
        'blog/index.html',
        {
            'page_obj': get_page_obj(posts, request)
        })


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """Display a post by id."""
    post = get_object_or_404(Post, pk=post_id)
    if not post.is_published and request.user != post.author:
        raise Http404
    return render(
        request,
        'blog/detail.html',
        {
            'post': post,
            'comments':
                Comment.objects.filter(post=post_id).select_related('author'),
            'form': CommentForm()
        }
    )


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """Display all posts by category."""
    posts = Post.published_objects.filter(
        category__slug=category_slug)
    return render(
        request,
        'blog/category.html',
        {
            'category': get_object_or_404(
                Category,
                slug=category_slug,
                is_published=True
            ),
            'page_obj': get_page_obj(posts, request)
        }
    )


def profile(request: HttpRequest, username: str) -> HttpResponse:
    """Display a user profile."""
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    return render(
        request,
        'blog/profile.html',
        {
            'profile': user,
            'page_obj': get_page_obj(posts, request)
        }
    )


@login_required
def edit_profile(request: HttpRequest) -> HttpResponse:
    """Display a user profile."""
    user = get_object_or_404(User, username=request.user.username)
    posts = Post.objects.filter(author=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = ProfileForm(instance=user)
    return render(
        request,
        'blog/user.html',
        {
            'profile': user,
            'page_obj': get_page_obj(posts, request),
            'form': form
        }
    )


def get_page_obj(posts, request):
    """Get page for Paginator."""
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


@login_required
def create_or_edit_post(request: HttpRequest, post_id=None) -> HttpResponse:
    """Create or edit a post."""
    if post_id is not None:
        instance = get_object_or_404(Post, pk=post_id)
        if request.user != instance.author:
            return redirect('blog:post_detail', post_id=post_id)
    else:
        instance = None
    form = PostForm(
        request.POST or None,
        instance=instance,
        files=request.FILES or None
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')
        post.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, post_id):
    """Delete a post."""
    instance = get_object_or_404(Post, pk=post_id)
    form = PostForm(instance=instance)
    if request.method == 'POST' and request.user == instance.author:
        instance.delete()
        return redirect('blog:profile', username=request.user.username)
    return render(
        request,
        'blog/create.html',
        {'form': form}
    )


@login_required
def create_or_edit_comment(request, post_id, comment_id=None):
    """Create or edit a comment."""
    if comment_id is not None:
        instance = get_object_or_404(Comment, pk=comment_id, post_id=post_id)
    else:
        instance = None
    form = CommentForm(request.POST or None, instance=instance)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = get_object_or_404(Post, pk=post_id)
        comment.save()
        return redirect('blog:post_detail', post_id=comment.post.pk)
    return render(
        request,
        'blog/comment.html',
        {
            'form': form,
            'comment': get_object_or_404(Comment, pk=comment_id)
        })


@login_required
def delete_comment(request, post_id, comment_id):
    """Delete a comment."""
    instance = get_object_or_404(Comment, pk=comment_id, post_id=post_id)
    form = CommentForm(instance=instance)
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(
        request,
        'blog/comment.html',
        {'form': form}
    )
