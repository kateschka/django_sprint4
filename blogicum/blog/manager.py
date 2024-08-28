from django.db.models import Manager
from django.db.models.query import QuerySet
from django.utils.timezone import now


class PublishedPostManager(Manager):
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
        )

    def get_all_for_user(self, user) -> QuerySet:
        """Return all published posts of a given author."""
        return self.get_queryset().filter(author=user)
