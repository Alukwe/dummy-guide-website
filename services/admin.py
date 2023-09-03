from django.contrib import admin
from .models import *


# Register your models here.

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')


admin.site.register(Services, ServiceAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Categories, CategoryAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('image',)


admin.site.register(ServiceImages, ImageAdmin)
