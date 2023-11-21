from django.urls import path

from shop import views
from shop.views import PriceChangeChartView

app_name = 'shop'
urlpatterns = [
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('price-chart/<slug:slug>/', PriceChangeChartView.as_view(), name='price_chart'),


]
