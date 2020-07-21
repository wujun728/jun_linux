import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.database
import os
from tornado.options import define, options
import json

define("port", default=80, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3366", help="blog database host")
define("mysql_database", default="test", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="passwd", help="blog database password")

class MainHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self):
        result = self.db.get("select created, img_src, content from t_qiushi order by created desc limit 1")
        self.render("joke.html", 
            created = result["created"],
            img_src = result["img_src"],
            content = result["content"]
        )


class JokeHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self):
        created = self.get_argument("hash", "")
        sql = "select created, img_src, content from t_qiushi where created < '%s' order by created desc limit 1" % created 
        result = self.db.get(sql)
        self.write(result)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/joke", JokeHandler)
        ]
        settings = dict(
            debug         = True,
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path   = os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret = "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o"

        )
        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = tornado.database.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

def main():
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
