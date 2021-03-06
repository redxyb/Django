# Generated by Django 2.1 on 2020-08-23 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcomment',
            name='parent_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bookcomment',
            name='root_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bookcomment',
            name='comment_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='bookinfo',
            name='book_author',
            field=models.CharField(max_length=50, null=True, verbose_name='书籍作者'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.SmallIntegerField(choices=[(1, 'male'), (0, 'female')], default=0, verbose_name='用户性别'),
        ),
        migrations.AlterField(
            model_name='userbooks',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='添加时间'),
        ),
    ]
