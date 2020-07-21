//关于布隆过滤器在URL去重中的应用  
  
//问题背景  
/** 
假设你想从网上(新浪新闻)去下载一批网页,做信息检索(搜索引擎)的第一步. 
你已经从网上下载下来了一批网页,并且有这批网页的URL,不过你还有一批需要下载的网页的URL, 
问题是这样的,如果有些URL已经被下载过了,你就不必要再次下载了,现在让你快速的识别 
出哪些URL上的是还没被下载的,可以有一定的误差,但是不能超过1%。. 
**/   
  
//本例中URL初始数量为20万条 ，如果有其它规模的数据，可以将具体参数进行相应更改  
//测试URL数量为186083条  
//请使用标准C＋＋进行编译  
//更多hash函数请登录 泪下的天空  
//原代码高亮显示  
  
#include <string>  
#include <iostream>  
#include <assert.h>  
#include <fstream>  
#include <time.h>  
using  namespace std;  
  
  
#define FUNC_NUM 8  
#define BIT_MAX 3999949 //这是一个素数，why?  
const int  HASH_SIZE = BIT_MAX / 8  + 1;  
  
char    hash[HASH_SIZE];  
int     strInt[FUNC_NUM];  
  
//以下标<<[1-8]>>数字的是字符串散列函数，本程序中我使用了８个散列函数  
  
//<<1>>  
unsigned int RSHash(const std::string& str)  
{  
   unsigned int b    = 378551;  
   unsigned int a    = 63689;  
   unsigned int hash = 0;  
  
   for(std::size_t i = 0; i < str.length(); i++)  
   {  
      hash = hash * a + str[i];  
      a    = a * b;  
   }  
  
   return hash;  
}  
  
//<<2>>  
unsigned int JSHash(const std::string& str)  
{  
   unsigned int hash = 1315423911;  
  
   for(std::size_t i = 0; i < str.length(); i++)  
   {  
      hash ^= ((hash << 5) + str[i] + (hash >> 2));  
   }  
  
   return hash;  
}  
  
//<<3>>  
unsigned int PJWHash(const std::string& str)  
{  
   unsigned int BitsInUnsignedInt = (unsigned int)(sizeof(unsigned int) * 8);  
   unsigned int ThreeQuarters     = (unsigned int)((BitsInUnsignedInt  * 3) / 4);  
   unsigned int OneEighth         = (unsigned int)(BitsInUnsignedInt / 8);  
   unsigned int HighBits          = (unsigned int)(0xFFFFFFFF) << (BitsInUnsignedInt - OneEighth);  
   unsigned int hash              = 0;  
   unsigned int test              = 0;  
  
   for(std::size_t i = 0; i < str.length(); i++)  
   {  
      hash = (hash << OneEighth) + str[i];  
  
      if((test = hash & HighBits)  != 0)  
      {  
         hash = (( hash ^ (test >> ThreeQuarters)) & (~HighBits));  
      }  
   }  
  
   return hash;  
}  
  
//<<4>>  
unsigned int APHash(const std::string& str)  
{  
   unsigned int hash = 0xAAAAAAAA;  
  
   for(std::size_t i = 0; i < str.length(); i++)  
   {  
      hash ^= ((i & 1) == 0) ? (  (hash <<  7) ^ str[i] * (hash >> 3)) :  
                               (~((hash << 11) + (str[i] ^ (hash >> 5))));  
   }  
  
   return hash;  
}  
  
//<<5>>  
unsigned int BKDRHash(const std::string& str)  
{  
   unsigned int seed = 131; // 31 131 1313 13131 131313 etc..  
   unsigned int hash = 0;  
  
   for(std::size_t i = 0; i < str.length(); i++)  
   {  
      hash = (hash * seed) + str[i];  
   }  
  
   return hash;  
}  
  
//<<6>>  
unsigned int SDBMHash(const std::string& str)  
{  
   unsigned int hash = 0;  
  
   for(std::size_t i = 0; i < str.length(); i++)  
   {  
      hash = str[i] + (hash << 6) + (hash << 16) - hash;  
   }  
  
   return hash;  
}  
  
//<<7>>  
unsigned int FNVHash(const std::string& str)  
{  
   const unsigned int fnv_prime = 0x811C9DC5;  
   unsigned int hash = 0;  
   for(std::size_t i = 0; i < str.length(); i++)  
   {  
      hash *= fnv_prime;  
      hash ^= str[i];  
   }  
  
   return hash;  
}  
  
//<<8>>  
 unsigned int Hflp(string str){  
        unsigned int len = str.length();  
        unsigned int sum = 0;  
        for(std::size_t i=0;i<len;i++){  
               sum ^= str[i] << (8*(i%4));  
        }  
         return sum & 0x7FFFFFFF;  
 }  
  
//更多hash函数请登录 http://jinyun2012.blog.sohu.com  
  
  
//将一个具体的url散列成一组整数  
void getIntSet(string url , int * set)  
{  
        set[0] = RSHash(url)   % BIT_MAX;  
        set[1] = JSHash(url)   % BIT_MAX;  
        set[2] = PJWHash(url)  % BIT_MAX;  
        set[3] = APHash(url)   % BIT_MAX;  
        set[4] = BKDRHash(url) % BIT_MAX;  
        set[5] = SDBMHash(url) % BIT_MAX;  
        set[6] = FNVHash(url)  % BIT_MAX;  
        set[7] = Hflp(url)     % BIT_MAX;  
}  
  
//将每个url映射到hash数组中  
void shadeHash(string url){  
        getIntSet(url , strInt);  
        for(int i=0;i<FUNC_NUM;i++){  
                int pos = (strInt[i] >> 3);  
                int mod = strInt[i] & 7;  
                int val = 1 << (7 - mod);  
                hash[pos] |= val;  
        }  
}  
  
//查找url是否存在于url.dat文件中  
bool find(string url)  
{  
        getIntSet(url , strInt);  
        bool res = true;  
        for(int i=0;i<FUNC_NUM && res == true; i++){  
                int pos = (strInt[i] >> 3);  
                int mod = strInt[i] & 7;  
                int val = 1 << (7 - mod);  
                res &= (bool)(hash[pos] & val);  
        }  
        return res;  
}  
  
int main(int argc, char* argv[])  
{  
        ifstream url_in("url.dat");  
        assert(url_in != NULL);  
        string url;  
        int len(0);  
        time_t con_start = time(NULL);  
        while(getline(url_in , url)){  
                len += url.length();  
                shadeHash(url);  
        }  
        time_t con_end = time(NULL);  
        url_in.close();  
  
        //读取文件中测试数据  
        ifstream test_in("test_url.dat");  
        assert(test_in);  
        int count(0) , size(0);  
        time_t test_start = time(NULL);  
        while(getline(test_in , url)){  
                size++;  
                if(find(url))count++;  
        }  
        time_t test_end = time(NULL);  
  
        cout<<"测试URL数量："<<size<<endl;  
        cout<<"错配URL数量："<<count<<endl;  
        cout<<"错配概率   : "<<count * 1.0 / size<<endl << endl;  
  
        cout<<"关于优势--->"<<endl;  
        cout<<"原URL所占存储空间:        "<<len <<" byte"<<endl;  
        cout<<"程序需要存储空间 :         "<< HASH_SIZE<<" byte"<<endl;  
        cout<<"空间节约       ：       "<< 1.0 - HASH_SIZE * 1.0 / len <<endl;  
        cout<<"构造hash表所用时间        "<<(con_end - con_start)<<"s"<<endl;  
        cout<<"测试所用时间                 "<<(test_end - test_start)<<"s"<<endl;  
            return 0;  
}  
