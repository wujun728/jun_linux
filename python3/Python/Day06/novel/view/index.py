from django.http import HttpResponse
from django.shortcuts import render
from utils.mysql_DBUtils import mysql


# 《星辰变》章节列表
def main(request):
    sql = "SELECT id,title FROM novel LIMIT 10;"
    result = mysql.getAll(sql)
    # result = json.dumps(result, cls=MyEncoder, ensure_ascii=False, indent=4)
    # result = json.loads(result)
    context = {'novel_list': result}
    return render(request, 'novel_list.html',  context)


# def chapter(request):
#     id = request.GET['id']
#     sql = "SELECT content FROM novel where id = %(id)s;"
#     param = {"id": id}
#     result = mysql.getOne(sql, param)
#     result['content'] = result['content'].decode('utf-8')
#     context = {}
#     context["content"] =  result['content']
#     return render(request, 'novel.html', context)

'''
单个章节
此处 novel_id 对应 urls.py 中的 <int:novel_id>
你可以访问：http://localhost:8000/chapter/1/
'''
def chapter(request, novel_id):
    sql = "SELECT title,content FROM novel where id = %(id)s;"
    param = {"id": novel_id}
    result = mysql.getOne(sql, param)
    # result['title'] = result['title'].decode('utf-8')
    # result['content'] = result['content'].decode('utf-8')
    context = {'novel': result}
    return render(request, 'novel.html', context)

