"""Utility functions for blog app."""
from django.core.paginator import Paginator
from .constants import QUERIES_PER_PAGE


def get_page_obj(queryset, request):
    """Get page for Paginator."""
    paginator = Paginator(queryset, QUERIES_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
