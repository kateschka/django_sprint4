"""Views for the blog app."""
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from .forms import PostForm, CommentForm, ProfileForm
from .models import Category, Post, Comment, User
from .constants import QUERIES_PER_PAGE


def get_page_obj(queryset, request):
    """Get page for Paginator."""
    paginator = Paginator(queryset, QUERIES_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


class IndexListView(ListView):
    """Display the index page."""

    model = Post
    template_name = 'blog/index.html'
    paginate_by = QUERIES_PER_PAGE

    def get_queryset(self):
        return Post.published_objects.all()


def category_posts(request, category_slug: str):
    """Display all posts by category."""
    posts = Post.published_objects.filter(
        category__slug=category_slug)
    context = {
        'category': get_object_or_404(
            Category,
            slug=category_slug,
            is_published=True
        ),
        'page_obj': get_page_obj(posts, request)
    }
    return render(request, 'blog/category.html', context)


def profile(request, username: str):
    """Display user profile."""
    user = get_object_or_404(User, username=username)
    if not user == request.user:
        posts = Post.published_objects.get_all_for_user(user)
    else:
        posts = Post.published_objects.get_all_for_author(user)
    context = {
        'profile': user,
        'page_obj': get_page_obj(posts, request)
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile."""
    user = get_object_or_404(User, username=request.user.username)
    posts = Post.objects.filter(author=user)
    form = ProfileForm(request.POST or None, instance=user)
    context = {
        'profile': user,
        'page_obj': get_page_obj(posts, request),
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/user.html', context)


def post_detail(request, post_id: int):
    """Display a post by id."""
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        post = get_object_or_404(Post.published_objects.all(), pk=post_id)
    comments = post.comments.select_related('author').filter(is_published=True)
    context = {
        'post': post,
        'comments': comments,
        'form': CommentForm()
    }
    return render(request, 'blog/detail.html', context)


def edit_post(request, post_id: int):
    """Edit post."""
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def create_post(request):
    """Create a post."""
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid() and request.method == 'POST':
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, post_id: int):
    """Delete post."""
    user = request.user
    post = get_object_or_404(Post, pk=post_id, author=user)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'post': post})


@login_required
def create_comment(request, post_id: int):
    """Create a comment."""
    form = CommentForm(request.POST or None)
    if form.is_valid() and request.method == 'POST':
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = get_object_or_404(Post, pk=post_id)
        comment.save()
        return redirect('blog:post_detail', post_id=comment.post.pk)
    return render(request, 'blog/comment.html', {'form': form})


def edit_comment(request, post_id: int, comment_id: int):
    """Edit comment."""
    comment = get_object_or_404(Comment, pk=comment_id)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid() and comment.author == request.user:
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(
        request,
        'blog/comment.html',
        {'form': form, 'comment': comment}
    )


@login_required
def delete_comment(request, post_id: int, comment_id: int):
    """Delete comment."""
    user = request.user
    comment = get_object_or_404(Comment, pk=comment_id, author=user)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', {'comment': comment})
