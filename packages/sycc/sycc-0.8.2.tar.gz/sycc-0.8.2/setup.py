# 2020-2022
from setuptools import setup
import os
import platform
import sys, time
import threading
import subprocess

def pip_check_test():
	def pip_check_Exist():
		try:
		 	import pip
		except ImportError:
			return False
		else:
			return True
	if pip_check_Exist()==False:
		print('\033[1;1mpip不存在\033[0m')
	else:
		pass
	def pip_check_use():
		import os
		try:
			pip_check_use_global=str(os.popen('pip -V').read().splitlines(False)[0]).split(' ')[0]
			if 'pip' == pip_check_use_global:
				return True
			else:
				return False
		except:
			pass
	#print(pip_check_use())
	if (pip_check_use() and pip_check_Exist())==True:
		return 1


if platform.system() == "Linux":  #
    pass
elif platform.system() == "Windows":
    pass
elif pip_check_test()!=1:
	print('没有pip,不支持使用!')
	time.sleep(10)
	sys.exit()
else:
    print("不支持该系统")
    time.sleep(10)
    sys.exit()
try:
    import netifaces
except ImportError:
	#import os
	(
        threading.Thread(target=(subprocess.call("pip install netifaces", shell=True)))
    ).start()
if platform.system()=='Linux':
		print("\033[1;33m欢迎\033[0m使用，\033[1;31m虹源三式\033[0m")
		time.sleep(1)
		print("""\033[1;1m\a公告\033[0m:
			\t1.联系\033[1;1mlwb@sycc1.tk\033[0m获取账号密码，谢谢，祝您新年快乐
			\t2.\033[1;1msycc\033[0m命令运行
			\t3.本项目提供pip安装,终端输入get-pip即可下载pip""")
		time.sleep(2)
		os.system('clear')
elif platform.system()=='windows':
		try:
			import colorama
			colorama.init(autoreset=True)
		except ImportError:
			#print("虎年大吉,新年快乐!")
			#time.sleep(1)
			print("""公告:1.联系lwb@sycc1.tk获取账号密码，或者在b站关注我
							2.sycc运行
							3.get-pip下载pip""")
			time.sleep(2)
			os.system('cls')
else:
		print('系统暂不支持，请联系lwb@sycc1.tk并获取使用方法')
		time.sleep(1.5)
		#sys.exit('新年快乐')
		
	
	

  
__Author__ = "神秘的·"
__project_start_time__ = "2020"
__date_end_time__ = "2021/11"
HERE = os.path.abspath(os.path.dirname(__file__))
print("\n\n| " + "PATH::README.rst:", HERE + " |\n\n")
with open(os.path.join(HERE, "README.rst")) as rst:
    R = rst.read()
setup(
    name="sycc",  # sycc
    py_modules=["sycc", "core", "__init__", "v","pip_check/get_pip",""],
    version="0.8.2",
    description="虹源三式(一个有技术含量的四圆计算器)",  # 原
    long_description=R,
    classifiers=[
        "Natural Language :: Chinese (Simplified)",
        "Development Status :: 6 - Mature",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Android",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Terminals",
        "Topic :: System :: Shells",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
    ],
    keywords=[
        "sycc",
        "3y",
        "a_3y",
        "Circle",
        "圆",
        "圆柱",
        "圆环",
        "py",
        "Chinese",
        "ycc",
        "python",
        "windows",
        "linux",
        "3",
        "y",
        "yh",
        "yz",
        "qt",
        "4",
        "4y",
        "计算器",
        "Calculator",
        "edu",
    ],  # 关键字
    author=__Author__,
    author_email="lwb29@qq.com",
    url="https://sycc1.tk",
    license="SYCC license",
    packages=["p", "k", "e", "colorama", "p/tqdm","pip_check"],
    python_requires=">=3.6",
    install_requires=["netifaces>=0.11.0", "sycc>=0.7.0","pip"],
    entry_points={
        "console_scripts": [
            "sycc = sycc:main",
            "get-pip = pip_check.get_pip:main",
        ]
    },
    project_urls={
        "github": "https://github.com/py-lwb/sycc",
        "pypi": "https://pypi.org/project/sycc/",
        "home": "https://project.sycc1.tk"
    },
    include_package_data=True,
    zip_safe=True,
)


