from msilib.schema import ListView
from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.


def HomePageView(request):
    return render(request, "pages/index.html")
