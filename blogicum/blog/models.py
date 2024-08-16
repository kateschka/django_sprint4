from django.db import models
from django.contrib.auth import get_user_model

from .constants import MAX_FIELD_LENGTH, REPRESENTATION_LENGTH
from .manager import PostManager

User = get_user_model()


class BaseModel(models.Model):
    """Base model for all models in the project."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        abstract = True


class Category(BaseModel):
    """Category model."""

    title = models.CharField(
        max_length=MAX_FIELD_LENGTH,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; разрешены '
                   'символы латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:REPRESENTATION_LENGTH]


class Location(BaseModel):
    """Location model."""

    name = models.CharField(
        max_length=MAX_FIELD_LENGTH,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(BaseModel):
    """Post model."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    title = models.CharField(
        max_length=MAX_FIELD_LENGTH,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в '
                   'будущем — можно делать отложенные публикации.')
    )
    location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )

    published_objects = PostManager()
    objects = models.Manager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:REPRESENTATION_LENGTH]


class Contest(models.Model):
    title = models.CharField('Название', max_length=20)
    description = models.CharField(
        'Описание'
    )
    price = models.IntegerField(
        'Цена',
        min_value=10, max_value=100,
        help_text='Рекомендованная розничная цена'
    )
    comment = models.CharField(
        'Комментарий',
        blank=True, null=True
    )
