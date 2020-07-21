#!/usr/bin/env python
# -*- coding: utf-8 -*-  
'''
@author: xiaoshui
@contact: opsonly.com@gmail.com
@file: forms.py
@time: 2018/11/19 16:39
'''

from django import forms
from .models import ArticlePost
from django.db import models

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ('title','body','category')


TOPIC_CHOICES=(
    ('level1','Bad'),
    ('level2','Soso'),
    ('level3','Good'),
)

class RemarkForm(forms.Form):
    subject=forms.CharField(max_length=100,label='Mark Board')
    mail=forms.EmailField(label='email')
    topic=forms.ChoiceField(choices=TOPIC_CHOICES,label='choose one topic')
    message=forms.CharField(label='content for mark',widget=forms.Textarea)
    cc_myself=forms.BooleanField(required=False,label='watch this tie')

class Remark(models.Model):
    subject = models.CharField(max_length=100)
    mail = models.EmailField()
    topic = models.CharField(max_length=100)
    message = models.CharField(max_length=300)
    cc_myself = models.BooleanField()

    def __str__(self):
        return self.subject

    class Meta:
        ordering=['subject']
