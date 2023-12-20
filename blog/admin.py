from django.contrib import admin
from .models import Blog, Category, Tag


# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published_date', 'status', 'counted_views')
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('title',)}

    @admin.display(description='something')
    def counted_views(self, blog):
        return blog.counted_views

admin.site.register(Category)
admin.site.register(Tag)