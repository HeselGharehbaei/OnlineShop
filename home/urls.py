from django.urls import path, include
from . import views


app_name='home'

Backet_urls= [
    path('', views.BucketHome.as_view(), name='bucket'),
    path('delete_obj/<key>', views.DeleteBucketObj.as_view(), name='delete_obj_bucket'),
]


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('bucket/', include(Backet_urls)),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
