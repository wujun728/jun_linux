from bencode import bencode, bdecode
import socket
from threading import Thread
import random
from hashlib import sha1
import time
import json
import struct
from Queue import Queue
import binascii
from SimpleXMLRPCServer import SimpleXMLRPCServer

BOOTSTRAP_NODES = [
    ("router.bittorrent.com", 6881),
    ("dht.transmissionbt.com", 6881),
    ("router.utorrent.com", 6881)
] 

q = Queue()

def entropy(bytes):
    s = ""
    for i in range(bytes):
        s += chr(random.randint(0, 255))
    return s


class DHT(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.ufd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.ufd.bind(("0.0.0.0", 6881))
        self.nid = self.rand_id()
        self.next_sequence = 0
        self.version = 'CWxx'
        self.new_nodes = []
        self.db = open("data.txt", "a")

    def rand_id(self):
        hash = sha1()
        hash.update( entropy(20) )
        return hash.digest()
    
    def new_sequence(self):
        seq = '%8d' % (self.next_sequence % 65536*65535)
        self.next_sequence += 1
        return seq

    def parse_nodes(self, nodes):
        n = []
        length = len(nodes)
        if (length % 26) != 0: 
            return n
        for i in range(0, length, 26):
            nid = nodes[i:i+20]
            ip = socket.inet_ntoa(nodes[i+20:i+24])
            port = struct.unpack("!H", nodes[i+24:i+26])[0]
            n.append( (ip, port) )
        return list(set(n))

    def run(self):
        while True:
            try:
                data, addr = self.ufd.recvfrom(65536)
            except:
                print "ERROR:recv data"
                continue
            try:
                msg = bdecode(data)
            except:
                print "bdecode error"
                continue
            self.recieve_msg(msg, addr)

    def recieve_msg(self, msg, addr):
        #print "++++++++++++RESPONSE MSG++++++++++++++"
        #print msg
        #print "++++++++++++RESPONSE MSG++++++++++++++"
        try:
            t = msg['y']
        except:
            return
        if t == "q":
            self.parse_request(msg, addr)
        elif t == "r":
            self.parse_response(msg, addr)
        else:
            print "IT'S AN ERROR MSG"

    def send_message(self, addr, msg):
        data = bencode(msg)
        try:
            self.ufd.sendto(data, addr)
        except:
            return
            #print '[ERROR] sending', msg, 'to', addr

    def parse_request(self, msg, addr):
        query_method = msg['q']
        resp_msg = {}
        if query_method == "ping":
            print "++++++ GOT A PING REQUEST++++++++"
            resp_msg = {
                "t": self.new_sequence(),
                "y": "r",
                "r": {"id": self.nid}
            }
        elif query_method == "find_node":
            print "++++++ GOT A FIND_NODE REQUEST++++++++"
            resp_msg = {
                "t": msg['t'],
                "y": "r",
                "r": { "id":self.nid, "nodes":""}
            }
        elif query_method == "get_peers":
            print "++++++ GOT A GET_PEERS REQUEST++++++++"
            print "----------ADDR:", addr
            resp_msg = {
                "id": self.nid,
                "t": msg["t"],
                "y": "r",
                #"r": {"id":self.nid, "token":"tokenstr", "values":""}
                "r": {"id":self.nid, "token":"tokenstr", "nodes":""}
            }
            self.log_infohash(msg, addr)
        elif query_method == "announce_peer":
            print "++++++ GOT A ANNOUNCE_PEER REQUEST++++++++"
        # send reply
        self.send_message(resp_msg, addr)

    def log_infohash(self, msg, addr):
        infohash = binascii.hexlify(msg["a"]["info_hash"])
        print ">>>>>>>>>>>>>  [%s] <<<<<<<<<<<<<<<<<<<" % infohash
        q.put(infohash)
        #self.db.write(infohash + "\n")
        #self.db.flush()

    def parse_response(self, msg, addr):
        try:
            l = self.parse_nodes(msg['r']['nodes'])
        except:
            return
        for node in l:
            self.new_nodes.append(node)

    def ping(self, addr):
        m = {
            'v': self.version,
            't': self.new_sequence(),
            'y': 'q',
            'q': 'ping',
            'a': {
                'id': self.nid
            }
        }
        self.send_message(addr, m)

    def find_node(self, addr, target_id):
        m = {
            'v': self.version,
            't': self.new_sequence(),
            'y': 'q',
            'q': 'find_node',
            'a': {
                'id': self.nid,
                'target': target_id,
            }
        }
        self.send_message(addr, m)

    def get_peers(self, addr, info_hash):
        m = {
            'v': self.version,
            't': self.new_sequence(),
            'y': 'q',
            'q': 'get_peers',
            'a': {
                'id': self.nid,
                'info_hash': info_hash,
            }
        }
        self.send_message(addr, m)

    def distance(self, a, b):
        dist = sum([bin(ord(x) ^ ord(y)).count('1') for x,y in zip(a,b)])
        return dist

    def boot(self):
        print "+++++++++++++BOOT START+++++++++++++++"
        for addr in BOOTSTRAP_NODES:
            self.find_node(addr, self.rand_id())
    
    def auto_find(self):
        print "+++++++++++++AUTO FIND+++++++++++++++"
        for addr in self.new_nodes:
            self.get_peers(addr, self.rand_id())

def get_hash():
    return q.get()

def rpc_server():
    server = SimpleXMLRPCServer(('0.0.0.0', 1989))
    server.register_function(get_hash, 'get_hash')
    server.serve_forever()


if __name__ == '__main__':
    rpc_thread = Thread(target=rpc_server)
    rpc_thread.start()
    d = DHT()
    d.start()
    d.boot()
    while True:
        d.auto_find()
        time.sleep(1)
    d.join()
