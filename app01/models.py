from django.db import models


# Create your models here.

# 用户表
class UserInfo(models.Model):
    uid = models.AutoField(verbose_name='用户ID', primary_key=True)
    mobile = models.CharField(verbose_name='账号', max_length=11)
    mbpwd = models.CharField(verbose_name='密码', max_length=12)

    def __str__(self):
        return self.mobile

# 新闻类型表
class NewType(models.Model):
    typename = models.CharField(verbose_name='新闻类型', max_length=16)
    description = models.CharField(verbose_name='新闻描述', max_length=255)

    def __str__(self):
        return self.typename

# 新闻表
class News(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标题', max_length=255)
    summary = models.CharField(verbose_name='简介', max_length=255)
    com_form = models.CharField(verbose_name='来自', max_length=255)
    head = models.CharField(verbose_name='头像', max_length=255,default=None,null=True)
    like_count = models.IntegerField(verbose_name='点赞数', default=0)
    comment_count = models.IntegerField(verbose_name='评论数', default=0)
    ctime = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)

    user = models.ForeignKey(verbose_name='作者', to='UserInfo', to_field='uid', related_name='author')
    newscategory = models.ForeignKey(verbose_name='新闻类型', to='NewType')
    like = models.ManyToManyField(verbose_name='点赞', to='UserInfo',through='Like',through_fields=('nid','uid'))

    def __str__(self):
        return self.title

# 评论表
class Comment(models.Model):
    content = models.CharField(verbose_name='评论内容', max_length=255)
    user = models.ForeignKey(verbose_name='评论作者', to='UserInfo')
    comment_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    news = models.ForeignKey(verbose_name='评论的新闻ID', to='News')

    def __str__(self):
        return self.content


#  新闻与用户点赞关系表
class Like(models.Model):
    lid = models.AutoField(primary_key=True)
    nid = models.ForeignKey('News',related_name='newsid')
    uid = models.ForeignKey('UserInfo')

    # 创建联合唯一索引
    class Meta:
        unique_together=(
            ('nid', 'uid'),
        )

    def __str__(self):
        return self.lid


