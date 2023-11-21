from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    queryset = Post.objects.filter().order_by('-created_date')
    template_name = 'myblog/post_list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'myblog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        # Get related posts based on similar content or title
        related_posts = Post.objects.filter(
            Q(content__icontains=post.content[:50]) |
            Q(title__icontains=post.title[:50])
        ).exclude(id=post.id)[:3]
        context['related_posts'] = related_posts
        return context
