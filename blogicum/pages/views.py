"""Views for the pages app."""

from django.shortcuts import render

# Create your views here.


def about(request):
    """Display the about page."""
    return render(request, 'pages/about.html')


def rules(request):
    """Display the rules page."""
    return render(request, 'pages/rules.html')
