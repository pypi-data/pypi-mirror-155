import os
import sys
import tty
import termios
 
'''
Enter:  13
Back:   127
?:      63
C-h:    8
C-w:    23
Tab:    9
C-u:    21
C-c:    3
C-d:    4
C-\:    28
SPACE:  32
'''
 
CLI_KEY_CNCR  = 13
CLI_KEY_BACK  = 127
CLI_KEY_QMARK = 63
CLI_KEY_CTRLH = 8
CLI_KEY_CTRLW = 23
CLI_KEY_TAB   = 9
CLI_KEY_CTRLU = 21
CLI_KEY_CTRLC = 3
CLI_KEY_CTRLD = 4
CLI_KEY_QUIT  = 28
CLI_KEY_SPACE = 32
CLI_KEY_TABLEN = 4
 
class CLI(object):
    def __init__(self):
        self.line = ''
        self.line_complete = ''
        self.completer_on = False
        self.completer_dict = {}
        self.completer_dict_keys = self.completer_dict.keys()
        self.completer_id = 0
        self.completer_cnt = len(self.completer_dict)
    def getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    def completer_kw_update(self):
        self.completer_dict_keys = self.completer_dict.keys()
        self.completer_dict_keys.sort()
        self.completer_cnt = len(self.completer_dict)
    def completer_kw_add(self, key, word):
        self.completer_dict[key] = word
        self.completer_kw_update()
    def completer_kw_clear(self):
        self.completer_dict.clear()
        self.completer_id_update()
    def completer_id_update(self):
        self.completer_kw_update()
        if self.completer_id < self.completer_cnt - 1:
            self.completer_id += 1
        else:
            self.completer_id = 0
    def completer_wd_select(self, word):
        if not word:
            return ''
        cnt = self.completer_cnt
        while cnt>0:
            completer = self.completer_dict_keys[self.completer_id]
            self.completer_id_update()
            cnt -= 1
            if word == completer[:len(word)]:
                return completer[len(word):]
        return ''
    def printf(self, info=''):
        sys.stdout.write(info)
    def show_spec_len_str(self, info, maxlen, spacech=' '):
        'display a string of the specified length'
        maxlen = maxlen
        infolen = len(info)
        if maxlen < infolen:
            maxlen = infolen
        while infolen>0:
            ch = info[-infolen]
            for i in range(self.char_memory_len(ch)):
                self.printf(info[i-infolen])
            infolen -= self.char_memory_len(ch)
            maxlen -= self.char_display_len(ch)
        while maxlen>0:
            self.printf(spacech)
            maxlen -= self.char_display_len(spacech)
    def show_help_info(self):
        if self.completer_on:
            line = self.line_complete
        else:
            line = self.line
        lastwd = ''
        show_all = False
        if not line or line[-1] == ' ':
            show_all = True
        else:
            lastwd = line.split()[-1]
        if self.completer_dict:
            maxlen = max([len(info) for info in self.completer_dict])
        else:
            maxlen = 12
        for info in self.completer_dict:
            if show_all or lastwd == info[:len(lastwd)]:
                self.printf(' ')
                self.show_spec_len_str(info, maxlen)
                self.printf(' ')
                self.printf(self.completer_dict[info])
                self.printf('\r\n')
    def is_chinese_char(self, ch):
        return ord(ch) > 127
    def char_display_len(self, ch):
        if self.is_chinese_char(ch):
            return 2
        elif ord(ch) == CLI_KEY_TAB:
            return CLI_KEY_TABLEN
        else:
            return 1
    def char_memory_len(self, ch):
        if self.is_chinese_char(ch):
            return 3
        else:
            return 1
    def rm_last_char(self, line):
        lastch = ''
        rmlen = 0
        if len(line)>0:
            lastch = line[-1]
            self.printf('\b \b' * self.char_display_len(lastch))
            rmlen = self.char_memory_len(lastch)
            if len(line) >= rmlen:
                line = line[:-(rmlen)]
            else:
                rmlen = len(line)
                line = ''
        return rmlen, line
    def rm_last_word(self, line):
        lastwd = ''
        linelen = len(line)
        rspacelen = linelen - len(line.rstrip())
        if not linelen:
            return line
        lastwd = line.split()[-1]
        backlen = len(lastwd) + rspacelen
        rmlen = 0
        while backlen>0 and line:
            rmlen, line = self.rm_last_char(line)
            backlen -= rmlen
        return line
    def rm_one_line(self, line):
        rmlen = 0
        while line:
            rmlen, line = self.rm_last_char(line)
        return line
    def do_line_complete_proc(self):
        line = self.line
        line_complete = self.line_complete
        lastwd = ''
        self.printf('\r\n')
        if self.line_complete:
            self.printf(self.line_complete)
        else:
            self.printf(self.line)
        if not line:
            return line
        lastwd = line.split()[-1]
        completer = self.completer_wd_select(lastwd)
        if not completer.strip():
            self.line_complete = line
            return line
        backlen = len(line_complete) - len(line)
        while backlen>0 and line_complete:
            rmlen, line_complete = self.rm_last_char(line_complete)
            backlen -= rmlen
        self.printf(completer)
        line_complete = line + completer
        self.line_complete = line_complete
    def do_line_complete_end(self):
        if self.completer_on:
            self.line = self.line_complete
            self.line_complete = ''
            self.completer_on = False
    def get_line(self):
        self.line = ''
        self.line_complete = ''
        self.completer_on = False
        while True:
            ch = self.getch()
            if ch == '\r' or ch == '\n':
                self.do_line_complete_end()
                self.printf('\r\n')
                break
            elif ord(ch) == CLI_KEY_BACK or ord(ch) == CLI_KEY_CTRLH:
                if self.completer_on:
                    rmlen, self.line_complete = self.rm_last_char(self.line_complete)
                else:
                    rmlen, self.line = self.rm_last_char(self.line)
                self.do_line_complete_end()
            elif ord(ch) == CLI_KEY_QMARK:
                self.printf('?')
                self.printf('\r\n')
                self.show_help_info()
                if self.completer_on:
                    self.printf(self.line_complete)
                else:
                    self.printf(self.line)
            elif ord(ch) == CLI_KEY_CTRLW:
                if self.completer_on:
                    self.line_complete = self.rm_last_word(self.line_complete)
                else:
                    self.line = self.rm_last_word(self.line)
                self.do_line_complete_end()
            elif ord(ch) == CLI_KEY_TAB:
                self.completer_on = True
                self.do_line_complete_proc()
            elif ord(ch) == CLI_KEY_CTRLD:
                if self.line:
                    return self.line
                else:
                    return ch
            elif ord(ch) == CLI_KEY_QUIT:
                self.printf('\r\n Interrupted by <Ctrl-\>.\r\n')
                sys.exit()
            elif ord(ch) == CLI_KEY_CTRLU:
                if self.completer_on:
                    self.line_complete = self.rm_one_line(self.line_complete)
                else:
                    self.line = self.rm_one_line(self.line)
                self.do_line_complete_end()
            elif ord(ch) == CLI_KEY_SPACE:
                self.printf(ch)
                if self.completer_on:
                    self.line_complete += ch
                else:
                    self.line += ch
            else:
                self.printf(ch)
                self.do_line_complete_end()
                self.line += ch
                # chinese qmask proc
                if ord(ch) == 159 and len(self.line)>= 3 and self.line[-3:] == '\xef\xbc\x9f':
                    self.printf('\r\n')
                    self.line = self.line[:-3]
                    self.show_help_info()
                    self.printf(self.line)
        return self.line
    def get_raw_line(self):
        self.raw_line = ''
        while True:
            ch = self.getch()
            if ch == '\r' or ch == '\n':
                self.printf('\r\n')
                break
            elif ord(ch) == CLI_KEY_BACK or ord(ch) == CLI_KEY_CTRLH:
                rmlen, self.raw_line = self.rm_last_char(self.raw_line)
            elif ord(ch) == CLI_KEY_CTRLW:
                self.raw_line = self.rm_last_word(self.raw_line)
            elif ord(ch) == CLI_KEY_TAB:
                self.printf(' ' * self.char_display_len(ch))
                self.raw_line += ch
            elif ord(ch) == CLI_KEY_CTRLD:
                if self.raw_line:
                    return self.raw_line
                else:
                    return ch
            elif ord(ch) == CLI_KEY_QUIT:
                self.printf('\r\n Interrupted by <Ctrl-\>.\r\n')
                sys.exit()
            elif ord(ch) == CLI_KEY_CTRLU:
                self.raw_line = self.rm_one_line(self.raw_line)
            else:
                self.raw_line += ch
                self.printf(ch)
        return self.raw_line
 
def test():
    cli = CLI()
    help_info = {
    	'hello0':     'say hello 0',
    	'hello1':     'say hello 1',
    	'hellohello': 'say hello hello',
    	'hellohehe':  'say hello hehe',
    	'hellohi':    'say hello hi'
    	}
    for key in help_info:
        cli.completer_kw_add(key, help_info[key])
    while True:
        line = cli.get_line()
        if len(line) == 1 and ord(line[0]) == CLI_KEY_CTRLD:
            break
        if line == 'quit':
            break
        print(line)
 
if __name__ == "__main__": 
    test()