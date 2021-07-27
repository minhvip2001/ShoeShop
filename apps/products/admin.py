from django.contrib import admin
from .models import Product, Category, ProductImage


class ProductAdmin(admin.ModelAdmin):
    pass
class CategoryAdmin(admin.ModelAdmin):
    pass
class ProductImageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage, ProductImageAdmin)