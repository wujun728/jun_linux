import socket, sys, time

def start_chat():
    #serv_addr = ('136.24.8.73', 1989)
    serv_addr = ('127.0.0.1', 1989)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(serv_addr)
    while True:
        data = sys.stdin.readline()
        s.send(data)
        if data.strip() == 'quit':
            print "bye!"
            time.sleep(1)
            break;
        data = s.recv(1024)
        print data
        print "\n$",
    time.sleep(1)
    s.close()

def simple_call_rpc():
    serv_addr = ('136.24.8.45', 1989)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(serv_addr)
    program_name = "R2319Cfm"
    cmd =  "find /crmbak -name %s.log.gz -mtime 30 2>/dev/null |xargs ls -l --block-size=1024 |grep %s.log.gz$ 2>/dev/null |awk '{sum+=$5}END{print sum}'" % (program_name, program_name)
    s.send(cmd)
    data = s.recv(1024)
    print 80 * '-'
    print "cmd:", cmd
    print "data:", data
    print 80 * '-'
    s.close()

if __name__ == '__main__':
    simple_call_rpc()
    #start_chat()
