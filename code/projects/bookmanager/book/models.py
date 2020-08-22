'''
@Author: xyb
@Date: 2020-07-24 21:57:19
@LastEditTime: 2020-07-25 11:24:38
'''
from django.db import models

# Create your models here.
#准备书籍信息表的模块类型
class BookInfo(models.Model):
    TYPE_CHOICES = (
        (0, '编程类'),
        (1, '其他类'),
    )
    #创建字段、字段类型
    book_image = models.ImageField(upload_to='book_images', default='book.jpg', verbose_name='书籍封面')
    book_name = models.CharField(max_length=20, verbose_name='书籍名称')
    book_url = models.CharField(max_length=50, verbose_name='书籍链接')
    description = models.TextField(verbose_name='书籍描述')
    book_author = models.CharField(null=True, max_length=50, verbose_name='书籍作者')
    book_type = models.SmallIntegerField(choices=TYPE_CHOICES, default=0, verbose_name='书籍类型')
    book_pub = models.CharField(verbose_name='书籍出版社', max_length=30, null=True)
    book_pubdate = models.DateField(verbose_name='书籍出版日期', null=True)
    book_adddate = models.DateField(verbose_name='书籍添加日期', auto_now_add=True)
    book_likes = models.IntegerField(default=0, verbose_name='书籍点赞量')
    commentcount = models.IntegerField(default=0, verbose_name='书籍评论量')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'bookinfo'  #指明数据库表名
        verbose_name = '书籍信息' #在admin站点中显示的名称
        ordering = ['-book_adddate']

    def __str__(self):
        '''定义每个数据对象的显示信息'''
        return self.book_name

    #重写all()方法
    def all(self):
        #默认查询未删除的图书信息
        return super().all().filter(isDelete=False)

    @staticmethod
    #创建模型方法，接收参数为属性赋值
    def create_book(name, pub_date, readcount, commentcount):
        book = BookInfo.objects.create(
            name=name,
            pub_date=pub_date,
            readcount=readcount,
            commentcount=commentcount,
            is_delete=False
        )
        #将数据插入数据表
        book.save()
        return book

    @staticmethod
    #删除模型，接收参数为要删除的id
    def delete_book(id):
        #删除与书籍对应的评论
        comment = BookComment.objects.get(book_name_id=int(id))
        comment.delete()
        book = BookInfo.objects.get(id=id)
        book.delete()



#准备用户表信息的模块
class User(models.Model):
    GENDER_CHOICES = (
        (1, 'male'),#男
        (0, 'female')#女
    )
    GRADE_CHOICES = (
        (0, 'VIP'),
        (1, 'SVIP'),
        (2, 'SSVIP')
    )
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=20, verbose_name='用户密码')
    head_image = models.ImageField(upload_to='user_images', default='head_image.jpg')
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='用户性别')
    email = models.CharField(max_length=30, verbose_name='用户邮箱')
    phonenum = models.CharField(max_length=15, null=True, verbose_name='用户电话')
    grade = models.SmallIntegerField(choices=GRADE_CHOICES, default=0, verbose_name='用户等级')
    user_addtime = models.DateField(auto_now_add=True, verbose_name='用户创建时间')
    is_admin = models.BooleanField(default=False, verbose_name='是否为管理员')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'userinfo'
        verbose_name = '用户信息'
        ordering = ['-user_addtime']

    def __str__(self):
        return self.username

    is_login = False
    login_name = ''

#准备用户书籍表信息的模块
class UserBooks(models.Model):
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户名')
    book_name = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='书籍名称')#外键
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'userbookinfo'
        verbose_name = '人物信息'
        ordering = ['-add_time']

    def __str__(self):
        return self.book_name

    def delete_book(id):
        #删除与书籍对应的评论
        book = UserBooks.objects.get(id=id)
        book.delete()

#准备书籍评论表信息的模块
class BookComment(models.Model):
    book_name = models.ForeignKey(BookInfo, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    ip_addr = models.GenericIPAddressField(verbose_name='评论者的IP')

    class Meta:
        db_table = 'commentinfo'
        verbose_name = '评论信息'
        ordering = ['-comment_time']

    def __str__(self):
        return self.content

    def __iter__(self):
        return [self.book_name, self.ip_addr, self.comment_time, self.username, self.content]