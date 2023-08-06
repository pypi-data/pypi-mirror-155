# -*- coding: utf-8 -*-
#!python3


#!/bin/python3
# pip install opencc-python-reimplemented
import sys,zlcython,json
import opencc
cc = opencc.OpenCC('t2s')

libusedict = {"urllib_request": [False, "import urllib.request as get__"],
    "random": [False, "import random"],
    "time": [False, "import time"],
    "threading": [False, "from threading import Thread"],
    "_": [False, ""]
}
def zlcytopypn(_code:str,libusedict=libusedict)->str:
    decodecode = ''
    code = []
    for i in _code:
        code.append(cc.convert(i))
    for linenum in range(len(code)):
        jghfkaghdbjv,libusedict,out__,exit__=zlcython.zlcytopy(code[linenum],linenum,libusedict)
        if exit__:exit()
        print(out__)
        decodecode+=jghfkaghdbjv
    return decodecode,libusedict,out__,exit__
def main():
    global libusedict
    # print(sys.argv) #debug
    codefile = sys.argv[-1]
    if codefile == 'zlcython' or codefile.endswith("__main__.py"):
        print('错误：请输入代码文件名！')
        return
    encodefile = codefile.replace(".zlcy", ".py")
    decodecode = ''
    code = []
    with open(codefile, encoding="utf-8") as f:
        _code = f.readlines()
        for i in _code:
            code.append(cc.convert(i))
    for linenum in range(len(code)):
        jghfkaghdbjv,libusedict,out__,exit__=zlcython.zlcytopy(code[linenum],linenum,libusedict)
        if exit__:exit()
        if out__!='':print(out__)
        decodecode+=jghfkaghdbjv
    with open(encodefile, mode="w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("#!python3"+"\n"*3)
        for lib, info in libusedict.items():
            if info[0]:
                f.write(info[1]+'\n')
        f.write(decodecode)
        f.write("\n"*2)
    print("编译完成！\n文件:"+encodefile)
    print('\n退出.code:0')
if __name__ == "__main__":
    main()


