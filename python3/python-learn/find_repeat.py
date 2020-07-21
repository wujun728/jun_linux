#!/usr/bin/env python2

import os.path
from os.path import isfile, isdir, join, getsize, basename
from sys import argv, exit
import getopt
from hashlib import md5

'''
    date:   2015-07-16 12:56:27
    author: withrock
    mail:   withfaker@gmail.com
    desc:   this tool is used to find content-repeated file in a directory tree. 
            it didn't use md5 hash because of calcluating hash slowly for big file.
            i wrote a simple hash function `calc_hash` whhich just depends on file size and file name.
            if you have good idea for quickly calcluating file hash, 
            you can give me some advise, thank you!
'''

def calc_hash(filepath, size):
    data = str(size) + "-" + basename(filepath)
    m = md5()
    m.update(data)
    return m.hexdigest()

def calc_hash_slow(filepath, size):
    buffer_size = 1024*1024*2
    handle = open(filepath, "rb")
    m = md5()
    while True:
        data = handle.read(buffer_size)
        if not data:
            break
        m.update(data)
    handle.close()
    return m.hexdigest()

def pretty_size(size):
    if size < 1024:
        return "%.2f Bytes" % size
    elif size < (1024 * 1024):
        return "%.2f Kibs" % (float(size) / 1024.00)
    elif size < (1024 * 1024 * 1024):
        return "%.2f Mibs" % (float(size) / (1024.00 * 1024.00))
    elif size < (1024 * 1024 * 1024 * 1024):
        return "%.2f Gibs" % (float(size) / (1024.00 * 1024.00 * 1024.00))
    else:
        return "%.2f Tibs" % (float(size) / (1024.00 * 1024.00 * 1024.00 * 1024.00))

'''
{
    hash1 --> [(path, filesize), ...],
    hash2 --> [(path, filesize), ...],
    hash3 --> [(path, filesize), ...],
    hash4 --> [(path, filesize), ...]
    ...
}
'''
data_set = {}

def insert_data(data):
    _hash = data['hash']
    if not data_set.has_key(_hash):
        data_set[_hash] = [data[_hash], ]
    else:
        data_set[_hash].append(data[_hash])

def analyze_data():
    for _hash in data_set:
        if len(data_set[_hash]) > 1:
            print "-" * 40
            for one in data_set[_hash]:
                print "\t", one

def find_repeat(p, big_size):
    '''find repeat-content file'''
    try:
        items = os.listdir(p)
    except:
        items = []
    for item in items:
        fp = join(p, item)
        if isfile(fp):
            file_size = getsize(fp)
            if file_size > big_size:
                _hash = calc_hash(fp, file_size)
                _size = pretty_size(file_size)
                data = { 
                        'hash': _hash,
                        _hash : (fp, _size)
                        }
                insert_data(data)
        else:
            find_repeat(fp, big_size)

def usage():
    print '''
        python find_repeat.py [options]

        -d, --dir           the dir to find
        -m, --minsize       find size large than minsize
        -h, --help          show help
        -v, --version       show version
    '''
    exit(0)

if __name__ == '__main__':
    big_size = ""
    query_dir = ""
    try:
        options, args = getopt.getopt(argv[1:], "hvd:m:", ["help", "dir=", "minsize="])
    except:
        usage()
    for o, v in options:
        if o in ("-h", "--help"):
            usage()
        if o in ("-v", "--version"):
            print "0.0.1 --by withrock"
            exit(0)
        if o in ("-d", "--dir"):
            query_dir = v
            if not isdir(query_dir):
                print "dir invalid."
                usage()
        if o in ("-m", "--minsize"):
            try:
                big_size = long(v)
            except:
                print "minsize invalid."
                usage()
    if not big_size or not query_dir:
        usage()
    find_repeat(query_dir, big_size)
    analyze_data()
