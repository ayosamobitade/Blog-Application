from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Post
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    tempelate_name = 'blog/post/list.html'



def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, 
    slug = post,
    status = "published",
    publish_year = year,
    published_month = month,
    publish_day = day)

    return render(request, "blog/post/detail.html",
    {"post":post}
    )