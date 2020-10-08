from django.conf.urls import url
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('kobe.html/', views.kobe, name='kobe_page'),
    path('', views.home_page, name='home_page'),
    path('login.html/', views.login_page, name='login_page'),
    path('booklist.html/', views.booklist, name='booklist_page'),
    path('register.html/', views.register, name='register_page'),
    path('find_password.html/', views.find_password, name='findpassword_page'),
    path('change_password.html/', views.change_password, name='changepassword_page'),
    path('personal_information.html/', views.personal_information_page, name='personal_information_page'),
    path('personal_books.html/', views.personal_books, name='personal_books_page'),
    path('book_type0', views.book_type0, name='book_type0'),
    path('book_type1', views.book_type1, name='book_type1'),
    path('add_book.html', views.create_books, name='add_book_page'),
    re_path('login_out/', views.login_out, name='login_out'),
    re_path('log_off/', views.log_off, name='log_off'),
    re_path(r'detail(\d+)/', views.detail),#好像url(re_path)才能使用正则匹配,url在后面会淘汰
    re_path(r'add(\d+)/', views.add),
    re_path(r'delete_book(\d+)', views.delete_books),
    re_path(r'delete_comment(\d+)/', views.delete_comment),
    re_path(r'search/', views.search, name='search'),
]
