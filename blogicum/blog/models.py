from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from .constants import MAX_FIELD_LENGTH, REPRESENTATION_LENGTH
from .manager import PublishedPostManager

User = get_user_model()


class BaseModelWithCreatedAtField(models.Model):
    """
    Base model for all models in the project.
    Adds created_at field to the model.
    """

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        abstract = True


class BaseModel(BaseModelWithCreatedAtField):
    """
    Base model for models in the project.
    Adds is_published field to the model.
    """

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
        ordering = ('title',)

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
        ordering = ('name',)

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
    image = models.ImageField(
        upload_to='posts',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    objects = models.Manager()
    published_objects = PublishedPostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:REPRESENTATION_LENGTH]

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=(self.pk,))


class Comment(BaseModelWithCreatedAtField):
    """Comment model."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Публикация'
    )
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ('created_at',)

    def __str__(self):
        return self.text[:REPRESENTATION_LENGTH]
