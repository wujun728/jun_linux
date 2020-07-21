#-*- coding=utf-8 -*-

import web

urls = (
        '/', 'Index',
        '/(.*)', 'Info',
        );

render = web.template.render('templates', cache=False)
db = web.database(dbn='sqlite', db='../qiubai.db')

config = web.storage(
    email='withfaker@gmail.com',
    site_name = '测试',
    site_desc = '',
    static = '/static',
)

web.template.Template.globals['config'] = config

def query_next_pic(created):
    sql = "select created, img_src, content from t_qiushi where created < '{0}' order by created desc limit 1".format(created)
    res = db.query(sql)
    if not res:
        return None
    return res

class Index:
    def GET(self):
        print type(web.ctx)
        print web.ctx['environ']['REMOTE_ADDR']
        return render.index()

class Info:
    def GET(self, created):
        info = query_next_pic(created)
        if not info:
            return '{"status":99}'
        ret = '{"status":200, "data":['
        s = ""
        for i in info:
            ret = ret + '{"created":' + '"' + i['created'] + '",' + '"img_src":"' + i['img_src'] + '", "content":"' + i['content']  + '"},'
        ret = ret + ']}'
        pos = ret.rfind(',')
        ret = ret[0:pos] + ret[pos+1:]
        return ret

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
