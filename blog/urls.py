from django.urls import path
from blog import views

urlpatterns = [
    path('', views.index, name="index"),
    path('blog/', views.blog, name="blog"),
    path('blogpost/<str:slug>', views.blogpost, name="blogpost"),
    path('contact/', views.contact, name="contact"),
    path('search/', views.search, name="search"),
    path('delete/<int:sno>/', views.delete, name='delete'),
    path('edit/<int:sno>/', views.edit, name='edit'),
    path('blog/<int:sno>/', views.update, name='update'),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),

]