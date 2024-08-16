"""Views for the blog app."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Category, Post
from .constants import POSTS_PER_PAGE


def index(request: HttpRequest) -> HttpResponse:
    """Display the index page."""
    posts = Post.published_objects.all()[:POSTS_PER_PAGE]
    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """Display a post by id."""
    return render(
        request,
        'blog/detail.html',
        {'post': get_object_or_404(
            Post.published_objects.all().filter(pk=post_id))}
    )


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """Display all posts by category."""
    posts = Post.published_objects.filter(category__slug=category_slug)
    return render(
        request,
        'blog/category.html',
        {
            'category': get_object_or_404(
                Category,
                slug=category_slug,
                is_published=True
            ),
            'post_list': posts
        }
    )
