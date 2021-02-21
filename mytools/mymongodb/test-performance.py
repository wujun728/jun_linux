import time,pymongo,multiprocessing,random,string 
class SqlToMongo:
    def m_sql(self,x,y):
        server="mongodb://python:oracle@192.168.4.167:27017/syslog"
        conn=pymongo.Connection(server)
        db=conn.syslog
        col=db.thing
        start=x*y
        end=start+x
        for i in xrange(start,end):
            d=random.randint(start,end)
            val=col.find({"user_id":d})
            a=list(val)
def gen_load(x,taskid):
    task=SqlToMongo()
    print "task %s start!" % taskid
    task.m_sql(x,taskid)
if __name__ == "__main__": 
        inser_number=2500000
        pro_pool = multiprocessing.Pool(processes=101)
        print time.strftime('%Y-%m-%d:%H-%M-%S',time.localtime(time.time()))
        start_time=time.time()
        manager = multiprocessing.Manager()
        for i in xrange(40):
                taskid=i  
                pro_pool.apply_async(gen_load,args=(inser_number,taskid)) 
        pro_pool.close()
        pro_pool.join()
        elapsed = time.time()-start_time
        print elapsed
        time.sleep(1)
        print "Sub-process(es) done." 