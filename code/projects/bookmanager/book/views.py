import os
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import re, time, socket

from django.urls import reverse

from book.models import BookInfo, UserBooks, User, BookComment

from django.views.decorators.csrf import csrf_exempt
# @csrf_protect：为当前函数强制设置防跨站请求伪造功能，即便settings中没有设置全局中间件
# @csrf_exempt：取消当前函数防跨站请求伪造功能，即便settings中设置了全局中间件

# Create your views here.
from bookmanager import settings


def home_page(request):
    '''主页'''
    username = request.COOKIES.get('username')
    title = 'homepage'
    books = BookInfo.objects.all()

    paginator = Paginator(books, 9)
    page = request.GET.get('page')
    ebooks = paginator.get_page(page)

    if username != None:
        return HttpResponseRedirect(reverse("book:booklist_page"))
    if username == None:
        content = {'ebooks': ebooks, 'title': title}
        return render(request, 'home_page.html', content)

def login_page(request):
    '''登录'''
    if request.method == 'GET':
        return render(request, 'user/login.html', {'error': ''})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '' or password == '':
            return render(request, 'user/login.html', {'error': '请填写用户名和密码'})
        if username != '' and password != '':
            Acountinfo = User.objects.filter(username=username)
            for user in Acountinfo:
                if user.password == password:
                    # User.is_login = True
                    # User.login_name = user.username
                    #设置cookie
                    response = HttpResponseRedirect(reverse("book:booklist_page"))
                    response.set_cookie('username', username, 900)
                    return response
                if user.password != password:
                    return render(request, 'user/login.html', {'error': '密码错误'})
            if not Acountinfo:
                return render(request, 'user/login.html', {'error': '此用户不存在'})

def register(request):
    '''注册'''
    if request.method == 'GET':
        return render(request, 'user/register.html', {'error': ''})
    if request.method == 'POST':
        username = request.POST.get('username')
        gender = request.POST.get('sex')
        #print(gender) # for test
        password = request.POST.get('password')
        email = request.POST.get('email')
        phonenum = request.POST.get('phonenum')
        if username == '' or password == '' or email == '' or gender == '':
            return render(request, 'user/register.html', {'error': '请将信息填写完整'})
        if username != '' and password != '' and email != '' and gender != '':
            #记得查重：已经存在的用户不能再注册
            users = User.objects.filter(username=username)
            if len(users) != 0:
                return render(request, 'user/register.html', {'error': '该用户已经存在'})
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
                    response = HttpResponseRedirect(reverse("book:booklist_page"))
                    response.set_cookie('username', username, 3600)
                    return response
                if not ret:
                    return render(request, 'user/register.html', {'error': '邮箱不合法'})

def log_off(request):
    '''普通用户注销账号'''
    username = request.COOKIES.get('username')
    if username != None:
        user = User.objects.filter(username=username)
        user.delete()
        response = HttpResponseRedirect('/')
        response.delete_cookie('username')
        return response
    if username == None:
        return redirect('book:login_page')

def find_password(request):
    '''找回密码'''
    if request.method == 'GET':
        return render(request, 'user/find_password.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        if username == '' or email == '':
            return render(request, 'user/find_password.html', {'error': '请把信息填写完整'})
        if username != '' and email != '':
            Acountinfo = User.objects.filter(username=username)
            for user in Acountinfo:
                password = {'password': user.password}
                if user.username == username and user.email == email:
                    return render(request, 'user/find_password.html', password)
                if user.username != username or user.email != email:
                    return render(request, 'user/find_password.html', {'error': '邮箱与用户名不匹配'})

def change_password(request):
    '''更改密码'''
    if request.method == 'GET':
        return render(request, 'user/change_password.html')
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
                        response = HttpResponseRedirect(reverse('book:login_page'))
                        response.delete_cookie('username')
                        return response
                    else:
                        return render(request, 'user/change_password.html', {'error': '你输入的当前密码错误'})
                if old_password == new_password:
                    return render(request, 'user/change_password.html', {'error': '新密码不能与旧密码一致'})
            else:
                return render(request, 'user/change_password.html', {'error': '新旧密码不能为空'})
        if username == None:
            return redirect('book:login_page')

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

        #引入分页模块：每页显示9本书
        paginator = Paginator(books, 9)
        #获取url中的页码
        page = request.GET.get('page')
        # 将导航对象相应的页码内容返回给 ebooks
        ebooks = paginator.get_page(page)

        #构造上下文
        content = {'user': user, 'count': count, 'ebooks': ebooks}
        #数据交给模板处理，处理完后通过视图响应给客户端
        return render(request, 'book/booklist.html', content)
    if name == None:
        return redirect('book:login_page')

def detail(request, bid):
    '''展示书籍详细信息'''
    username = request.COOKIES.get('username')
    if username != None:
        books = BookInfo.objects.get(id=int(bid))
        #print(username) #for test
        user = User.objects.get(username=username)
        # print(user)
        i = user.id
        if request.method == 'POST':
            content = request.POST.get('content')
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
            root_list, child_list = handle_comment(comments)
            return render(request, 'book/book_detail.html',
                          {'book': books, 'count': count, 'comments': root_list, 'child_comments': child_list,
                           'user': user})
        #查找所有关于本书的评论
        comments = BookComment.objects.filter(book_name_id=int(bid))
        count = len(comments)
        books.commentcount = count
        books.save()
        root_list, child_list = handle_comment(comments)
        return render(request, 'book/book_detail.html', {'book': books, 'count': count, 'comments': root_list, 'child_comments': child_list, 'user': user})
    if username == None:
        return redirect('book:login_page')

def handle_comment(comments):
    '''将同一本书的根评论与子评论分开'''
    root_list = []
    child_list = []
    for comment in comments:
        if comment.root_id == 0:
            root_list.append(comment)
        else:
            child_list.append(comment)
    return root_list, child_list

'''
删除评论：用户可以删除自己发表的评论，不能删除其他人的评论；
管理员可以删除所有人的评论；
如果根评论被删除，其下对应的子评论也对应删除
'''
def delete_comment(request, id):
    username = request.COOKIES.get('username')
    print(username)
    user = User.objects.get(username=username)
    if username != None:
        comment = BookComment.objects.get(id=id)
        print(comment)
        book_id = comment.book_name_id
        if comment.root_id == 0:
            comments = BookComment.objects.filter(parent_id=id)
            print(comments)
            comments.delete()
            return redirect('book:login_page')
        # BookComment.delete_c(id)
        comment.delete()
        return redirect('book:login_page')
    if username == None:
        return redirect('book:login_page')


def add(request, id):
    '''添加书本到个人书库：不能重复添加，已经添加的书籍不再添加'''
    username = request.COOKIES.get('username')
    if username != None:
        user = User.objects.get(username=username)
        userbooks = UserBooks.objects.filter(book_name_id=id)
        book = user.userbooks_set.filter(book_name_id=id)
        # print(len(book))
        if len(book) >= 1:
            return redirect('book:booklist_page')
        if len(book) < 1:
            userbook = UserBooks(
                username_id=user.id,
                book_name_id=id,
            )
            userbook.save()
            return redirect('book:booklist_page')
    if username == None:
        return redirect('book:login_page')


def delete_books(request, id):
    '''彻底删除书籍:还需要删除对应的评论'''
    BookInfo.delete_book(id)
    return redirect('book:booklist_page')

def delete_personal_books(request, id):
    '''删除个人书库中的书籍'''
    UserBooks.delete_book(id)
    return redirect('book:personal_books_page')

def create_books(request):
    '''添加书籍'''
    if request.method == 'GET':
        return render(request, 'book/add_book.html', {'error': ''})
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        book_pub_date = request.POST.get('book_pub_date')
        book_url = request.POST.get('book_url')
        book_author = request.POST.get('book_author')
        book_description = request.POST.get('book_description')
        book_pub = request.POST.get('book_pub')
        book_type = request.POST.get('book_type')
        print(book_name, book_author, book_pub, book_type, book_pub_date, book_url, book_description)

        #判断要添加的书籍是否存在，已存在就不添加
        books = BookInfo.objects.filter(book_name=book_name)
        if len(books) == 0:
            if book_name == '' or book_pub_date == '' or book_url == '' or book_author == '' or book_description == '' or book_pub == '' or book_type == '':
                return render(request, 'book/add_book.html', {'error': '请将书籍信息填写完整！'})
            if book_name != '' and book_pub_date != '' and book_url != '' and book_author != '' and book_description != '' and book_pub != '' and book_type != '':
                if 'b_icon' in request.FILES:
                    b_icon = request.FILES['b_icon']
                    #构建封面图片名称
                    image_name = book_name + '.jpg'
                    #构建封面图片所要上传的路径
                    img_path = os.path.join(settings.MEDIA_ROOT + '/book_images/', image_name)
                    #上传图片到指定位置
                    with open(img_path, 'wb') as f:
                        for i in b_icon.chunks():
                            f.write(i)
                    book_image = 'book_images' + '/' + image_name
                else:
                    book_image = 'book_images/book.jpg'
                # BookInfo.create_book(book_name=book_name, book_image=book_image, book_pubdate=book_pub_date, book_url=book_url, description=book_description, book_author=book_author, book_type=book_type, book_pub=book_pub)
                book = BookInfo(book_name=book_name, book_image=book_image, book_pubdate=book_pub_date, book_url=book_url, description=book_description, book_author=book_author, book_type=book_type, book_pub=book_pub)
                book.save()
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
    head_image = user.head_image
    # print(email, phonenum) #for test
    if request.method == 'POST':
        username1 = request.POST.get('username')
        gender1 = request.POST.get('sex')
        email1 = request.POST.get('email')
        # print(email1) #for test
        phonenum1 = request.POST.get('phonenum')

        if 'u_icon' in request.FILES:
            #获取文件数据
            icon = request.FILES['u_icon']
            # print(icon) #for test
            t = time.gmtime()
            #构建头像图片的名字
            file_name = username + '(' + str(t.tm_year) + str(t.tm_mon) + str(t.tm_mday) + ')' + '.jpg'

            #构建头像图片所要上传的路径
            image_path = os.path.join(settings.MEDIA_ROOT + '/user_images/', file_name)
            #打开拼接的文件路径
            with open(image_path, 'wb') as fp:#图片上传到指定文件夹
                #遍历图片的块数据（切块的传图片）
                for i in icon.chunks():
                    fp.write(i)
            user.head_image = file_name
        else:
            user.head_image = head_image
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
        return render(request, 'user/personal_information.html', {'user': user})
    return render(request, 'user/personal_information.html', {'user': user})

def personal_books(request):
    username = request.COOKIES.get('username')
    if username != None:
        user = User.objects.get(username=username)
        books = UserBooks.objects.filter(username_id=user.id)
        return render(request, 'book/personal_books.html', {'books': books})
    if username == None:
        return redirect('book:login_page')

def login_out(request):
    '''退出登录'''
    if request.method == 'GET':
        response = HttpResponseRedirect(reverse('book:login_page'))
        response.delete_cookie('username')
        #这里要清除cookies
        return response

def book_type0(request):
    '''编程类'''
    books = BookInfo.objects.filter(book_type=0)
    username = request.COOKIES.get('username')

    #引入分页模块：没一页显示9本书
    paginator = Paginator(books, 9)
    #获取url中的页码
    page = request.GET.get('page')
    #将导航对象相应的页码内容返回给ebooks
    ebooks = paginator.get_page(page)

    if username != None:
        user = User.objects.get(username=username)
        book = UserBooks.objects.filter(username_id=user.id)
        count = len(book)
        return render(request, 'book/booklist0.html', {'user': user, 'ebooks': ebooks, 'count': count})
    if username == None:
        return render(request, 'home_page0.html', {'ebooks': ebooks})

def book_type1(request):
    '''其他类'''
    books = BookInfo.objects.filter(book_type=1)
    username = request.COOKIES.get('username')

    #引入分页模块：没一页显示9本书
    paginator = Paginator(books, 9)
    #获取url中的页码
    page = request.GET.get('page')
    #将导航对象相应的页码内容返回给ebooks
    ebooks = paginator.get_page(page)

    if username != None:
        user = User.objects.get(username=username)
        book = UserBooks.objects.filter(username_id=user.id)
        count = len(book)
        return render(request, 'book/booklist1.html', {'user': user, 'ebooks': ebooks, 'count': count})
    if username == None:
        return render(request, 'home_page1.html', {'ebooks': ebooks})

def search(request):
    '''先写简单的书名（模糊）搜索'''
    if request.method == 'GET':
        requirement = request.GET.get('requirement')
        # print(requirement)#for test
        books = BookInfo.objects.filter(book_name__contains=requirement)
        paginator = Paginator(books, 9)
        page = request.GET.get('page')
        ebooks = paginator.get_page(page)
        username = request.COOKIES.get('username')
        if username == None:
            return render(request, 'home_page.html', {'ebooks': ebooks})
        if username != None:
            user = User.objects.get(username=username)
            count = len(UserBooks.objects.filter(username_id=user.id))
            return render(request, 'book/booklist.html', {'ebooks': ebooks, 'user': user, 'count': count})

def kobe(request):
    return render(request, 'kobe.html')