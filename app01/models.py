from django.db import models


# Create your models here.

class UserInfo(models.Model):
    uid = models.AutoField(verbose_name='用户ID', primary_key=True)
    mobile = models.CharField(verbose_name='账号', max_length=11)
    mbpwd = models.CharField(verbose_name='密码', max_length=12)

    def __str__(self):
        return self.mobile


class NewType(models.Model):
    typename = models.CharField(verbose_name='新闻类型', max_length=16)
    description = models.CharField(verbose_name='新闻描述', max_length=255)

    def __str__(self):
        return self.typename


class News(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标题', max_length=255)
    summary = models.CharField(verbose_name='简介', max_length=255)
    com_form = models.CharField(verbose_name='来自', max_length=255)
    head = models.CharField(verbose_name='头像', max_length=255)
    user = models.ForeignKey(verbose_name='作者', to='UserInfo', to_field='uid', related_name='author')
    newscategory = models.ForeignKey(verbose_name='新闻类型', to='NewType')
    like_count = models.IntegerField(verbose_name='点赞数', default=0)
    comment_count = models.IntegerField(verbose_name='评论数', default=0)
    like = models.ManyToManyField(verbose_name='点赞', to='UserInfo')
    ctime = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.CharField(verbose_name='评论内容', max_length=255)
    user = models.ForeignKey(verbose_name='评论作者', to='UserInfo')
    comment_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    news = models.ForeignKey(verbose_name='评论的新闻ID', to='News')

    def __str__(self):
        return self.content
