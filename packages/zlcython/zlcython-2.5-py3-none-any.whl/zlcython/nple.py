import json,zlcython,errentozh
libusedict = {"urllib_request": [False, "import urllib.request as get__"],
    "random": [False, "import random"],
    "time": [False, "import time"],
    "threading": [False, "from threading import Thread"],
    "_": [False, ""]
}
zlcython='''Zlcython 2.2.0 (tags/v2.2.0)
Type ".exit" or press Control+C to exit.
Copyright (c) 2022, LucasZ228.
All rights reserved.'''
allfuncandclass=''
print(zlcython)
exit_=False
code=''
# notrun=False
while True:
    try:
        while True:
            incode=(input('>>>')+'\n')
            if incode=='.exit':raise SystemExit
            if incode=='':continue
            # if incode[-1]==":" or incode[-1]=="：":
            #         print("暂不支持类和函数的定义。")
            #         continue
            if False:
                pass
            else:
                if incode[-2]==":" or incode[-2]=="：":
                    code__='something'
                    while code__!='':
                        code__=input('...')
                        incode+=(code__+'\n')
                        # exit()
                code_,libusedict,out,tmp=zlcython.zlcytopypn(incode,libusedict)
                code=code_
                if out!='':
                    print(out)
                    continue
                if not False:#notrun:
                    runcode= (allfuncandclass+'\n'+code) if code != '' else 'print("",end="")'
                    # notrun=False
                    exec(runcode)
                    code=''
    except KeyboardInterrupt or SystemExit:
        print('\nexit')
        exit_=True
    except Exception as e:
        e=str(e)
        print(errentozh.tran(e))
    if exit_:break