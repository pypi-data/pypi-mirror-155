try:
    from core import *
    if __name__=='__main__':
    	main()
except Exception as sycc_error:
    print('sycc Error:',sycc_error)