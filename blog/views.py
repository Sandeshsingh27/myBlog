from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from urllib.parse import urlencode

# Create your views here.

def index(request):
    context={'success':False}
    if request.method=='POST':
        title=request.POST['title']
        content=request.POST['content']
        slug=request.POST.get('slug')
        try:
            data=Blog(title=title, content=content, slug=slug)
            data.save()
            context={'success':True}
            print('Blog saved')
        except:
            return 'There was an issue adding your task'
    return render(request, "index.html", context)

def blog(request):
    blogs=Blog.objects.all()
    # getting variable passed from delete function to render some alert on blog.html through redirect method
    delete = True if request.GET.get('delete') else False
    edit = True if request.GET.get('edit') else False

    context={'blogs':blogs, 'delete':delete, 'edit':edit}
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

def edit(request, sno):
    blog=Blog.objects.get(sno=sno)
    context={'blog':blog}

    return render(request, 'edit.html', context)


def update(request, sno):
    context={}
    if request.method=='POST':
        title=request.POST['title']
        content=request.POST['content']
        slug=request.POST.get('slug')
        blog = Blog.objects.get(sno=sno)
        blog.title=title
        blog.content=content
        blog.slug=slug
        
        blog.save()
        print('Blog updated')

        # here we are passing value through url to the redirecting page
        base_url = reverse('blog')  # 1 /blog/
        context={'edit':True}
        query_string =  urlencode(context)  # 2 'edit' = True
        url = '{}?{}'.format(base_url, query_string)  # 3 /products/?edit=True
        return redirect(url)

    blogs=Blog.objects.all()
    context.update({'blogs':blogs})
    return render(request, 'blog.html', context)

def delete(request, sno):
    item = Blog.objects.get(sno=sno)
    context={}

    if item:
        item.delete()

        print('Blog updated')

        # here we are passing value through url to the redirecting page
        base_url = reverse('blog')  # 1 /blog/
        context={'delete':True}
        query_string =  urlencode(context)  # 2 'delete' = True
        url = '{}?{}'.format(base_url, query_string)  # 3 /products/?delete=True
        return redirect(url)  # 4

    context.update({'item':item})
    return render(request, 'blog.html', context)

