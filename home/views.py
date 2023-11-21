from django.views.generic import ListView, DetailView

from django.shortcuts import render, get_object_or_404
from django.views import View

from myblog.models import Post
from shop.models import Product


class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(is_active=True)
        latest_posts = Post.objects.order_by('-created_date')[:5]
        return render(request, 'home/index.html', {'products': products , 'posts':latest_posts})


def offline(request):
    return render(request, 'home/offline.html')
