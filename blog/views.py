from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.urls import reverse
from urllib.parse import urlencode
import math
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

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

    # fetching all blogs from database according to the search query and
    # if length of query is greater than specified character than don't display the result
    if len(query) > 60:
        searchBlogs = Blog.objects.none()
    else:
        searchBlogsTitle= Blog.objects.filter(title__icontains=query)
        searchBlogsContent= Blog.objects.filter(content__icontains=query)
        searchBlogs=searchBlogsTitle.union(searchBlogsContent)
    # if query serach result is not found then using DJANGO FLASH MESSAGES feature
    if searchBlogs.count() == 0:
        messages.warning(request, "No Search Results Found! Please refine your query.")
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


# we cannot use login and logout keywords as these are reserved keywords of django
def signin(request):
    # if method is post then perform the action otherwise if it is get(ie, if user enter /login in the url then show error message)
    if request.method=='POST':
        loginusername= request.POST.get('loginusername')
        loginpass=request.POST.get('loginpass')

        user=authenticate(request, username=loginusername, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("index")
        else:
            messages.error(request, "Invalid Credentials! Please try again")
            return redirect("index")
    else:
        return HttpResponse("404 - NOT FOUND")

def signout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('index')


def signup(request):
    # if method is post then perform the action otherwise if it is get(ie, if user enter /signup in the url then show error message)
    if request.method=='POST':
        username= request.POST.get('username')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')

        # Check for errorneous inputs

        # username shoud be under 10 characters
        if (len(username) > 10):
            messages.error(request, "Your username must be under 10 characters")
            return redirect('/')

        # if User.objects.get(username=username):
        #     messages.error(request, "Your username has already been taken. Enter unique username!")
        #     return redirect('/')
        
        # username should be alpha-numeric only
        if not username.isalnum():
            messages.error(request, "Your username must only contains letter and numbers")
            return redirect('/')
        
        # pass1 soud match pass2
        if pass1 != pass2:
            messages.error(request, "Your passwords do not match")
            return redirect('/')
        
        # length of pass1 must be atleast 8 characters
        if (len(pass1) < 8):
            messages.error(request, "Your passwords must contains atleast 8 characters")
            return redirect('/')

        # Creating user
        my_user=User.objects.create_user(username, email, pass1)
        my_user.first_name=fname
        my_user.last_name=lname
        my_user.save()
        messages.success(request, "Your account has been successfully created")

        # we can also use name of urls to redirect
        return redirect('index')

    else:
        return HttpResponse("404 - NOT FOUND")