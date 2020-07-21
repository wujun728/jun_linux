import socket, sys, os
import subprocess
from commands import getoutput

def exec_cmd(cmd):
    p = subprocess.Popen(['C:\\Windows\\System32\\cmd.exe', cmd], shell=True)
    p.wait()
    out, err = p.communicate()
    if not err:
        return err
    return out

def simple_rpc():
    server_addr = ("0.0.0.0", 1989)
    white_list = ["130.89.200.99", "136.24.224.4"]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(server_addr)
    s.listen(5)
    while True:
        c, addr = s.accept()
        print addr[0]
        if addr[0] not in white_list:
            c.send("forbidden")
            c.close()
        else:
            cmd = c.recv(1024).strip("\r\n")
            print "calc ..."
            print cmd
            ret = getoutput(cmd)
            print ret
            print "done ..."
            c.send(ret)
            print "after send"
            c.close()



def start_chat():
    address = ('0.0.0.0', 1989)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    c, addr = s.accept()
    print 'CONNECTION:', addr
    while True:
        cmd = c.recv(512)
        cmd = cmd.strip('\r\n ')
        print 'cmd:[%s]' % cmd
        if cmd == 'quit':
            c.close()
        if cmd == 'cmd':
            os.system("cmd.exe")
    s.close()
if __name__ == '__main__':
    simple_rpc()
    #start_chat()
