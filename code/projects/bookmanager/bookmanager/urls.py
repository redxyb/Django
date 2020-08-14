'''
@Author: xyb
@Date: 2020-07-24 21:53:51
@LastEditTime: 2020-07-25 11:43:48
'''
"""bookmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from book import views, urls
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    #正则为：只要不是 admin/ 就算匹配成功
    path('', views.home_page, name='home_page'),
    path('login.html/', views.login_page, name='login_page'),
    path('booklist.html/', views.booklist, name='booklist_page'),
    path('register.html/', views.register, name='register_page'),
    path('find_password.html/', views.find_password, name='findpassword_page'),
    path('change_password.html', views.change_password, name='changepassword_page'),
    url('detail(\d+)/', views.detail),#好像url才能使用正则匹配
    re_path(r'booklist.html/', include('book.urls')),
    # re_path(r'find_password.html/', include('book.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#
