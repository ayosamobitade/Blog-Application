from .models import Post, Comment
from django import forms
from django.contrib.postgres.search import SearchVector
from .forms import EmailPostForm, CommentForm, SearchForm
from django.shortcuts import render


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length = 25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required = False, widget = forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class SearchForm(forms.Form):
    query = forms.CharField()

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                search = SearchVector('title', 'body'),
            ).filter(search = query)
    return render(request, 'blog/post/search.html', 
    {
        'form':form,
        'query':query,
        'results':results
    })