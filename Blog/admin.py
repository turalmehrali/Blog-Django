from django.contrib import admin
from .models import Article, Comment, Reply, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'publish_date', 'slug']


    class Meta:
        model = Article

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'slug']

    class Meta:
        model = Category


admin.site.register(Article, ArticleAdmin)
#admin.site.register(Comment)
#admin.site.register(Reply)
admin.site.register(Category, CategoryAdmin)