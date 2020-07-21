# -*- coding: utf-8 -*-

import re
import json

logformat = r'^\[(?P<app_name>[^\]]*)\]\[(?P<log_level>[^\]]*)\]\[(?P<timestamp>[^\]]*)\]\[(?P<server_ip>[^\]]*)\]\[(?P<server_host>[^\]]*)\]\[(?P<req_ip>[^\]]*)\]\[(?P<pid>[^\]]*)\]\[(?P<log_id>[^\]]*)\]\[(?P<method>[^\]]*)\]\[(?P<uri>[^\]]*)\]\[(?P<exec_time>[^\]]*)\]\[(?P<step_time>[^\]]*)\]\[(?P<code_line>[^\]]*)\](?P<back_trace>[^\n]*)$'
#logformat2 = r'^(?P<back_trace>.*)$'


def linetojson(item, logformat):
    """
    解析单行日志为json
    """
    jsonstr = ''
    itempattern = re.compile(logformat)
    matches = itempattern.match(item)
    if matches != None:
        linedict = matches.groupdict()
        jsonstr = json.dumps(linedict)
    return jsonstr

def linetojson2(item, logformat):
    """
    解析单行日志为json
    """
    jsonstr = ''
    itempattern = re.compile(logformat)
    matches = itempattern.match(item)
    if matches != None:
        linedict = matches.groupdict()
        jsonstr = json.dumps(linedict, ensure_ascii=False).encode('utf8')
    return jsonstr
    
stra = """[cp][DEBUG][2015-01-21 20:50:58.758676 +0800][192.168.1.38][cp.sudongdong.xqzuche.com][192.168.1.153][26838][7acc159406b3589256dcd52119f82e19][GET][/cp/ajax_sys_notice/?t=1421844700712][82.721948623657][3.5641193389893][/home/work/website/sudongdong/modules/Account.php:309][5.78mb][{"t":"1421844700712"}][{"admin_city_code":110100,"cp_back_url":"\/cp\/order\/confirmed"}][521665] the_user_type, uid=521665, hr=admin #0 /home/work/website/sudongdong/modules/Account.php(327): Account::the_user_type(0) #1 /home/work/website/sudongdong/site/cp/actions/CP_SysNotice.php(7): Account::is_admin() #2 nofile(noline): CP_SysNotice->ajax_get_list() #3 /home/work/website/sudongdong/lib/base.php(1336): call_user_func([{},"ajax_get_list"]) #4 /home/work/website/sudongdong/lib/base.php(1474): F3::call("CP_SysNotice->ajax_get_list", true) #5 /home/work/website/sudongdong/site/cp/index-test.php(100): F3::run() """
print type(linetojson2(stra, logformat))

