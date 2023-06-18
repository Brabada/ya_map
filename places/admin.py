from django.contrib import admin
from django.utils.html import format_html

from .models import Place, Image

from adminsortable2.admin import SortableTabularInline, SortableAdminMixin
# Register your models here.


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


class ImageInline(SortableTabularInline, admin.TabularInline):
    model = Image
    readonly_fields = ['place_preview']
    fields = ['image', 'place_preview', 'order', ]


    def place_preview(self, obj):
        return (
            format_html(
                f'<img src={obj.image.url} width=200px />'
            )
        )


@admin.register(Place)
class PlaceAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]






