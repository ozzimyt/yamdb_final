from django.contrib import admin

from .models import Category, Genre, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)


class GenreTitleInline(admin.TabularInline):
    model = Title.genre.through


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'year', 'category', 'description', 'show_genre'
    )
    search_fields = ('name', 'description',)
    list_filter = ('year', 'category', 'genre',)
    list_editable = ('category',)
    empty_value_display = '-не указано-'
    inlines = (GenreTitleInline,)

    def show_genre(self, obj):
        return ', '.join(str(value) for value in obj.genre.all())


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
