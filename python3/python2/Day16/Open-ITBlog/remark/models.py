from django.db import models
from django.utils import timezone
# Create your models here.

class Remark(models.Model):
    name = models.CharField(max_length=20, verbose_name='评论人', null=False)
    text = models.TextField(verbose_name='评论内容', null=False, blank=True, default="")
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间', null=False, blank=False)
    aid = models.IntegerField(default=0)

    class Meta:
        verbose_name = '评论内容'
        ordering = ['-create_time']
        db_table = "remark"

class ArticleReply(models.Model):
    name = models.CharField(max_length=20,verbose_name='回复人姓名',null=False)
    text = models.TextField(verbose_name='回复内容',null=False,blank=True,default="")
    create_time = models.DateTimeField(default=timezone.now,verbose_name='创建时间',null=False,blank=False)
    modelsid = models.IntegerField(default=0)
    class Meta:
        verbose_name = '回复内容'
        ordering = ['-create_time']
        db_table = "articlereply"
