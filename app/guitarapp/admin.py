from django.contrib import admin
from .models import Song, Review


class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'nr_viewed', 'author', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'author', 'category')


admin.site.register(Song, SongAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('song', 'rating', 'comment')
    list_filter = ('rating',)
    search_fields = ('song', 'comment')


admin.site.register(Review, ReviewAdmin)