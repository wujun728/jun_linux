
#!/usr/bin/evn python
# -*- encoding: utf-8 -*-

# FTP操作
import paramiko


class Ftptest:
    def connectOfKey(self):
        pkey = u'E:/id_rsa/xxx.xxx' # 本地密钥文件路径[此文件服务器上~/.ssh/id_rsa可下载到本地]
        key = paramiko.RSAKey.from_private_key_file(pkey, password='******') # 有解密密码时,
        paramiko.util.log_to_file('paramiko.log')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # 通过公共方式进行认证 (不需要在known_hosts 文件中存在)
        # ssh.load_system_host_keys() #如通过known_hosts 方式进行认证可以用这个,如果known_hosts 文件未定义还需要定义 known_hosts
        ssh.connect(u'127.0.0.1', username=u'root', password=u'******', pkey=key) # 这里要 pkey passwordkey 密钥文件
        stdin, stdout, stderr = ssh.exec_command(u'hostname') # 执行命令
        print stdout.read() # 获取命令执行后的结果
        stdin, stdout, stderr = ssh.exec_command(u'ls')
        print stdout.read()

    def upLoad(self,pkey):
        key = paramiko.RSAKey.from_private_key_file(pkey, password='******')
        paramiko.util.log_to_file('paramiko.log')

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(u'127.0.0.1', username=u'root', password=u'******', pkey=key)
        t = ssh.get_transport()
        sftp = paramiko.SFTPClient.from_transport(t)
        d = sftp.put("/mm.txt", "/home/mm.txt")
        print d
        t.close()

    def downLoad(self,pkey):
        key = paramiko.RSAKey.from_private_key_file(pkey, password='******')
        paramiko.util.log_to_file('paramiko.log')

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(u'127.0.0.1', username=u'root', password=u'******', pkey=key)
        t = ssh.get_transport()
        sftp = paramiko.SFTPClient.from_transport(t)
        d = sftp.get("/home/mm.txt", "/mm.txt")
        print d
        t.close()

    def connect(self):
        transport = paramiko.Transport(('127.0.0.1', 22))
        transport.connect(username='xxxx', password='xxxxx')
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put("", "")
        transport.close()

    def main(self):
        #私匙存放位置
        pkey = u'E:/id_rsa/xxx.xxx'

        #链接并执行命令
        self.connectOfKey()

        #上传文件
        self.upLoad(pkey)

        # 下载文件
        self.downLoad(pkey)

        #不使用密匙文件
        self.connect()

if __name__ == '__main__':
    ftptest = Ftptest()
    ftptest.main()
