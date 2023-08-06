import re
import json

tranlist = [
    {
        "se": "re",
        "re": "name '(.*)' is not defined",
        "t": "名字 '%s' 未被定义"
    },
    {
        "se": "re",
        "re":"SyntaxError: invalid syntax",
        "t":"语法错误: 无效的语法"
    },
    {
        "se": "re",
        "re":"SyntaxError: '(.*)' outside function",
        "t":"语法错误: '%s' 在函数外运行"
    },
    {
        "se": "re",
        "re":"AttributeError: type object '(.*)' has no attribute '(.*)'",
        "t":"属性错误: 类型对象 '%s' 没有属性 '%s'"
    },
    {
        "se": "startwithreplace",
        "re":"expected an indented block after class definition on line ",
        "t":"定义类后需要一个缩进块"
    },{
        "se":"startwithreplace",
        "re":"expected an indented block after function definition on line ",
        "t":"定义函数后需要一个缩进块"
    },{
        "se":"startwithreplace",
        "re":"invalid syntax",
        "t":"无效的语法"
    },{
        "se":"re",
        "re":"expected '(.*)'",
        "t":"需要 '%s'"
    },{
        "se":"re",
        "re":"invalid character '(.*)'",
        "t":"无效字符 '%s'"
    },{
        "se":"re",
        "re":"unexpected '(.*)'",
        "t":"不应该出现 '%s'"
    },{
        "se":"startwithreplace",
        "re":"unexpected EOF while parsing",
        "t":"解析时遇到了意外的结束符"
    },{
        "se":"startwithreplace",
        "re":"unterminated string literal",
        "t":"无法结束的字符串"
    },{
        "se":"re",
        "re":"'(.*)' was never closed",
        "t":"'%s' 没有被关闭"
    },{
        "se":"re",
        "re":"unmatched '(.*)'",
        "t":"'%s' 没有匹配"
    },{
        "se":"startwithreplace",
        "re":"list index out of range",
        "t":"列表索引超出范围"
    }
]

def tran(err:str)->str:

    for v in tranlist:
        isre,re_,tran_=v["se"],v["re"],v["t"]
        if re_ == err:
            return tran_
    for v in tranlist:
        isre,re_,tran_=v["se"],v["re"],v["t"]
        if isre=="re":
            eee=re.findall(re_,err)
            if len(eee)==1:
                return tran_ % eee[0]
        elif isre=="startwithreplace":
            if err.startswith(re_):
                return tran_
    return err

def main():
    i=input("请输入错误代码：")
    print(tran(i))

if __name__ == '__main__':
    main()