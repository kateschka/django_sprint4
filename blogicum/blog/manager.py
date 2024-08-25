from django.db.models import Manager
from django.db.models.query import QuerySet
from django.utils.timezone import now
from django.db.models import Count


class PostManager(Manager):
    """Custom manager for the Post model."""

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().select_related(
            'author', 'category', 'location'
        ).filter(
            is_published=True,
            pub_date__lte=now(),
            category__is_published=True,
        ).order_by(
            '-pub_date'
        ).annotate(
            comment_count=Count('comments'))

    def get_all_for_author(self, user) -> QuerySet:
        """Return all posts of a given author, including unpublished ones."""
        return super().get_queryset().select_related(
            'author', 'category', 'location'
        ).filter(
            author=user
        ).order_by(
            '-pub_date'
        ).annotate(
            comment_count=Count('comments'))

    def get_all_for_user(self, user) -> QuerySet:
        """Return all published posts of a given author."""
        return self.get_queryset().filter(author=user)
