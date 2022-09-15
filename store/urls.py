from django.urls import path
from .import views


urlpatterns = [

    path('',views.Store, name = 'home'),
    path('category/<slug:category_slug>/',views.Store, name ='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_details'),
    path('search/',views.search,name ='search'),

]