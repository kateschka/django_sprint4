"""Utility functions for blog app."""
from django.core.paginator import Paginator
from django.db.models import Count

from .constants import QUERIES_PER_PAGE


def get_page_obj(queryset, request):
    """Get page for Paginator."""
    paginator = Paginator(queryset, QUERIES_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def get_comment_count(posts):
    """Get comment count for post."""
    return posts.annotate(
        comment_count=Count('comments'))
