from django.urls import path
from . import views as core_views


urlpatterns = [
	path('products/', core_views.ProductList.as_view(), name='product_list'),
	path('products/<int:pk>/', core_views.ProductDetail.as_view(), name='product_detail'),
	path('products/add/', core_views.ProductCreate.as_view(), name='product_add'),
	path('products/<int:pk>/edit/', core_views.ProductUpdate.as_view(), name='product_update'),
	path('products/<int:pk>/delete/', core_views.ProductDelete.as_view(), name='product_delete'),
]
