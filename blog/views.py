from django.shortcuts import render, redirect
from .models import *

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
    # getting session variable passed from delete function to render some alert on blog.html
    delete = request.session.get('delete') # get the value from session
    context={'blogs':blogs, 'delete':delete}
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
        context={'edit':True, 'delete':False}
        print('Blog updated')
        # return redirect('/tasks')

    blogs=Blog.objects.all()
    context.update({'blogs':blogs})
    return render(request, 'blog.html', context)

def delete(request, sno):
    item = Blog.objects.get(sno=sno)
    context={}

    if item:
        item.delete()

        # context={'edit':False, 'delete':True}
        print('Blog updated')
        # creating session variable to store value, so that alert can be displayed on Blog.html
        # So, if you want to pass some value through redirect method can be passed using session creation
        # and second way of doing it is to pass value in url and get it from there
        # refer this problem-> https://stackoverflow.com/questions/32274852/django-dictionary-passed-in-redirect-is-not-showing-in-template
        request.session['delete'] = True # set in session
        return redirect('/blog')

    # context.update({'item':item})
    return render(request, 'blog.html', context)

