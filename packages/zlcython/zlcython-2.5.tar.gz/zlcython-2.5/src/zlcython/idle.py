from contextlib import redirect_stdout
import subprocess as subp
import io
import tkinter
import time
import zlcython as zlcytran
import json
import tkinter.filedialog as tkf
import runzlcython
import zlcython
import opencc
import random
import errentozh

lucasicon = """"""''""''""'\n╭─| ~/Desktop/zlcy |───────────────────────────| ✔ |  at 00:00:00  |─╮\n╰─ /usr/local/bin/python3 /Users/lucas/Desktop/zlcy/idle.py         ─╯'
lucasname = "lucas"  # '╔╗   \n║║   \n║║   \n║║ ╔╗\n║╚═╝║\n╚═══╝\n╔╗ ╔╗\n║║ ║║\n║║ ║║\n║║ ║║\n║╚═╝║\n╚═══╝\n╔═══╗\n║╔═╗║\n║║ ╚╝\n║║ ╔╗\n║╚═╝║\n╚═══╝\n╔═══╗\n║╔═╗║\n║║ ║║\n║╚═╝║\n║╔═╗║\n╚╝ ╚╝\n╔═══╗\n║╔═╗║\n║╚══╗\n╚══╗║\n║╚═╝║\n╚═══╝\n'

year = time.strftime("%Y")


class TkGuiApp(object):  # class _main
    def __init__(self, errorl=0, l=1, debugmode=False) -> None:  # class _main
        import tkinter as tk  # import random,sys,tkinter as tk
        from tkinter import simpledialog  # from tkinter import simpledialog
        from tkinter import messagebox  # from tkinter import messagebox
        self.tk = tk
        self.messagebox = messagebox
        self.simpledialog = simpledialog

    def init(self):
        self.root = self.tk.Tk()
        self.root.withdraw()

    def inputbox(self, text):
        return self.simpledialog.askstring('quiz', text)  # askstring quiz text

    def mbox(self, text):  # mbox
        self.messagebox.showinfo('message', text)

    def yesnobox(self, text):
        return self.messagebox.askyesno('message', text)


open_window = []


def blankfunc(*args, **kwargs): pass


app = TkGuiApp()
app.init()
# XXX################################################################   M A I N
# XXX################################################################   R U N  C O D E


def get_random(length):
    randomstr = ''
    for i in range(length):
        randomstr += random.choice(
            '1234567890-=qwertyuiop[]\\`asdfghjkl;\'zxcvbnm,.\~!@#$%^&*()_+|}{POIUYTREWQ":LKJHGFDSA?><MNBVCXZ}')
    return randomstr


def runcode(tktextclass):
    app.mbox('正在开发...')
    return
    outcode = runzlcython.runcode(code.get('1.0', 'end'))
    if outcode == '<err_exit.err>':
        app.mbox('出现错误，请检查代码')
    else:
        runcodeonroot(outcode)


def codezlcy(tktextclass, path=None):
    if path == None:
        path_ = tkf.asksaveasfilename(title='保存文件', filetypes=[
            ('Zlcython源文件', '*.py')])
    else:
        path_ = path
    encodefile = path_+('.py' if path_[-3:] != '.py' else '')
    code = tktextclass.get('1.0', 'end').split('\n')
    cc = opencc.OpenCC('t2s')
    decodecode = ''
    libusedict = {"urllib_request": [False, "import urllib.request as get__"],
                  "random": [False, "import random"],
                  "time": [False, "import time"],
                  "threading": [False, "from threading import Thread"],
                  "_": [False, ""]
                  }
    printonroot('')
    printonroot('='*10+'转换代码'+'='*10)
    for linenum in range(len(code)):
        jghfkaghdbjv, libusedict, out__, exit__ = zlcython.zlcytopy(
            code[linenum], linenum, libusedict)
        if exit__:
            exit()
        printonroot(out__)
        decodecode += jghfkaghdbjv
    with open(encodefile, mode="w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("#!python3"+"\n"*3)
        for lib, info in libusedict.items():
            if info[0]:
                f.write(info[1]+'\n')
        f.write(decodecode)
        f.write("\n"*2)
    printonroot("编译完成！\n输出文件："+encodefile)
    printonroot('\n退出。\ncode：0')
    shell.nextline()


def check_exit():
    global open_window
    if len(open_window) == 0:
        exit()


def add_right_click_menu(win):
    f = tkinter.Menu(win, tearoff=False)
    f1 = tkinter.Menu(f, tearoff=False)
    f2 = tkinter.Menu(f, tearoff=False)
    f1.add_command(label='新建', command=lambda: new_file())
    f1.add_command(label='打开', command=lambda: open_file())
    f.add_cascade(label='文件', menu=f1)
    f.add_cascade(label='关于', command=lambda: app.mbox(
        f'zlcython shell\n作者：lucas z\n版本：1.0.0\n更新日期：2022-01-28\nCopyright © {year} {lucasname}. All rights reserved.'))

    def xShowMenu(event):
        f.post(event.x_root, event.y_root)   # #将菜单条绑定上事件，坐标为x和y的root位置
    win.bind("<Button-3>", xShowMenu)     # #设定鼠标右键触发事件，调用xShowMenu方法

# XXX # R U N  C O D E  E N D
# XXX # N E W  F I L E


def new_file():
    def save_file(code):
        code = code.get('1.0', 'end')
        out = tkf.asksaveasfilename(title='保存文件', filetypes=[
                                    ('Zlcython源文件', '*.zlcy'), ('所有文件', '*')])+'.zlcy'
        if out:
            with open(out, 'w', encoding='utf-8') as f:
                f.write(code)
        else:
            pass
    newfilwwindow = tkinter.Tk()
    add_right_click_menu(newfilwwindow)
    open_window.append('new')
    newfilwwindow.title('zlcython idle')
    newfilwwindow.geometry('600x800')
    newfilwwindow.resizable(width=False, height=False)
    f = tkinter.Menu(newfilwwindow)
    newfilwwindow['menu'] = f
    f1 = tkinter.Menu(f, tearoff=False)
    f2 = tkinter.Menu(f, tearoff=False)
    f1.add_command(label='新建', command=lambda: new_file())
    f1.add_command(label='打开', command=lambda: open_file())
    f1.add_command(label='保存', command=lambda: save_file(nfwcode))
    f1.add_command(label='退出', command=lambda: newfilwwindow.destroy())
    f.add_cascade(label='文件', menu=f1)
    f.add_cascade(label='关于', command=lambda: app.mbox(
        f'zlcython shell\n作者：lucas z\n版本：1.0.0\n更新日期：2022-01-28\nCopyright © {year} {lucasname}. All rights reserved.'))
    newfilwwindow.protocol("WM_DELETE_WINDOW", lambda: newc(newfilwwindow))
    nfwcode = tkinter.Text(newfilwwindow, width=600, height=800)
    nfwcode.pack()
    newfilwwindow.mainloop()
# XXX # N E W  F I L E  E N D
# XXX # O P E N  F I L E


def open_file():
    open_window.append('open')

    def save_file(code):
        code = code.get('1.0', 'end')
        out = tkf.asksaveasfilename(title='保存文件', filetypes=[
                                    ('Zlcython源文件', '*.zlcy'), ('所有文件', '*')])+'.zlcy'
        if out:
            with open(out, 'w', encoding='utf-8') as f:
                f.write(code)
        else:
            pass

    def lsave_file(code, file_name):
        code = code.get('1.0', 'end')
        out = file_name
        if out:
            with open(out, 'w', encoding='utf-8') as f:
                f.write(code)
        else:
            pass
    openfilwwindow = tkinter.Tk()
    add_right_click_menu(openfilwwindow)
    openfilwwindow.title('zlcython idle')
    openfilwwindow.geometry('600x800')
    openfilwwindow.resizable(width=False, height=False)
    f = tkinter.Menu(openfilwwindow)
    openfilwwindow['menu'] = f
    f1 = tkinter.Menu(f, tearoff=False)
    f2 = tkinter.Menu(f, tearoff=False)
    f1.add_command(label='新建', command=lambda: new_file())
    f1.add_command(label='打开', command=lambda: open_file())
    f1.add_separator()
    f1.add_command(label='保存', command=lambda: lsave_file(
        nfwcode, file_name=file_name))
    f1.add_command(label='另存为', command=lambda: save_file(nfwcode))
    f2.add_command(label='运行', command=lambda: runcode(nfwcode))
    f2.add_command(label='编译', command=lambda: codezlcy(nfwcode))
    f.add_cascade(label='文件', menu=f1)
    f.add_cascade(label='代码', menu=f2)
    f.add_cascade(label='关于', command=lambda: app.mbox(
        f'zlcython shell\n作者：lucas z\n版本：1.0.0\n更新日期：2022-01-28\nCopyright © {year} {lucasname}. All rights reserved.'))
    filetypes = [('Zlcython源文件', '*.zlcy'), ('所有文件', '*')]
    file_name = tkf.askopenfilename(
        title='选择文件', filetypes=filetypes, initialdir='./')
    openfilwwindow.protocol("WM_DELETE_WINDOW", lambda: openc(openfilwwindow))
    if file_name != '':
        with open(file_name, 'r', encoding='utf-8') as f:
            nfwcode = tkinter.Text(openfilwwindow, width=600, height=800)
            nfwcode.pack()
            nfwcode.insert('1.0', f.read())
        openfilwwindow.mainloop()
    else:
        openfilwwindow.withdraw()


# XXX # O P E N  F I L E  E N D
# XXX # TODO
#                                                     #        #        #######      ###     ####        ###       #
# TODO:                                               #      #             #       ##   ##   ##  ##    ##   ##     #
#     1. 滚动条    ×                                  #    ###########     #     ##     ##  ##    ##  ##     ##    #
#     2. 右键菜单  √                                  #      #             #      ##   ##   ##   ##    ##   ##     #
#                                                    #        #           #        ###     #####        ###       #
# XXX # TODO  E N D
# XXX # L O A D   F I L E
libusedict = {"urllib_request": [False, "import urllib.request as get__"],
    "random": [False, "import random"],
    "time": [False, "import time"],
    "threading": [False, "from threading import Thread"],
    "_": [False, ""]
}
# XXX # L O A D   F I L E  E N D
# XXX#XXX############################################################  M E N U
root = tkinter.Tk()
root.title('zlcython shell')
root.geometry('600x800')
root.resizable(width=False, height=False)
add_right_click_menu(root)
open_window.append('root')
f = tkinter.Menu(root)
root['menu'] = f
f1 = tkinter.Menu(f, tearoff=False)
f2 = tkinter.Menu(f, tearoff=False)
f1.add_command(label='新建', command=lambda: new_file())
f1.add_command(label='打开', command=lambda: open_file())
f.add_cascade(label='文件', menu=f1)
f.add_cascade(label='关于', command=lambda: app.mbox(
    f'zlcython shell\n作者：lucas z\n版本：1.0.0\n更新日期：2022-01-28\nCopyright © {year} {lucasname}. All rights reserved.'))
# XXX M E N U  E N D

# XXX#XXX############################################################  S H E L L


class Shell(tkinter.Text):
    def __init__(self, parent, **kwargs):
        tkinter.Text.__init__(self, parent, **kwargs)
        # setup handler to process pressed keys
        self.bind('<Key>', self.on_key)
        self.cmd = None        # hold the last command issued
        self.show_prompt()
    # to append given text at the end of Text box

    def insert_text(self, txt='', end='\n'):
        self.insert(tkinter.END, txt+end)
        self.see(tkinter.END)  # make sure it is visible

    def show_prompt(self):
        self.insert_text('>> ', end='')
        # make sure the input cursor is at the end
        self.mark_set(tkinter.ALL, tkinter.END)
        self.cursor = self.index(tkinter.INSERT)  # save the input position
    # handler to process keyboard input

    def on_key(self, event):
        # print(event)
        if event.keysym == 'Up':
            if self.cmd:
                # show the last command
                self.delete(self.cursor, tkinter.END)
                self.insert(self.cursor, self.cmd)
            return "break"  # disable the default handling of up key
        if event.keysym == 'Down':
            return "break"  # disable the default handling of down key
        if event.keysym in ('Left', 'BackSpace'):
            # get the current position of the input cursor
            current = self.index(tkinter.INSERT)
            if self.compare(current, '==', self.cursor):
                # if input cursor is at the beginning of input (after the prompt), do nothing
                return "break"
        if event.keysym == 'Return':
            # extract the command input
            cmd = self.get(self.cursor, tkinter.END).strip()
            self.insert_text()  # advance to next line
            if cmd.startswith('`'):
                # it is an external command
                self.system(cmd)
            else:
                # it is python statement
                self.execute(cmd)
            self.show_prompt()
            return "break"  # disable the default handling of Enter key
        if event.keysym == 'Escape':
            self.master.destroy()  # quit the shell
    # function to handle python statement input

    def execute(self, cmd):
        self.cmd = cmd  # save the command
        # use redirect_stdout() to capture the output of exec() to a string
        f = io.StringIO()
        with redirect_stdout(f):
            try:
                # self.cmd
                if cmd[-1] == ":" or cmd[-1] == "：":
                    print("暂不支持类和函数的定义。")
                else:
                    code__ = zlcytran.zlcytopy(self.cmd, 0, libusedict)
                    exec(code__[0] if code__[0] !=
                         '' else 'print("",end="")', globals())
            except Exception as e:
                print(errentozh.tran(str(e).replace('<string>', '<zlcython_idle_input>').replace(
                    ", line 1", ", line <input.length>").replace("line 1", "<zlcython_idle_input>")))
        # then append the output of exec() in the Text box
        self.insert_text(f.getvalue(), end='')
    # function to handle external command input

    def system(self, cmd):
        self.cmd = cmd  # save the command
        try:
            # extract the actual command
            cmd = cmd[cmd.index('`')+1:cmd.rindex('`')]
            proc = subp.Popen(cmd, stdout=subp.PIPE,
                              stderr=subp.PIPE, text=True)
            stdout, stderr = proc.communicate(5)  # get the command output
            # append the command output to Text box
            self.insert_text(stdout)
        except Exception as e:
            self.insert_text(str(e))

    def printout(self, *text):
        f = io.StringIO()
        with redirect_stdout(f):
            print(*text)
        self.insert_text(f.getvalue(), end='')

    def nextline(self):
        self.insert_text()
        self.show_prompt()

    def runcodeonroot(self, code):
        self.insert_text('\n'*2)
        self.insert_text('='*10+'RUN CODE'+'='*10+'')
        f = io.StringIO()
        with redirect_stdout(f):
            try:
                exec(code)
            except Exception as e:
                print(str(e).replace('<string>', '<zlcython_idle_input>'))
        self.insert_text(f.getvalue(), end='')
        self.insert_text('='*10+'RUN CODE END'+'='*10+'')
        self.insert_text('\n'*2)
        self.show_prompt()


shell = Shell(root, width=100, height=50, font=('Consolas', 10))
shell.pack(fill=tkinter.BOTH, expand=1)
shell.focus_set()
# XXX S H E L L  E N D
# XXX M A I N   E N D


def runcodeonroot(pythoncode):
    root.wm_attributes('-topmost', 1)  # 锁定窗口置顶
    root.wm_attributes('-topmost', 0)  # 释放窗口置顶
    shell.runcodeonroot(pythoncode)


def printonroot(text):
    root.wm_attributes('-topmost', 1)  # 锁定窗口置顶
    root.wm_attributes('-topmost', 0)  # 释放窗口置顶
    shell.printout(text)


def rootc(win):
    win.withdraw()
    open_window.remove('root')
    check_exit()


def openc(win):
    win.withdraw()
    open_window.remove('open')
    check_exit()


def newc(win):
    win.withdraw()
    open_window.remove('new')
    check_exit()


root.protocol("WM_DELETE_WINDOW", lambda: rootc(root))
# app.mbox(f'zlcython shell\n作者：lucas z\n版本：1.0.0\n更新日期：2022-01-28\nCopyright © {year} {lucasname}. All rights reserved.')
print(lucasicon)
root.mainloop()
