# -*- coding: utf-8 -*-
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer

'''
-- 自带web服务
python -m http.server port

-- pip install pyftpdlib

python -m pyftpdlib -i 127.0.0.1 -w -d /file/ -u user -P 123456

-i 指定IP地址（默认为本机所有可用 IP 地址）
-p 指定端口（默认为 2121）
-w 写权限（默认为只读）
-d 指定目录 （默认为当前目录）
-u 指定登录用户名
-P 指定登录密码

更多 python -m pyftpdlib --help

'''

if __name__ == '__main__':
    authorizer = DummyAuthorizer()
    '''
        权限说明：
        Read permissions:
         - "e" = change directory (CWD command)
         - "l" = list files (LIST, NLST, STAT, MLSD, MLST, SIZE, MDTM commands)
         - "r" = retrieve file from the server (RETR command)

        Write permissions:
         - "a" = append data to an existing file (APPE command)
         - "d" = delete file or directory (DELE, RMD commands)
         - "f" = rename file or directory (RNFR, RNTO commands)
         - "m" = create directory (MKD command)
         - "w" = store a file to the server (STOR, STOU commands)
         - "M" = change file mode (SITE CHMOD command)
         - "T" = update file last modified time (MFMT command)
    '''
    '''
     这里我们创建一个管理员，拥有所有权限，创建一个普通用户，只拥有浏览权限
    '''
    authorizer.add_user('admin', 'admin', 'F:\\file', perm='elradfmwM')
    authorizer.add_user('user', 'user', 'F:\\file')
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(('0.0.0.0', 8888), handler)
    server.serve_forever()


