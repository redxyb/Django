'''
@Author: xyb
@Date: 2020-07-24 21:57:19
@LastEditTime: 2020-07-25 16:26:40
'''
from django.contrib import admin
from book.models import BookInfo, UserBooks, User, BookComment

# Register your models here.
#注册模型
admin.site.register(BookInfo)
admin.site.register(User)
admin.site.register(UserBooks)
admin.site.register(BookComment)

class BookInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_image', 'book_url', 'description', 'book_type', 'book_name', 'book_author', 'book_pub', 'book_pubdate', 'book_adddate', 'book_likes', 'commentcount']

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'head_image', 'email', 'phonenum', 'gender', 'grade', 'user_addtime', 'is_admin']

class UserBooksAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'book_name', 'add_time']

class BookCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'book_name', 'content', 'comment_time']