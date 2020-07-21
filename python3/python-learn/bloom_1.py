#coding:utf-8
# Bloom filters in Python
# Adam Langley <agl@imperialviolet.org>
# 给CountedBloom加了一个max_count 张沈鹏 <zsp007@gmail.com>
# Bloom-Filter算法简介
# http://www.googlechinablog.com/2007/07/bloom-filter.html
# http://zh.wikipedia.org/wiki/%E5%B8%83%E9%9A%86%E8%BF%87%E6%BB%A4%E5%99%A8
# 这个计算器可以帮你求最佳的参数
# http://www.cc.gatech.edu/~manolios/bloom-filters/calculator.html
# CountedBloom 的 buckets 参数对应于计算器的m,也就是"m denotes the number of bits in the Bloom filter"

import array
import struct

mixarray = array.array ('B', '\x00' * 256)
# The mixarray is based on RC4 and is used as diffusion in the hashing function

def mixarray_init (mixarray):
    for i in range (256):
        mixarray[i] = i
    k = 7
    for j in range (4):
        for i in range (256):
            s = mixarray[i]
            k = (k + s) % 256
            mixarray[i] = mixarray[k]
            mixarray[k] = s

mixarray_init (mixarray)

class Bloom (object):
    '''Bloom filters provide a fast and compact way of checking set membership. They do this by introducing a risk of a 
  false positive (but there are no false negatives).

  For more information see http://www.cs.wisc.edu/~cao/papers/summary-cache/node8.html'''
    def __init__ (self, bytes, hashes, data = None):
        '''@bytes is the size of the bloom filter in 8-bit bytes and @hashes is the number of hash functions to use. Consult the
    web page linked above for values to use. If in doubt, bytes = num_elements and hashes = 4'''
        self.hashes = hashes
        self.bytes = bytes

        if data == None:
            self.a = self._make_array (bytes)
        else:
            assert len (data) == bytes
            self.a = data

    def init_from_counted (self, cnt):
        '''Set the contents of this filter from the contents of the counted filter @cnt. You have to match sizes'''
        if self.bytes * 8 != (len (cnt.a) * 2):
            raise ValueError ('Filters are not the same size')
        for i in xrange (len (cnt.a)):
            b = cnt.a[i]
            b1 = (b & 0xf0) >> 4
            b2 = (b & 0x0f)
            if b1:
                self.a[(i * 2) // 8] |= self.bitmask[(i * 2) % 8]
            if b2:
                self.a[(i * 2 + 1) // 8] |= self.bitmask[(i * 2 + 1) % 8]

    def _make_array (self, size):
        a = array.array ('B')
        # stupidly, there's no good way that I can see of resizing an array without allocing a huge string to do so
        # thus I use this, slightly odd, method:

        blocklen = 256
        arrayblock = array.array ('B', '\x00' * blocklen)
        todo = size
        while (todo >= blocklen):
            a.extend (arrayblock)
            todo -= blocklen
        if todo:
            a.extend (array.array ('B', '\x00' * todo))
        # now a is of the right length
        return a

    def _hashfunc (self, n, val):
        '''Apply the nth hash function'''

        global mixarray

        b = [ord(x) for x in struct.pack ('I', val)]
        c = array.array ('B', [0, 0, 0, 0])
        for i in range (4):
            c[i] = mixarray[(b[i] + n) % 256]

        return struct.unpack ('I', c.tostring())[0]

    bitmask = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]

    def insert (self, val):
        for i in range (self.hashes):
            n = self._hashfunc (i, val) % (self.bytes * 8)
            self.a[n // 8] |= self.bitmask[n % 8]

    def __contains__ (self, val):
        for i in range (self.hashes):
            n = self._hashfunc (i, val) % (self.bytes * 8)
            if not self.a[n // 8] & self.bitmask[n % 8]:
                return 0
        return 1
MAX_COUNT = 15
class CountedBloom (Bloom):
    '''Just like a Bloom filter, but provides counting (e.g. you can delete as well). This uses 4 bits per bucket, so is
  generally four times larger than the same non-counted bloom filter.'''

    def __init__ (self, buckets, hashes):
        '''Please note that @buckets must be even. Also note that with a Bloom object you give the number of *bytes* and each byte is 8 buckets. Here you're giving the number of buckets.'''
        assert buckets % 2 == 0
        self.hashes = hashes
        self.buckets = buckets

        self.a = self._make_array (buckets // 2)

    def insert (self, val):
        masks  = [(0x0f, 0xf0), (0xf0, 0x0f)]
        shifts = [4, 0           ]

        for i in range (self.hashes):
            n = self._hashfunc (i, val) % self.buckets
            byte         = n // 2
            bucket = n % 2
            (notmask, mask) = masks[bucket]
            shift        = shifts[bucket]
            bval         = ((self.a[byte] & mask) >> shift)
            if bval < MAX_COUNT: # we shouldn't increment it if it's at the maximum
                bval += 1

            self.a[byte] = (self.a[byte] & notmask) | (bval << shift)
    def __contains__ (self, val):
        masks        = [(0x0f, 0xf0), (0xf0, 0x0f)]
        shifts = [4, 0]

        for i in range (self.hashes):
            n = self._hashfunc (i, val) % self.buckets
            byte         = n // 2
            bucket = n % 2
            (notmask, mask) = masks[bucket]
            shift        = shifts[bucket]
            bval          = ((self.a[byte] & mask) >> shift)

            if bval == 0:
                return 0
        return 1

    def max_count(self, val):
        masks        = [(0x0f, 0xf0), (0xf0, 0x0f)]
        shifts = [4, 0]
        count_val = MAX_COUNT
        for i in range (self.hashes):
            n = self._hashfunc (i, val) % self.buckets
            byte         = n // 2
            bucket = n % 2
            (notmask, mask) = masks[bucket]
            shift        = shifts[bucket]
            bval          = ((self.a[byte] & mask) >> shift)

            if bval < MAX_COUNT:
                if bval == 0:
                    return 0
                else:
                    count_val = bval
        return count_val

    def __delitem__ (self, val):
        masks  = [(0x0f, 0xf0), (0xf0, 0x0f)]
        shifts = [4, 0]

        for i in range (self.hashes):
            n = self._hashfunc (i, val) % self.buckets
            byte         = n // 2
            bucket = n % 2
            (notmask, mask) = masks[bucket]
            shift        = shifts[bucket]
            bval          = ((self.a[byte] & mask) >> shift)

            if bval < MAX_COUNT: # we shouldn't decrement it if it's at the maximum
                bval -= 1

            self.a[byte] = (self.a[byte] & notmask) | (bval << shift)

__all__ = ['Bloom']

if __name__ == '__main__':
    print 'Testing bloom filter: there should be no assertion failures'
    a = Bloom (3, 4)

    a.insert (45)
    print a.a
    a.insert (17)
    print a.a
    a.insert (12)
    print a.a
    assert 45 in a

    assert 45 in a
    assert not 33 in a
    assert 45 in a
    assert 17 in a
    assert 12 in a

    c = 0
    for x in range (255):
        if x in a:
            c += 1
    print c
    print float(c)/255


    a = CountedBloom (24, 4)
    a.insert (45)
    print a.a
    a.insert (17)
    print a.a
    a.insert (12)
    a.insert (12)
    print "a.max_count(12)", a.max_count(12)
    a.insert ("张沈鹏")
    a.insert ("张沈鹏")
    a.insert ("张沈鹏")
    print "a.max_count(zsp)", a.max_count(12)
    print a.a
    assert 45 in a

    assert 45 in a
    assert not 33 in a
    assert 45 in a
    assert 17 in a
    assert 12 in a

    c = 0
    for x in range (255):
        if x in a:
            c += 1
    print c
    print float(c)/255

    del a[45]
    assert not 45 in a

    a2 = Bloom (3, 4)
    a2.init_from_counted (a)

    print a2.a

    assert 17 in a2
    assert 12 in a2
    assert not 45 in a

