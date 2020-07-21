
import sys
 
def test():
    print '666'

if __name__== "__main__":
    print len(sys.argv)
    test()
    print sys.argv[0]
    print sys.argv[1]
    print sys.argv[2]

