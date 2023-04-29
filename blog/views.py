from django.shortcuts import render
from .models import *

# Create your views here.

def index(request):
    return render(request, "index.html")

def blog(request):
    blogs=Blog.objects.all()
    context={'blogs':blogs}
    return render(request, "blog.html", context)

# slug is the url part whether is a string or int after some urlpaths such as xyz123 in www.google.com/home/xyz123
def blogpost(request, slug):
    blog= Blog.objects.filter(slug=slug).first()
    context={'blog':blog}
    return render(request, "blogpost.html", context)

def contact(request):
    return render(request, "contact.html")

def search(request):
    return render(request, "search.html")