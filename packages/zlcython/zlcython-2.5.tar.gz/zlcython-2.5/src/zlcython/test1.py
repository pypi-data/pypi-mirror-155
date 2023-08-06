# -*- coding: utf-8 -*-
#!python3


if True:
    if True:
        def a():
            print('a')
if True:
    if True:
        from tkinter import *
        window=Tk()
        def 图形化标题(title):
            window.title(title)
        def 图形化窗口大小(width,height):
            window.geometry(str(width)+"x"+str(height))
        def 显示窗口():
            window.mainloop()
        def 显示文本(text,x=0,y=0):
            l=Label(window,text=text)
            l.place(x=x,y=y)
            return l
        def 显示文本框(text,x=0,y=0,width=None,height=None):
            e=Entry(window,text=text,width=width,height=height)
            e.place(x=x,y=y)
            return e
        def 显示按钮(text,command,x=0,y=0,width=None,height=None):
            b=Button(window,text=text,width=width,height=height,command=command)
            b.place(x=x,y=y)
            return b
        def 当窗口关闭时(command):
            def func():
                command()
                try:
                    window.destroy()
                except:pass
            window.protocol("WM_DELETE_WINDOW",func)
        def 图形化窗口位置(x,y):
            window.geometry("+"+str(x)+"+"+str(y))
        def 刷新窗口():
            window.update()
        
        图形化标题('标题')
        图形化窗口大小(300,300)
        显示按钮('a',a)
        当窗口关闭时(a)
        显示窗口()


