from django.contrib import admin
from django.http import HttpRequest
from .models import MenuLink, SiteSetup


class MenuLinkInline(admin.TabularInline):
    model = MenuLink
    extra = 1


@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    inlines = MenuLinkInline,

    list_display = [
        'title',
        'description',
        'show_header',
        'show_search',
        'show_menu',
        'show_description',
        'show_pagination',
        'show_footer',
    ]

    list_display_links = [
        'title',
        'description',
    ]

    list_editable = [
        'show_header',
        'show_search',
        'show_menu',
        'show_description',
        'show_pagination',
        'show_footer',
    ]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return not SiteSetup.objects.exists()
