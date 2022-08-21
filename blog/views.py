from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from django.db.models import Count
from .forms import EmailPostForm, CommentForm, SearchForm

# Create your views here.
from .models import Post, Comment
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight = 'A') + SearchVector('body', weight = 'B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                search = search_vector, 
                rank = SearchRank(search_vector, search_query)
                ).filter(search = search_query).order_by('-rank')
    return render(request, 'blog/post/search.html',{
        'form':form,
        'query':query,
        'results':results
    })



class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    tempelate_name = 'blog/post/list.html'





def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
    status='published',
    publish__year=year,
    publish__month=month,
    publish__day=day)

    comments = post.comments.filter(active = True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()


    return render(request, 'blog/post/detail.html',{
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form})







def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com',
                [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})



