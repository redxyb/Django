'''
@Author: xyb
@Date: 2020-07-24 21:57:19
@LastEditTime: 2020-07-25 11:24:38
'''
from django.db import models

# Create your models here.
#准备书籍列表信息的模块类型
class BookInfo(models.Model):
    #创建字段、字段类型
    name = models.CharField(max_length=20, verbose_name='名称')
    pub_date = models.DateField(verbose_name='发布日期', null=True)
    readcount = models.IntegerField(default=0, verbose_name='阅读量')
    commentcount = models.IntegerField(default=0, verbose_name='评论量')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'bookinfo'  #指明数据库表名
        verbose_name = '图书' #在admin站点中显示的名称

    def __str__(self):
        '''定义每个数据对象的显示信息'''
        return self.name

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
        #调用语法：book = BookInfo.bookinfo.create_book("abc", date(1998-2-17), 13, 34)

    @staticmethod
    #删除模型，接收参数为要删除的id
    def delete_book(id):
        book = BookInfo.objects.get(id=id)
        book.delete()

#准备人物列表信息的模块
class PeopleInfo(models.Model):
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    name = models.CharField(max_length=20, verbose_name='名称')#书中人物姓名
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    description = models.CharField(max_length=200, null=True, verbose_name='描述信息')
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='图书')#外键
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'peopleinfo'
        verbose_name = '人物信息'

    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=20, verbose_name='密码')
    email = models.CharField(max_length=30, verbose_name='邮箱')
    phonenum = models.CharField(max_length=15, null=True, verbose_name='电话')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'userinfo'
        verbose_name = '用户信息'

    def __str__(self):
        return self.username

    is_login = False
    login_name = ''