'''
@Author: xyb
@Date: 2020-07-24 21:57:19
@LastEditTime: 2020-07-25 16:26:40
'''
import xadmin
from django.contrib import admin
from book.models import BookInfo, UserBooks, User, BookComment

# Register your models here.
#注册模型
xadmin.site.register(BookInfo)
xadmin.site.register(User)
xadmin.site.register(UserBooks)
xadmin.site.register(BookComment)

class BookInfoAdmin(object):
    list_display = ['id', 'book_image', 'book_url', 'description', 'book_type', 'book_name', 'book_author', 'book_pub', 'book_pubdate', 'book_adddate', 'book_likes', 'commentcount']

class UserAdmin(object):
    list_display = ['id', 'username', 'password', 'head_image', 'email', 'phonenum', 'gender', 'grade', 'user_addtime', 'is_admin']

class UserBooksAdmin(object):
    list_display = ['id', 'username', 'book_name', 'add_time']

class BookCommentAdmin(object):
    list_display = ['id', 'username', 'book_name', 'content', 'comment_time']