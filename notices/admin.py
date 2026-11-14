from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', )
    list_filter = ('created_at', )
    
