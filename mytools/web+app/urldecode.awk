#!/bin/sh
#使用awk进行urldecode的脚本
#awk '
BEGIN {
hextab="0123456789ABCDEF"
for(i=1;i<=255;++i)
    ord[i]=sprintf("%c",i);
}
{
    decoded=""
    for(i=1;i<=length($0);++i)
    {
        c=substr($0,i,1)
        if(c~/[a-zA-Z0-9.-]/)
        {
            decoded=decoded c
        }
        else if(c==" ")
        {
            decoded=decoded "+"
        }
        else if(c=="%")
        {
            hi=substr($0,i+1,1);
            low=substr($0,i+2,1);
            i++;
            i++
            decoded=decoded ord[(index(hextab,hi)-1)*16+index(hextab,low)-1]
        }
    }
    print decoded
}
END {print decoded}
#'