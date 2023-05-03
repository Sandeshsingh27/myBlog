from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from urllib.parse import urlencode
import math

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
    # PAGINATION LOGIC STARTS
    # designing pagination logic
    no_of_posts=3
    page= request.GET.get('page') # fetching value from url

    # By default, request.GET.get('page') returns string and if there is no page then return None
    # so if there is no page, make page = 1 otherwise convert ot integer
    if page is None:
        page = 1
    else:
        page = int(page)

    # fetching all blogs from database
    blogs=Blog.objects.all()
    # counting all blogs in the databases to perform pagination logic
    length = len(blogs)
    # here we are using python slicing function
    # below line just used to show how many blogs can be rendered on blog page and from where to where (ie, if page = 1, then blogs from index 0 to 2 will be displayed)
    blogs = blogs[(page-1)*no_of_posts: page*no_of_posts]

    # if page is greater than 1 then prev will be decremented by page-1 else make it None
    if page > 1:
        prev=page-1
    else:
        prev=None

    # Similarly, if page is less than ceiling value of required number of pages then nxt will be incremented by page+1 else make it None
    if page<math.ceil(length/no_of_posts):
        nxt=page+1
    else:
        nxt=None
    
    # PAGINATION LOGIC ENDS

    # getting variable passed from delete function to render some alert on blog.html through redirect method
    delete = True if request.GET.get('delete') else False
    edit = True if request.GET.get('edit') else False

    context={'blogs':blogs, 'delete':delete, 'edit':edit, 'prev':prev, 'nxt':nxt}
    return render(request, "blog.html", context)

# slug is the url part whether is a string or int after some urlpaths such as xyz123 in www.google.com/home/xyz123
def blogpost(request, slug):
    blog= Blog.objects.filter(slug=slug).first()
    context={'blog':blog}
    return render(request, "blogpost.html", context)

def contact(request):
    if request.method=='POST':
        name= request.POST.get('name')
        email= request.POST.get('email')
        phone= request.POST.get('phone')
        desc= request.POST.get('desc')

        instance = Contact(name=name, email=email, phone=phone, desc=desc)
        instance.save()
        print("Contact details are saved")
    return render(request, "contact.html")

def search(request):
    query=request.GET.get('query')
    # PAGINATION LOGIC STARTS
    # designing pagination logic
    no_of_posts=3
    page= request.GET.get('page') # fetching value from url

    # By default, request.GET.get('page') returns string and if there is no page then return None
    # so if there is no page, make page = 1 otherwise convert ot integer
    if page is None:
        page = 1
    else:
        page = int(page)

    # fetching all blogs from database
    searchBlogs= Blog.objects.filter(title__icontains=query)
    # counting all blogs in the databases to perform pagination logic
    length = len(searchBlogs)
    # here we are using python slicing function
    # below line just used to show how many blogs can be rendered on blog page and from where to where (ie, if page = 1, then blogs from index 0 to 2 will be displayed)
    searchBlogs = searchBlogs[(page-1)*no_of_posts: page*no_of_posts]

    # if page is greater than 1 then prev will be decremented by page-1 else make it None
    if page > 1:
        prev=page-1
    else:
        prev=None

    # Similarly, if page is less than ceiling value of required number of pages then nxt will be incremented by page+1 else make it None
    if page<math.ceil(length/no_of_posts):
        nxt=page+1
    else:
        nxt=None
    
    # PAGINATION LOGIC ENDS
    
    
    context={'searchBlogs':searchBlogs, 'prev':prev, 'nxt':nxt,'query':query}
    return render(request, "search.html", context)

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

