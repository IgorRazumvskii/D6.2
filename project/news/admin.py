from django.contrib import admin

from .models import Author, Category, Post, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'header', 'rate_of_post', 'article_or_news')
    list_display_links = ('id', 'header', 'article_or_news')
    search_fields = ('header', 'text')  #  поиск
    list_editable = ('rate_of_post',)
    #fields = ('header', 'rate_of_post', 'article_or_news', 'author')
    readonly_fields = ('date_and_time',)


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
