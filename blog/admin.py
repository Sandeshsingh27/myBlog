from django.contrib import admin
from .models import *

# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    class Media:
        css= {
            "all": ("css/admin.css",)
        }

        js= ("js/admin.js",)


admin.site.register(Blog, BlogAdmin)