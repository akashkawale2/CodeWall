from django.contrib import admin
from .models import post, BlogComment

# Register your models here.

admin.site.register((BlogComment))

@admin.register(post)

class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyinject.js',) 
        
    