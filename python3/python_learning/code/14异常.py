'''
Created on 2018年10月10日

@author: Administrator
'''
# f=None
# try:
# #     print(num)
#     print("test1")
#     f=open("123.txt","w")
#     print("test2")
# except (FileNotFoundError,NameError) as errormsg:
#     print("报错了")
#     print(errormsg)
# else:
#     print("没有异常")
# finally:
#     print("finally----")
#     f.close()
# print("test3")
class ShortInputException(Exception):
    def __init__(self, length, atleast):
        #super().__init__() 
        self.length = length 
        self.atleast = atleast 
def main():
        try: 
            s = input('请输入 --> ') 
            if len(s) < 3: # raise引发一个你定义的异常
                raise ShortInputException(len(s), 3) 
        except ShortInputException as result:#x这个变量被绑定到了错误的实例 
            print('ShortInputException: 输入的长度是 %d,长度至少应是 %d'% (result.length, result.atleast)) 
        else: 
            print('没有异常发生.') 
main()
