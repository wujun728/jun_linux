#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
#Used update game path to server  
import os,re,sys,urllib,urllib2,hashlib,time,shutil,platform  
 
def post(status, type, info, err_info=""):  
    post_url = args["post_url"]  
    aid = args["aid"]  
    data = {"aid": aid, "status": status, "type": type, "info": info}  
    if err_info:  
        data = {"aid": aid, "status": status, "type": type, "info": info, "err_info": err_info}  
    print data  
    f = urllib2.urlopen(url=post_url, data=urllib.urlencode(data))  
 
def md5sum(file_name):  
    if os.path.isfile(file_name):  
        f = open(file_name,'rb')  
        py_ver = sys.version[:3]  
        if py_ver == "2.4":  
            import md5 as hashlib  
        else:  
            import hashlib  
            md5 = hashlib.md5(f.read()).hexdigest()  
            f.close()  
            return md5  
    else:  
        return 0 
 
def config(args,files):  
    try:  
        game = args["main_prefix"]  
        url = "http://208.asktao.com/autoupdate/%s/config.ini" % game  
        get = urllib.urlopen(url)  
        aa = get.readlines()  
        w = {}  
        for i in aa:  
            a = i.strip().split()[0]  
            if "[" in a:  
                x = a.strip("[]")  
                w[x] = {}  
                continue 
            w[x][i.strip().split()[1].strip()] = i.strip().split()[0].strip()  
        for key in w:  
            if key == files:  
                return w[key]  
    except Exception,e:  
        return 0 
 
class down_start():  
 
    def work(self,args):  
        aa = config(args,"path_md5")  
        game = args["main_prefix"]  
        if aa == 0:  
            post(2,"read update config","Not find %s config file" % game)  
            sys.exit()  
        local = '/data/autoupdate/' 
        url = "http://208.asktao.com/autoupdate/%s/" % game  
        for f in aa:  
            md5_r = f.strip().split()[0]  
            pkg_name = f.strip().split()[1]  
            get = urllib.urlopen(os.path.join(url,pkg_name))  
            status = get.getcode()  
            if status == 200:#验证MD5，MD5错误的话重新下载一次，再次错误就提示失败，退出程序  
                urllib.urlretrieve(os.path.join(url,pkg_name),os.path.join(local,pkg_name),)  
                md5_l = md5sum(os.path.join(local,pkg_name))  
                if md5_l == md5_r:  
                    post(1,"down",pkg_name)  
                else:  
                    urllib.urlretrieve(os.path.join(url,pkg_name),os.path.join(local,pkg_name),)  
                    md5_l = md5sum(os.path.join(local,pkg_name))  
                    if md5_l == md5_r:  
                        post(1,"down",pkg_name)  
                    else:  
                        post(2,"down",pkg_name,"Download %s,MD5 not right" % pkg_name)  
                        sys.exit()  
            else:  
                post(2,"down",pkg_name,"Not find %s path file" % pkg_name)  
        # 检查rsync服务是否启动  
        while True:  
            pid = os.popen("ps auxww | grep 'rsync --daemon' | grep -v grep").read()  
            if not pid:  
                getso("/usr/bin/rsync --daemon")  
                continue 
            break 
        #全部完成，更新中心状态  
        post(1,"down","down_done")
 
class sync_start():  
 
    def rsync(self,update_pkg,args):  
        node_ip = args["node_ip"]  
        game = args["main_prefix"]  
        os_type = platform.system()  
        if os_type == "Windows":  
            local = "C:\\update\\" 
        elif os_type == "Linux":  
            local = "/home/update/tmp/" 
        if not os.path.isdir(local):  
            os.mkdir(local)  
        for f in os.listdir(local):  
            if os.path.isfile(f):  
                os.remove(os.path.join(local,f))  
            elif os.path.isdir(f):  
                shutil.rmtree(os.path.join(local,f))  
        aa = config(args,"path")  
        if aa == 0:  
            post(2,"read update config","Not find %s config file" % game)  
            sys.exit()  
        for f in aa:  
            if update_pkg in f:  
                md5_r = aa[f]  
                pkg_name = f  
                if os_type == "Windows":  
                    sync = "rsync -avz %s::update/*%s* /cygdrive/c/update/" % (node_ip,update_pkg)  
                elif os_type == "Linux":  
                    sync = "rsync -avz %s::update/*%s* /home/update/tmp/" % (node_ip,update_pkg)  
                result = os.popen(sync).readlines()  
                md5_l = md5sum(os.path.join(local,pkg_name))  
                if md5_l == md5_r:  
                    post(1,"sync",pkg_name)  
                else:  
                    if os_type == "Windows":  
                        sync = "rsync -avz %s::update/*%s* /cygdrive/c/update/" % (node_ip,update_pkg)  
                    elif os_type == "Linux":  
                        sync = "rsync -avz %s::update/*%s* /home/update/tmp/" % (node_ip,update_pkg)  
                    result = os.popen(sync).readlines()  
                    md5_l = md5sum(os.path.join(local,pkg_name))  
                    if md5_l == md5_r:  
                        post(1,"sync",pkg_name)  
                    else:  
                        post(2,"rsync",pkg_name,"sync Error,%s not find or file's md5 wrong" % pkg_name)  
                        sys.exit()  
 
    def work(self,args):  
        update_pkg = args["update_pkg"].split(',')  
        for i in range(len(update_pkg)):  
            self.rsync(update_pkg[i],args)  
        post(1,"sync","sync_done")  
 
class update_start():  
 
    def copy(self,src, dst):  
        if os.path.isdir(src):  
            base = os.path.basename(src)  
            if os.path.exists(dst):  
                dst = os.path.join(dst, base)  
            if not os.path.exists(dst):  
                os.makedirs(dst)  
            names = os.listdir(src)  
            for name in names:  
                srcname = os.path.join(src, name)  
                self.copy(srcname, dst)  
        else:  
            shutil.copy2(src, dst)  
 
    def unrar(self,src,dst,args):  
        os_type = platform.system()  
        try:  
            if not os.path.exists(dst) or not os.path.exists(src):  
                raise Exception, "%s or %s not exist!" % (src, dst)  
            if os_type == "Windows":  
                os.system(r'C:\Progra~1\WinRAR\rar x -o+ -inul %s %s' % (src, dst))  
            elif os_type == "Linux":  
                if os.path.splitext(src)[1] == ".tgz":  
                    os.system("tar -zxf %s -C %s" % (src, dst))  
                elif os.path.splitext(src)[1] == ".zip":  
                    os.system("unzip -oq %s -d %s" % (src, dst))  
            return 0 
        except Exception,e:  
            return e  
 
    def work(self,args):  
        os_type = platform.system()  
        if os_type == "Windows":  
            update = "C:\\update\\" 
        elif os_type == "Linux":  
            update = "/home/update/tmp/" 
        server_dir = {"tmcs":"C:\\Server\\","wd":"/home/asktao/"}  
        server = server_dir[args["main_prefix"]]  
        update_pkg = args["update_pkg"].split(',')  
        game = args["main_prefix"]  
        for i in range(len(update_pkg)):   
#####################解压更新包  
            for tgz in os.listdir(update):  
                if update_pkg[i] in tgz:  
                    src = os.path.join(update,tgz)  
                    r = self.unrar(src,update,args)  
                    if r == 0:  
                        post(1,"update","%s unzip success" % src)  
                    else:  
                        post(2,"update",src,"unzip fail:%s" % r)  
#####################拷贝更新文件到游戏目录  
            ser_list = os.listdir(server)  
            up_list = os.listdir(update)  
            for dir in up_list:  
                for line in ser_list:  
                    filepath = os.path.join(update,dir+"\\")  
                    serv = os.path.join(server,line+"\\")  
                    if dir in line:  
                        self.copy(filepath,serv)  
                        post(1,"update","%s files copy success" % line)  
#####################验证重要文件MD5  
        aa = config(args,"files")  
        if aa == 0:  
            post(2,"read update config","Not find %s config file" % game)  
            sys.exit()  
        for f in aa:  
            md5_r = aa[f]  
            pkg_name = f  
            if os.path.exists(pkg_name):  
                md5_s = md5sum(pkg_name)  
                if md5_r == md5_s:  
                    post(1,"update","%s md5 Ok,update success" % pkg_name)  
                else:  
                    post(2,"update","%s md5 Error,update fail" % pkg_name)  
                    sys.exit()  
        shutil.rmtree(update)  
        os.mkdir(update)  
        post(1,"update","All_done")  
 
if __name__ == "__main__":  
    args = {"pack":"auto_update","func1":"down_start","url":"http://208.2222.com/manage/auto_update","post_url":"http://192.168.50.209/reg.php","update_pkg":"up,up","node_ip":"192.168.50.208","main_prefix":"tmcs","aid":"123"}  
    #down = down_start()  
    #down.work(args)  
    sync = sync_start()  
    sync.work(args)  
    update = update_start()  
    update.work(args)  
 
 
[files]#需要验证MD5的重要文件绝对路径和MD5  
15a6605156e29f68fdfd637e73a889d4  C:\Server\Line1\SAFlashPlayer.exe  
15a6605156e29f68fdfd637e73a889d4  C:\Server\Line2\SAFlashPlayer.exe  
[path]#更新包名字和MD5  
32fcb8932799aa553db13b5b9b41e5e9  auto.rar  
32fcb8932799aa553db13b5b9b41e5e9  update.rar  
