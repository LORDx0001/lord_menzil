from parler.translator import translator, TranslationOptions
from .models import Product, ProductCategory

class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

class ProductCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Product, ProductTranslationOptions)
translator.register(ProductCategory, ProductCategoryTranslationOptions)
