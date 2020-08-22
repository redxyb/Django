'''
@Author: xyb
@Date: 2020-07-24 21:57:19
@LastEditTime: 2020-07-25 17:35:59
'''
from datetime import date

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import re, time, socket
from book.models import BookInfo, UserBooks, User, BookComment

from django.views.decorators.csrf import csrf_exempt
# @csrf_protect：为当前函数强制设置防跨站请求伪造功能，即便settings中没有设置全局中间件
# @csrf_exempt：取消当前函数防跨站请求伪造功能，即便settings中设置了全局中间件

# Create your views here.

def home_page(request):
    '''主页'''
    username = request.COOKIES.get('username')
    title = 'homepage'
    books = BookInfo.objects.all()
    if username != None:
        user = User.objects.get(username=username)
        book = UserBooks.objects.filter(username_id=user.id)
        count = len(book)
        return render(request, 'book/booklist.html', {'books': books, 'user': user, 'count': count})
    if username == None:
        content = {'books': books, 'title': title}
        return render(request, 'home_page.html', content)


def login_page(request):
    '''登录'''
    if request.method == 'GET':
        return render(request, 'people/login.html', {'error': ''})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '' or password == '':
            return render(request, 'people/login.html', {'error': '请填写用户名和密码'})
        if username != '' and password != '':
            Acountinfo = User.objects.filter(username=username)
            for user in Acountinfo:
                if user.password == password:
                    # User.is_login = True
                    # User.login_name = user.username
                    #设置cookie
                    response = HttpResponseRedirect("/booklist.html/")
                    response.set_cookie('username', username, 900)
                    return response
                if user.password != password:
                    return render(request, 'people/login.html', {'error': '密码错误'})
            if not Acountinfo:
                return render(request, 'people/login.html', {'error': '此用户不存在'})

def register(request):
    '''注册'''
    if request.method == 'GET':
        return render(request, 'people/register.html', {'error': ''})
    if request.method == 'POST':
        username = request.POST.get('username')
        gender = request.POST.get('sex')
        #print(gender) # for test
        password = request.POST.get('password')
        email = request.POST.get('email')
        phonenum = request.POST.get('phonenum')
        if username == '' or password == '' or email == '' or gender == '':
            return render(request, 'people/register.html', {'error': '请将信息填写完整'})
        if username != '' and password != '' and email != '' and gender != '':
            #记得查重：已经存在的用户不能再注册
            users = User.objects.filter(username=username)
            if len(users) != 0:
                return render(request, 'people/register.html', {'error': '该用户已经存在'})
            if len(users) == 0:
                # 验证邮箱的合法性
                ret = re.match('\w{4,20}@(qq|163|126|gmail|outlook)\.com$', email)
                if ret:
                    # 将用户数据存入数据库
                    User.objects.create(
                        username=username,
                        gender=gender,
                        password=password,
                        email=email,
                        phonenum=phonenum, )
                    # User.is_login = True
                    # User.login_name = username
                    response = HttpResponseRedirect("/booklist.html/")
                    response.set_cookie('username', username, 3600)
                    return response
                if not ret:
                    return render(request, 'people/register.html', {'error': '邮箱不合法'})

def find_password(request):
    '''找回密码'''
    if request.method == 'GET':
        return render(request, 'people/find_password.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        if username == '' or email == '':
            return render(request, 'people/find_password.html', {'error': '请把信息填写完整'})
        if username != '' and email != '':
            Acountinfo = User.objects.filter(username=username)
            for user in Acountinfo:
                password = {'password': user.password}
                if user.username == username and user.email == email:
                    return render(request, 'people/find_password.html', password)
                if user.username != username or user.email != email:
                    return render(request, 'people/find_password.html', {'error': '邮箱与用户名不匹配'})

def change_password(request):
    '''更改密码'''
    if request.method == 'GET':
        return render(request, 'people/change_password.html')
    if request.method == 'POST':
        username = request.COOKIES.get('username')
        if username != None:
            user = User.objects.get(username=username)
            # print(user) #for test
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            if old_password != None and new_password != None:
                if old_password != new_password:
                    # name = User.login_name
                    # user = User.objects.get(username=name)
                    if old_password == user.password:
                        user.password = new_password
                        user.save()
                        response = HttpResponseRedirect('/change_password.html/')
                        response.delete_cookie('username')
                        return response
                    else:
                        return render(request, 'people/change_password.html', {'error': '你输入的当前密码错误'})
                if old_password == new_password:
                    return render(request, 'people/change_password.html', {'error': '新密码不能与旧密码一致'})
            else:
                return render(request, 'people/change_password.html', {'error': '新旧密码不能为空'})
        if username == None:
            return redirect('login_page')

def booklist(request):
    name = request.COOKIES.get('username')
    #print(name)#for test
    if name != None:
        user = User.objects.get(username=name)
        #print(name) #for test
        #查询数据库书籍列表数据
        books = BookInfo.objects.all()
        personal_book = UserBooks.objects.filter(username_id=user.id)
        count = len(personal_book)
        #构造上下文
        content = {'books': books, 'user': user, 'count': count}
        #数据交给模板处理，处理完后通过视图响应给客户端
        return render(request, 'book/booklist.html', content)
    if name == None:
        # return HttpResponse('you have not login!!!')
        return redirect('login_page')

def detail(request, bid):
    '''展示书籍详细信息'''
    username = request.COOKIES.get('username')
    if username != None:
        books = BookInfo.objects.get(id=int(bid))
        #print(username) #for test
        i = User.objects.get(username=username).id
        if request.method == 'POST':
            content = request.POST.get('content')
            # username_id = request.user.id
            # print(username_id)
            comment_time = time.ctime()
            ip_addr = socket.gethostbyname(socket.gethostname())
            comment = BookComment(
                content=content,
                username_id=i,
                book_name_id=int(bid),
                comment_time=comment_time,
                ip_addr=ip_addr
            )
            comment.save()
            comments = BookComment.objects.filter(book_name_id=int(bid))
            count = len(comments)
            return render(request, 'book/book_detail.html', {'book': books, 'count': count, 'comments': comments})
        #查找所有关于本书的评论
        comments = BookComment.objects.filter(book_name_id=int(bid))
        count = len(comments)
        return render(request, 'book/book_detail.html', {'book': books, 'count': count, 'comments': comments})
    if username == None:
        return redirect('login_page')

def add(request, id):
    '''添加书本到个人书库'''
    username = request.COOKIES.get('username')
    if username != None:
        user = User.objects.get(username=username)
        userbook = UserBooks(
            username_id=user.id,
            book_name_id=id,
        )
        userbook.save()
        book = BookInfo.objects.all()
        return redirect('booklist_page')
    if username == None:
        return redirect('login_page')

def delete_books(request, id):
    '''彻底删除书籍:还需要删除对应的评论'''
    BookInfo.delete_book(id)
    books = BookInfo.objects.all()
    # 构造上下文
    content = {'title': '图书列表', 'books': books}
    # 数据交给模板处理，处理完后通过视图响应给客户端
    return render(request, 'book/booklist.html', content)

def delete_personal_books(request, id):
    '''删除个人书库中的书籍'''
    UserBooks.delete_book(id)
    return redirect('personal_books_page')

def create_books(request):
    '''添加书籍'''
    if request.method == 'GET':
        return render(request, 'book/add_book.html', {'error': ''})
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        book_pub_date = request.POST.get('book_pub_date')
        book_readcount = request.POST.get('book_readcount')
        book_commentcount = request.POST.get('book_commentcount')
        # print(book_name, book_pub_date, book_commentcount, book_readcount) #for test
        books = BookInfo.objects.filter(name=book_name)
        if len(books) == 0:
            if book_name == '' or book_readcount == '' or book_commentcount == '':
                return render(request, 'book/add_book.html', {'error': '请将书籍信息填写完整！'})
            if book_name != '' and book_readcount != '' and book_commentcount != '':
                BookInfo.create_book(name=book_name, pub_date=book_pub_date, readcount=book_readcount, commentcount=book_commentcount)
                return render(request, 'book/add_book.html', {'error': '书本添加完成'})
        if len(books) != 0:
            return render(request, 'book/add_book.html', {'error': '该书本已经存在'})

def personal_information_page(request):
    username = request.COOKIES.get('username')
    # print(username) #for test
    user = User.objects.get(username=username)
    # gender = user.gender
    email = user.email
    phonenum = user.phonenum
    # print(email, phonenum) #for test
    if request.method == 'POST':
        username1 = request.POST.get('username')
        gender1 = request.POST.get('sex')
        email1 = request.POST.get('email')
        # print(email1) #for test
        phonenum1 = request.POST.get('phonenum')
        if username1 == '':
            user.username = username
        else:
            user.username = username1
        if email1 == '':
            user.email = email
        else:
            user.email = email1
        if phonenum1 == '':
            user.phonenum = phonenum
        else:
            user.phonenum = phonenum1
        user.gender = gender1
        user.save()
        user = User.objects.get(username=username)
        return render(request, 'people/personal_information.html', {'user': user})
    return render(request, 'people/personal_information.html', {'user': user})

def personal_books(request):
    username = request.COOKIES.get('username')
    if username != None:
        user = User.objects.get(username=username)
        books = UserBooks.objects.filter(username_id=user.id)
        return render(request, 'book/personal_books.html', {'books': books})
    if username == None:
        return redirect('login_page')

def login_out(request):
    User.login_name = ''
    response = HttpResponseRedirect('/')
    response.delete_cookie('username')
    #这里要清楚cookies
    return response

def book_type0(request):
    '''编程类'''
    books = BookInfo.objects.filter(book_type=0)
    username = request.COOKIES.get('username')
    if username != None:
        user = User.objects.get(username=username)
        book = UserBooks.objects.filter(username_id=user.id)
        count = len(book)
        return render(request, 'book/booklist0.html', {'user': user, 'books': books, 'count': count})
    if username == None:
        return render(request, 'home_page0.html', {'books': books})

def book_type1(request):
    '''其他类'''
    books = BookInfo.objects.filter(book_type=1)
    username = request.COOKIES.get('username')
    if username != None:
        user = User.objects.get(username=username)
        book = UserBooks.objects.filter(username_id=user.id)
        count = len(book)
        return render(request, 'book/booklist1.html', {'user': user, 'books': books, 'count': count})
    if username == None:
        return render(request, 'home_page1.html', {'books': books})

def search(request):
    '''先写简单的书名（模糊）搜索'''
    if request.method == 'GET':
        requirement = request.GET.get('requirement')
        # print(requirement)#for test
        books = BookInfo.objects.filter(book_name__contains=requirement)
        username = request.COOKIES.get('username')
        if username == None:
            return render(request, 'home_page.html', {'books': books})
        if username != None:
            user = User.objects.get(username=username)
            count = len(UserBooks.objects.filter(username_id=user.id))
            return render(request, 'book/booklist.html', {'books': books, 'user': user, 'count': count})

def kobe(request):
    return render(request, 'kobe.html')