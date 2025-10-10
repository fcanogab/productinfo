from django.urls import path
from . import views as core_views


urlpatterns = [
    path('', core_views.ProductList.as_view(), name='home'),
    path('products/', core_views.ProductList.as_view(), name='product_list'),
    path('products/<int:pk>/', core_views.ProductDetail.as_view(), name='product_detail'),
    path('products/add/', core_views.ProductCreate.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', core_views.ProductUpdate.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', core_views.ProductDelete.as_view(), name='product_delete'),
    path('components/<int:pk>/', core_views.ComponentDetail.as_view(), name='component_detail'),
    path('components/add/', core_views.ComponentCreate.as_view(), name='component_add'),
    path('components/<int:pk>/edit/', core_views.ComponentUpdate.as_view(), name='component_update'),
    path('components/<int:pk>/delete/', core_views.ComponentDelete.as_view(), name='component_delete'),
    path('features/', core_views.FeatureList.as_view(), name='feature_list'),
    path('features/<int:pk>/', core_views.FeatureDetail.as_view(), name='feature_detail'),
    path('features/add/', core_views.FeatureCreate.as_view(), name='feature_add'),
    path('features/<int:pk>/edit/', core_views.FeatureUpdate.as_view(), name='feature_update'),
    path('features/<int:pk>/delete/', core_views.FeatureDelete.as_view(), name='feature_delete'),
    path('threats/', core_views.ThreatList.as_view(), name='threat_list'),
    path('threats/<int:pk>/', core_views.ThreatDetail.as_view(), name='threat_detail'),
    path('threats/add/', core_views.ThreatCreate.as_view(), name='threat_add'),
    path('threats/<int:pk>/edit/', core_views.ThreatUpdate.as_view(), name='threat_update'),
    path('threats/<int:pk>/delete/', core_views.ThreatDelete.as_view(), name='threat_delete'),
]
