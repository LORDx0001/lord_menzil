from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Product, ProductImage, ProductCategory

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ('name', 'category', 'is_featured')
    list_filter = ('category', 'is_featured')
    list_editable = ('is_featured',)
    search_fields = ('translations__name', 'translations__description')
    inlines = [ProductImageInline]

@admin.register(ProductCategory)
class ProductCategoryAdmin(TranslatableAdmin):
    list_display = ('name',)
    search_fields = ('translations__name',)
