'''
本代码探究模块的名字空间，与模块中的变量与函数
'''

a = 100
b = 200

def add(x,y):
    '''
  本函数演示 函数实现两个数字相加
    '''
    return x+y

if __name__ == '__main__':
    print(add(a,b))
    x=dir(__builtins__)
    print(x)

    print(add.__code__ )
    print(add.__code__.co_code,add.__code__.co_names)