from django.contrib import admin
from .models import Category, Tag, Blog, BlogImage

# ✅ Inline view for Blog Images
class ImageInline(admin.StackedInline):
    """Stacked Inline View for BlogImage"""
    model = BlogImage
    min_num = 1
    extra = 0  # অতিরিক্ত খালি ফিল্ড দেখাবে না

# ✅ Admin view for Blog
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'get_tags_display', 'created_date']
    list_filter = ['category', 'tags', 'created_date']
    search_fields = ['title', 'content', 'author__email']
    ordering = ['-created_date']

    inlines = [ImageInline]

    def get_tags_display(self, obj):
        return ', '.join(tag.title for tag in obj.tags.all())
    get_tags_display.short_description = 'Tags'

# ✅ Register other models
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']

@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ['blog', 'image']
