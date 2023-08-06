from __init__ import *  # 排好顺序start变量覆盖
#from p.__init__ import *
from k.test import * #密码
from p.y import *
from p.yh import *
from p.yz import *
from p.qt import *
from p.beginnings import * #开头
#import threading as tr #多线程


#pypi_org()
#pdios()

'''

def get_sycc_ver():
	def sycc_ver():
	    try:
	        global ver_str
	        ver_str=list(popen('pip show sycc').read().splitlines(False))[1].split(':')[1].split('.')
	    except Exception or IndexError as e_test:
	        if len(str(e_test))>1:
	            __version__='定制版'
'''
def main():
    pdios()
    get_sycc_ver()
    
    
    A()
    user_key()
    
    # A()
    # print(version)
    print(
        "\033[7;36m本次开始使用时间:\033[0m",
        "\033[7;32m",
        start,
        "\b\b" + "\033[0m",
        "\033[1;1m",
    )
    clear_cls = 0
    while True:
        clear_cls += 1
        if clear_cls > 1:
            if os1 == "Linux":
                os.system("clear")
            elif os2 == "Windows" or os2 == "Win32":
                os.system("cls")
        print("\033[1;1m", "\b【虹源三式】".center(5))
        print(
            "===== 切换/选择模式，请选择 =====\n模式1.计算关于"
            + y_font
            + "的计算(输入1执行)\n模式2.计算关于"
            + yz_font
            + "的计算(输入2执行)\n模式3.计算关于\033[6;35m圆环\033[0m\033[1;1m的计算(输入3执行)\n模式4.计算关于"
            + qt_font
            + "的计算(输入4执行)\n输入其他字符退出\n"
        )
        yyy = input("请选择模式(输入数字):")
        try:
            yyy = eval(yyy)
        except (
            IOError,
            ValueError,
            TypeError,
            SyntaxError,
            EOFError,
            NameError,
            KeyboardInterrupt,
        ):
            print("请输入正确数字")
        except ZeroDivisionError:
            print("除数不能为0")
        if yyy == 1:
            part_y()
        elif yyy == 2:
            part_yz()
        elif yyy == 3:
            part_yh()
        elif yyy == 4:
            part_qt()
        else:
            end = sj.now() - start
            print("即将\033[10;31m退出\033[0m,", "本次使用时间:", end, "\n程序将在5秒后关闭,谢谢使用")
            exitings(5)
            tc()

main()