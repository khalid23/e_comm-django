from django.contrib import admin
from .models import Category, Color, Collection, Product, Image

class ProductInline(admin.TabularInline):
    model = Product.collections.through  # Use the intermediary model for the many-to-many relationship
    extra = 1

class CollectionAdmin(admin.ModelAdmin):
    inlines = [ProductInline]

admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Product)
admin.site.register(Image)
