'''
@Author: xyb
@Date: 2020-07-24 21:57:19
@LastEditTime: 2020-07-25 17:35:59
'''
from datetime import date

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import re
from django.template import loader, RequestContext

from book.models import BookInfo, UserBooks, User, BookComment

# Create your views here.

def home_page(request):
    '''主页'''
    title = 'homepage'
    books = BookInfo.objects.all()
    #print(books) #for test
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
                    User.is_login = True
                    User.login_name = user.username
                    return HttpResponseRedirect("/booklist.html/")
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
        password = request.POST.get('password')
        email = request.POST.get('email')
        phonenum = request.POST.get('phonenum')
        if username == '' or password == '' or email == '':
            return render(request, 'people/register.html', {'error': '请将信息填写完整'})
        if username != '' and password != '' and email != '':
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
                        password=password,
                        email=email,
                        phonenum=phonenum, )
                    User.is_login = True
                    User.login_name = username
                    return HttpResponseRedirect("/booklist.html/")
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
        return render(request, 'people/change_password.html', {'error': ''})
    if request.method == 'POST':
        user = request.user
        user.is_authenticated
        print(user) #for test
        if User.is_login == True:
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            if old_password != '' and new_password != '':
                if old_password != new_password:
                    name = User.login_name
                    user = User.objects.get(username=name)
                    if old_password == user.password:
                        user.password = new_password
                        user.save()
                        User.is_login = False
                        return render(request, 'people/change_password.html', {'error': '密码修改成功'})
                    else:
                        return render(request, 'people/change_password.html', {'error': '你输入的当前密码错误'})
                if old_password == new_password:
                    return render(request, 'people/change_password.html', {'error': '新密码不能与旧密码一致'})
            else:
                return render(request, 'people/change_password.html', {'error': '新旧密码不能为空'})
        if User.is_login == False:
            return redirect('login_page')

def booklist(request):
    if User.is_login == True:
        name = User.login_name
        #print(name) #for test
        #查询数据库书籍列表数据
        books = BookInfo.objects.all()
        #构造上下文
        content = {'title': 'Electronic books', 'books': books, 'name': name}
        #数据交给模板处理，处理完后通过视图响应给客户端
        return render(request, 'book/booklist.html', content)
    if User.is_login == False:
        # return HttpResponse('you have not login!!!')
        return redirect('/')

def detail(request, bid):
    '''展示书籍详细信息'''
    #查询所有图书
    books = BookInfo.objects.get(id=int(bid))
    #查找book图书中的所有人物
    return render(request, 'book/book_detail.html', {'book': books})

def delete_books(request, id):
    '''删除书籍'''
    BookInfo.delete_book(id)
    books = BookInfo.objects.all()
    # 构造上下文
    content = {'title': '图书列表', 'books': books}
    # 数据交给模板处理，处理完后通过视图响应给客户端
    return render(request, 'book/booklist.html', content)

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

def kobe(request):
    return render(request, 'kobe.html')