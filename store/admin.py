from django.contrib import admin
from .models import Product,Variational,ReviewRating
# from django.db import
# Register your models here.

class VariationalAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable =('is_active',)
    list_filter = ('product','variation_category','variation_value')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug': ('product_name',)}
admin.site.register(Product,ProductAdmin)
admin.site.register(Variational,VariationalAdmin)
admin.site.register(ReviewRating)