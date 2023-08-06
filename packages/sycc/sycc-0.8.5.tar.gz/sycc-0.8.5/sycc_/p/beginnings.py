__Author__='神秘的·'
__Project__='虹源三式'
link='https://project.sycc1.tk'
from time import sleep as dd
from sys import path
path.append('..')
path.append('.')
from tqdm._tqdm import trange
from random import uniform as float__wait_time
from k.Mac import bs64
from os import popen
from os.path import exists,isfile
import sys as s, time as t
import threading
from pip_check.pip_ import *
import socket
from v import *
import platform
import os
from os.path import split as path1,realpath as path2,exists,getsize as size;from sys import argv as path3
now_path=path1(path2(path3[0]))[0]
#from k.test import now_path
version=[]
#print(platform.system)
def clr_cls():
    if platform.system()== "Linux":
        os.system("clear")
    elif platform.system()=='windows':
        os.system("cls")    
def pypi_org():
    s = socket.socket()
    s.settimeout(10)
    try:
        readme = open(now_path + "/.net.txt", "a+")
        status = s.connect_ex(("pypi.org", 443))
        if status == 0:
            s.close()
            if size(now_path + "/.net.txt") == 0:
                save_v(1, now_path + "/.net.txt")
            else:
                pass
            if load_v(now_path + "/.net.txt") == 1:
                import webbrowser#
                open_web = 3
                while open_web in range(1, 4):
                    open_web = open_web - 1
                    print("\r将在%ds后打开浏览器查看sycc的介绍,请勿关闭" % open_web, end="", flush=True)
                    dd(1)
                    if open_web<=1:
                        webbrowser.open(link, new=0, autoraise=True)
                        save_v(0, now_path + "/.net.txt")
            else:
                print('readme:'.upper(),load_v(now_path+"/.net.txt"))
        else:
            print(1)
    except Exception as e:
        print("NET:{}".format(e))

def get_sycc_ver():
	pypi_org()
	def sycc_ver():
	    try:
	        global ver_str
	        ver_str=list(popen('pip show sycc').read().splitlines(False))[1].split(':')[1].split('.')
	    except Exception or IndexError as e_test:
	        if len(str(e_test))>1:
	            __version__='定制版'
	
	def wf():
	    print('\r请稍等,全力加载中')  
	    (threading.Thread(target=sycc_ver)).start()
	    def wait_ver():
	                try:
	                    if len(version)>3:
	                        for x in range(len(version),0,1):
	                            del version[x]
	                    elif len(version)==0:
	                        version.append(ver_str[0])
	                        version.append(ver_str[1])
	                        version.append(ver_str[2])
	                        dd(0.1)
	                except Exception as e1:
	                    print('error1:',e1)
	                    __version__='定制版'
	    with trange(0,10) as t:
	        for i in t:
	            t.set_description('sycc')
	            dd_random=float__wait_time(0.6,1.2)
	            dd(0.12)
	            dd(dd_random)
	
	    try:
	        version.append(ver_str[0])
	        dd(0.01)
	        version.append(ver_str[1])
	        dd(0.01)
	        version.append(ver_str[2])
	        dd(0.01)
	    except Exception:
	        print('请耐心等待…')
	        if len(version)!=3:
	            dd(2)
	        else:
	            wait_ver()
	        #os.system('')
	    if  len(version)>3:
	        wait_ver()
	        
	        dd(0.02)
	        #clr_cls()
	    elif len(version)==3:
	        dd(0.02)
	        #clr_cls()
	    else:        
	        for dd_tips in ['请  ','耐心 ','等待 ','几秒 ',',  ','子线程','未运行','完成 ']:#空格凑位
	            print(dd_tips,end='\r',flush=True)
	            dd(0.5)
	            
	            if dd_tips=='完成 ':
	                print('    ',end='\r')
	                dd(0.01)
	        wait_ver()
	        if len(version)==3:
	            print('\ndone!')
	            dd(0.02)
	            #clr_cls()
	if pip_check_test()==1:
		wf()
	else:
		global __version__
		__version__=='定制版'
def A():
    try:
        __version__=version[0]+'.'+version[1]+'.'+version[2]
    except Exception:
        __version__='定制版'
    clr_cls()
    print('\n\033[1;25;44m作者:' ,__Author__,'\033[0m')  
    print('\033[1;25;44m版本:',__version__,'\033[0m')
    print('\033[1;25;44mname:',__Project__,'\033[0m')
    print('\033[1;25;33m联系lwb@sycc1.tk或在关注b站账号即可获取账号密码，获取账号密码\033[0m')
    #print('\033[1;25;44mDescribe_README:',link,'\033[0m')
    dd(0.3)
    #print('\033[1;44m支持\033[0m','输入运算符(选项除外),\033[0m(使用英文字符)')
    #dd(0.02)
pai2='π' #下面要用到，提前放上来 
def dw():#单位
    print('请自行换算单位并保持单位一致')
from math import pi as pai1
def aboutpi():
    print('''
    请选择π的值
    1.输入1,π为3.14
    2.输入2,π为''',pai1,
    '''
    3.输入3,保留π(π不换成数字)
    4.输入4,π自定义大小(大于3 ,小于3.2)
    其他选项:
    5.输入5,切换模式
    6.输入不是1~5中的数,直接退出''')
#wf();A()#test

    
