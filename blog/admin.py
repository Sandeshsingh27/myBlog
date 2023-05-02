from django.contrib import admin
from .models import *

# Register your models here.

# Below class is used to apply javascript and css on admin panel page
class BlogAdmin(admin.ModelAdmin):
    class Media:
        css= {
            "all": ("css/admin.css",)
        }

        js= ("js/admin.js",)


admin.site.register(Blog, BlogAdmin)

admin.site.register(Contact)