from django.contrib import admin

from .models import Comment, Review, Title, Category, Genre


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'rating', 'pub_date')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'text', 'author', 'pub_date')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
