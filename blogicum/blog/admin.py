from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Category, Location, Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author', 'text', 'category', 'pub_date',
        'location', 'created_at', 'is_published'
    )
    list_display_links = ('title',)
    list_editable = ('category', 'is_published', 'location')
    list_filter = ('is_published',)
    search_fields = ('title', 'text')
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'description', 'slug', 'is_published', 'created_at'
    )
    list_display_links = ('title',)
    list_editable = ('is_published',)
    search_fields = ('title', 'description')
    empty_value_display = '-пусто-'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'is_published', 'created_at'
    )
    list_display_links = ('name',)
    list_editable = ('is_published',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'text', 'post', 'created_at', 'is_published'
    )
    list_display_links = ('text',)
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    search_fields = ('text',)
    empty_value_display = '-пусто-'


admin.site.unregister(Group)
