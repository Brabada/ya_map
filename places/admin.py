from django.contrib import admin
from django.utils.html import format_html
from .models import Place, Image
# Register your models here.


# admin.site.register(Place)
# admin.site.register(Image)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


class ImageInline(admin.TabularInline):
    model = Image
    readonly_fields = ['place_image']

    def place_image(self, obj):
        return(
            format_html(
                f'<img src={obj.image.url} width=200px />'
            )
        )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]






