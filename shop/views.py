from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView
from django.views.generic import TemplateView

from .models import PriceChange, Product


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'shop/detail.html', {'product': product})


class PriceChangeChartView(TemplateView):
    template_name = 'shop/price_change_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        price_changes = PriceChange.objects.annotate(date=TruncDate('created_at')).values('date').annotate(
            total_price=Sum('new_price')).order_by('date')
        dates = [price_change['date'] for price_change in price_changes]
        prices = [float(price_change['total_price']) for price_change in price_changes]
        context['dates'] = dates
        context['prices'] = prices
        return context


