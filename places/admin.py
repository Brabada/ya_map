from django.contrib import admin
from django.utils.html import format_html

from .models import Place, Image

from adminsortable2.admin import SortableTabularInline, SortableAdminBase


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


class ImageInline(SortableTabularInline):

    model = Image
    readonly_fields = ['place_preview']
    fields = ['image', 'place_preview', 'order', ]

    def place_preview(self, image):
        return (
            format_html(
                '<img src={} height=200px />',
                image.image.url
            )
        )


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [
        ImageInline
    ]
