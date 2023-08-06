a="\\b(%s)\\b"
l=[]
import json
tranlist={    "输出": "print",
    "输入": "input",
    "转整数": "int",
    "转浮点数": "float",
    "转字符串": "str",
    "转布尔": "bool",
    "转列表": "list",
    "转元组": "tuple",
    "转字典": "dict",
    "转集合": "set",
    "转比特": "bytes",
    "转字节": "bytearray",    "请求网页": "get__.urlopen",
    "获取内容": "read()",
    "随机数": "random.randint",    "等待": "time.sleep",
    "长度":"len",}
for i in tranlist.keys():
    l.append(i)
out=a % "|".join(l)
# copy to clipboard
import pyperclip
pyperclip.copy(out)