from django.contrib import admin
from .models import Tag, Category, Page, Post


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'slug',
    ]

    list_display_links = ['name']

    search_fields = [
        'id',
        'name',
        'slug',
    ]

    ordering = ['-id']

    list_per_page = 10

    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'slug',
    ]

    list_display_links = ['name']

    search_fields = [
        'id',
        'name',
        'slug',
    ]

    list_per_page = 10

    ordering = ['-id']

    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'is_published',
    ]

    list_display_links = ['title']

    search_fields = [
        'id',
        'slug',
        'title',
        'content',
    ]

    list_per_page = 50
    list_filter = ['is_published']
    list_editable = ['is_published']
    ordering = ['-id']

    prepopulated_fields = {
        'slug': ('title',),
    }


@admin.register(Post)
class PostAdmim(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'is_published',
        'created_by',
    ]
    list_display_links = ['title']
    search_fields = [
        'id',
        'slug',
        'title',
        'excerpt',
        'content',
    ]
    list_per_page = 50
    list_filter = [
        'category',
        'is_published',
    ]
    list_editable = ['is_published']
    ordering = ['-id']
    readonly_fields = [
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    ]
    prepopulated_fields = {
        'slug': ('title',),
    }
    autocomplete_fields = [
        'tags',
        'category',
    ]
