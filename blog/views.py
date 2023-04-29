from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html")

def blog(request):
    return render(request, "blog.html")

def blogpost(request, slug):
    # slug is the url part whether is a string or int after some urlpaths such as xyz123 in www.google.com/home/xyz123
    context={'slug':slug}
    return render(request, "blog.html", context)


def contact(request):
    return render(request, "contact.html")