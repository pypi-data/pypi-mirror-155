import zlcython
import json
import opencc
import coderun


def runcode(codes):
    decodecode = ''
    for code in codes:
        libusedict = {"urllib_request": [False, "import urllib.request as get__"],
                      "random": [False, "import random"],
                      "time": [False, "import time"],
                      "threading": [False, "from threading import Thread"],
                      "_": [False, ""]
                      }
        for lib, info in libusedict.items():
            if info[0]:
                code = info[1]+'\n'+code
        code = opencc.OpenCC('t2s').convert(code)
        linenum = 0
        jghfkaghdbjv, libusedict, out__, exit__ = zlcython.zlcytopy(
            code, linenum, libusedict)
        if exit__:
            return '<err_exit.err>'
        decodecode += jghfkaghdbjv+'\n'
    return decodecode
