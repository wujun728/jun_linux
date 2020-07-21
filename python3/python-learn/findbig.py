import os.path
from os.path import isfile, isdir, join, getsize
from sys import argv, exit
import getopt

def find_big_directory(p, big_size):
    total_size = 0
    try:
        items = os.listdir(p)
    except:
        items = []
    for item in items:
        fp = join(p, item)
        if isfile(fp):
            total_size = total_size + getsize(fp)
        else:
            total_size = total_size + find_big_directory(fp, big_size)
    if total_size > big_size:
        pprint(p, total_size)
    return total_size


def find_big_file(p, big_size):
    total_size = 0
    try:
        items = os.listdir(p)
    except:
        items = []
    for item in items:
        fp = join(p, item)
        if isfile(fp):
            total_size = getsize(fp)
            if total_size > big_size:
                pprint(fp, total_size)
        else:
            find_big_file(fp, big_size)

def pprint(p, size):
    if size < 1024:
        print "[%s]: %.2f Bytes" % (p, size)
    elif size < (1024 * 1024):
        print "[%s]: %.2f Kib" % (p, float(size) / 1024)
    elif size < (1024 * 1024 * 1024):
        print "[%s]: %.2f Mib" % (p, float(size) / (1024 * 1024))
    elif size < (1024 * 1024 * 1024 * 1024):
        print "[%s]: %.2f Gib" % (p, float(size) / (1024 * 1024 * 1024))
    else:
        print "[%s]: %.2f Tib" % (p, float(size) / (1024 * 1024 * 1024 * 1024))


def usage():
    print '''
        python findbig.py [options]

        -t, --type          dir or file, find bing dir or find big file
        -d, --dir           the dir to find
        -m, --minsize       find dir or file size large than minsize
        -h, --help          show help
        -v, --version       show version
    '''
    exit(0)

if __name__ == '__main__':
    dst_dir = ""
    big_size = ""
    query_type = ""
    try:
        options, args = getopt.getopt(argv[1:], "hvt:d:m:", ["help", "type=" "dir=", "minsize="])
    except:
        usage()
    for o, v in options:
        if o in ("-h", "--help"):
            usage()
        if o in ("-v", "--version"):
            print "0.0.1 --by withrock"
            exit(0)
        if o in ("-t", "--type"):
            if v in ("dir", "file"):
                query_type = v
            else:
                usage()
        if o in ("-d", "--dir"):
            dst_dir = v
            if not isdir(dst_dir):
                print "dir invalid."
                usage()
        if o in ("-m", "--minsize"):
            try:
                big_size = long(v)
            except:
                print "minsize invalid."
                usage()
    if query_type == "" or dst_dir == "" or big_size == "":
        usage()
    if query_type == "dir":
        find_big_directory(dst_dir, big_size)
    else:
        find_big_file(dst_dir, big_size)
