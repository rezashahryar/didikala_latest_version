from django.contrib import admin
from .models import Blog, Category, Tag, Comment, Like, DisLike


# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published_date', 'status', 'counted_views')
    list_filter = ('status', 'author')
    date_hierarchy = 'published_date'
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')
    list_per_page = 300
    # @admin.display(description='reza')
    # def is_low(self, blog):
    #     if blog.status:
    #         return "hi"
    #     else:
    #         return False

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(DisLike)