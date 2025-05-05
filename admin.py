from django.contrib import admin
from .models import Post, Author

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_summary', 'author', 'updated_at', 'created_at')
    list_filter = ('title',)
    search_fields = ('title', 'content')

    # Custom method to show a brief part of content
    def content_summary(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content

    content_summary.short_description = 'Content'

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
