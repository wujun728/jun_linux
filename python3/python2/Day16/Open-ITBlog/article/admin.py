from django.contrib import admin

# Register your models here.
from .models import ArticlePost
from .forms import Remark

admin.site.register(ArticlePost)

class RemarkAdmin(admin.ModelAdmin):
    list_display = ('subject','mail','topic','message')

admin.site.register(Remark,RemarkAdmin)