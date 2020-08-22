'''
@Author: xyb
@Date: 2020-07-25 11:39:50
@LastEditTime: 2020-07-25 17:08:51
'''
from django.conf.urls import url
from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('kobe.html/', views.kobe, name='kobe_page'),
    url('delete_book(\d+)', views.delete_books),
    url('delete_personal_books(\d+)', views.delete_personal_books),
    url('add_book.html/', views.create_books, name='create_books')
    # path('detail.html/', views.detail, name='detail_page')
    # path('login.html/', views.login_page, name='login_page'),
]
