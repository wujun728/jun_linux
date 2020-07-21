#!/usr/bin/env python3



from struct import unpack, pack
import sys, _socket, mmap
from collections import namedtuple

DataFileName = "E:\\Soft\\QQWry.Dat"

def _ip2ulong(ip):
  return unpack('>L', _socket.inet_aton(ip))[0]

def _ulong2ip(ip):
  return _socket.inet_ntoa(pack('>L', ip))

class ipInfo(namedtuple('ipInfo', 'sip eip country area')):
  __slots__ = ()
  def __str__(self):
    '''str(x)
    '''
    # TODO: better formatting
    return str(self[0]).ljust(16) + ' - ' + str(self[1]).rjust(16) + ' ' + self[2] + self[3]

  def normalize(self):
    return self.__class__(
      _ulong2ip(self[0]), _ulong2ip(self[1]), self[2], self[3])

class QQWry:
  def __init__(self, dbfile = DataFileName, charset = 'gbk'):
    if isinstance(dbfile, (str, bytes)):
      dbfile = open(dbfile, 'rb')

    self.f = dbfile
    self.charset = charset
    self.f.seek(0)
    self.indexBaseOffset = unpack('<L', self.f.read(4))[0] 
    self.Count = (unpack('<L', self.f.read(4))[0] - self.indexBaseOffset) // 7 

  def Lookup(self, ip):
    return self.nLookup(_ip2ulong(ip))

  def nLookup(self, ip):
    si = 0
    ei = self.Count
    if ip < self._readIndex(si)[0]:
      raise LookupError('IP NOT Found.')
    elif ip >= self._readIndex(ei)[0]:
      si = ei
    else: # keep si <= ip < ei
      while (si + 1) < ei:
        mi = (si + ei) // 2
        if self._readIndex(mi)[0] <= ip:
          si = mi
        else:
          ei = mi
    ipinfo = self[si]
    if ip > ipinfo[1]:
      raise LookupError('IP NOT Found.')
    else:
      return ipinfo

  def __str__(self):
    tmp = []
    tmp.append('RecCount:')
    tmp.append(str(len(self)))
    tmp.append('\nVersion:')
    tmp.extend(self[self.Count].normalize()[2:])
    return ''.join(tmp)

  def __len__(self):
    '''len(x)
    '''
    return self.Count + 1

  def __getitem__(self, key):
    if isinstance(key, int):
      if key >=0 and key <= self.Count:
        index = self._readIndex(key)
        sip = index[0]
        self.f.seek(index[1])
        eip = unpack('<L', self.f.read(4))[0]
        country, area = self._readRec()
        if area == ' CZ88.NET':
          area = ''
        return ipInfo(sip, eip, country, area)
      else:
        raise KeyError('INDEX OUT OF RANGE.')
    elif isinstance(key, str):
      return self.Lookup(key).normalize()
    else:
      raise TypeError('WRONG KEY TYPE.')

  def _read3ByteOffset(self):
    return unpack('<L', self.f.read(3) + b'\x00')[0]

  def _readCStr(self):
    if self.f.tell() == 0:
      return 'Unknown'

    return self._read_cstring().decode(self.charset, errors='replace')

  def _read_cstring(self):
    tmp = []
    ch = self.f.read(1)
    while ch != b'\x00':
      tmp.append(ch)
      ch = self.f.read(1)
    return b''.join(tmp)

  def _readIndex(self, n):
    self.f.seek(self.indexBaseOffset + 7 * n)
    return unpack('<LL', self.f.read(7) + b'\x00')

  def _readRec(self, onlyOne=False):
    mode = unpack('B', self.f.read(1))[0]
    if mode == 0x01:
      rp = self._read3ByteOffset()
      bp = self.f.tell()
      self.f.seek(rp)
      result = self._readRec(onlyOne)
      self.f.seek(bp)
    elif mode == 0x02:
      rp = self._read3ByteOffset()
      bp = self.f.tell()
      self.f.seek(rp)
      result = self._readRec(True)
      self.f.seek(bp)
      if not onlyOne:
        result.append(self._readRec(True)[0])
    else: # string
      self.f.seek(-1,1)
      result = [self._readCStr()]
      if not onlyOne:
        result.append(self._readRec(True)[0])

    return result

class MQQWry(QQWry):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.f = mmap.mmap(self.f.fileno(), 0, access = 1)

  def _read_cstring(self):
    start = self.f.tell()
    end = self.f.find(b'\x00')
    if end < 0:
      raise Exception('fail to read C string')
    self.f.seek(end + 1)
    return self.f[start:end]

if __name__ == '__main__':
  Q = QQWry()
  if len(sys.argv) == 1:
    print(Q)
  elif len(sys.argv) == 2:
    if sys.argv[1] == '-': 
      print(''.join(Q[input()][2:]))
    elif sys.argv[1] in ('all', '-a', '-all'): 
      try:
        for i in Q:
          print(i.normalize())
      except IOError:
        pass
    else: 
      print(''.join(Q[sys.argv[1]][2:]))
  else:
    for i in sys.argv[1:]:
      print(Q[i])
