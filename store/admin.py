from django.contrib import admin
from .models import Product,Variational,ReviewRating,ProductGallery
# from django.db import
# Register your models here.
import admin_thumbnails
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class VariationalAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable =('is_active',)
    list_filter = ('product','variation_category','variation_value')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]

admin.site.register(Product,ProductAdmin)
admin.site.register(Variational,VariationalAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
