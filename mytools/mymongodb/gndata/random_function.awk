#
# 产生各类型数据随机函数
# chm, 461810517@qq.com
# 2011/09/21
#
# 产生随机整数, 其值大于等于min, 小于等于max
function random_int(min, max) {
    return int( rand()*(max-min+1) ) + min
}
# 产生随机浮点数, 其整数部分位数最大为precision, 小数部分位数最大为scale
function random_float(precision, scale) {
    scale = 10^scale;
    return int( rand()*(10^precision) ) + int( rand()*scale )/scale
}
# 产生长度为len的随机字符串
# opt为"lower"时, 产生由小写字母构成的随机字符串; opt为"upper"时, 产生由大写字母构成的随机字符串; opt为其它时, 产生大小写字母构成的随机字符串
function random_string(opt, len) {
    if (!is_define_T) {
        is_define_T = 1;
        T_LEN_LOWER = split("a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z", T_LOWER, ",");
        T_LEN_UPPER = split("A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z", T_UPPER, ",");
        T_LEN_DEFAULT = split("a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z", T_DEFAULT, ",");
    }
    
    if (opt == "lower") {
        return _random_string(len, T_LOWER, T_LEN_LOWER);
    } else if (opt == "upper") {
        return _random_string(len, T_UPPER, T_LEN_UPPER);
    } else {
        return _random_string(len, T_DEFAULT, T_LEN_DEFAULT);
    }
}
# 产生长度为len, 由字母表alphabet中的字母构成的随机字符串
function _random_string(len, alphabet, alphabet_len, _result, _i) {
    for (_i=0; _i<len; _i++) {
        _result = _result alphabet[ random_int(1, alphabet_len) ];
    }
    return _result;
}
# 产生格式为format的随机日期时间值
# begin_time, end_time格式: YYYY MM DD HH MM SS[ DST]
# format: 日期时间格式, 如"%Y-%m-%d %H:%M:%S"
function random_time(begin_time, end_time, format) {
  begin_time = mktime(begin_time);
  end_time = mktime(end_time);
  return strftime(format, begin_time + random_int(1, end_time-begin_time+1));
}
