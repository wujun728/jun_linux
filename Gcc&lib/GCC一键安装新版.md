# [GCC一键安装新版](https://www.cnblogs.com/longzhu/p/gcc_update.html)

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
cd /usr/local/src/
wget http://mirrors-usa.go-parts.com/gcc/releases/gcc-6.2.0/gcc-6.2.0.tar.bz2
wget ftp://ftp.gnu.org/gnu/mpc/mpc-1.0.3.tar.gz
wget --no-check-certificate https://gmplib.org/download/gmp/gmp-6.1.1.tar.bz2
wget http://www.mpfr.org/mpfr-current/mpfr-3.1.4.tar.bz2
tar zxf mpc-1.0.3.tar.gz
cd mpc-1.0.3
 ./configure --prefix=/usr/local/mpc103
make && make install
cd ..
tar jxf gmp-6.1.1.tar.bz2
cd gmp-6.1.1
./configure --prefix=/usr/local/gmp611
make && make install
cd ..
tar jxf mpfr-3.1.4.tar.bz2
cd mpfr-3.1.4
./configure --prefix=/usr/local/mpfr314 --with-gmp=/usr/local/gmp611
make && make install
cd ..
declare -x LD_LIBRARY_PATH=":/usr/local/mpc103/lib:/usr/local/mpfr314/lib:/usr/local/gmp611/lib"
cd cd gcc-6.2.0
./configure --with-mpc=/usr/local/mpc103 --with-gmp=/usr/local/gmp611 --with-mpfr=/usr/local/mpfr314 --disable-multilib
make && make install
cd ..
tar gcc-6.2.0.tar.bz2
cd gcc-6.2.0./configure --prefix=/usr/local/gcc620 --with-mpc=/usr/local/mpc103 --with-gmp=/usr/local/gmp611 --with-mpfr=/usr/local/mpfr314 --disable-multilibmake && make install
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)