# -*- coding: UTF-8 -*-
from pathlib import Path

import win32clipboard
import win32con


def format_sql():
    try:
        my_file = Path("sql.txt")
        p = "Preparing: "
        ps = "Parameters: "
        finalSQL = ""
        state = "啥都没有"
        if not my_file.exists():
            clipboard = get_clipboard()
            lines = clipboard.split('\n')
            for line in lines:
                if p in line:
                    PSQL = line.split(p)[-1].split('?')
                elif ps in line:
                    Parameters = line.split(ps)[-1].split('), ')
            state = "从剪贴板取"
        else:
            f = open("sql.txt", "r", encoding="utf-8")
            for line in f:
                if p in line:
                    PSQL = line.split(p)[-1].split('?')
                elif ps in line:
                    Parameters = line.split(ps)[-1].split('), ')
            f.close()
            state = "从文件中取"

        if len(PSQL) != len(Parameters) + 1:
            print("拆分长度出错")
            print("SQL长度: ", len(PSQL))
            print("参数长度: ", len(Parameters))
            print("取值状态为: ", state)
        else:
            finalSQL += PSQL[0]
            for index, ParameterW in enumerate(Parameters):
                Parameter = ParameterW[:ParameterW.rfind('(')]
                St = ParameterW.split('(')[-1]
                if 'String' in St:
                    Parameter = '\'' + Parameter + '\''
                finalSQL += Parameter
                finalSQL += PSQL[index + 1]
            finalSQL.rstrip('\n')
            finalSQL += ';'
            print(finalSQL)
            print(state)
            set_clipboard(finalSQL)
    except FileNotFoundError:
        print("将需要拼接的语句放在同目录下的sql.txt中")
    except UnboundLocalError:
        print("请检查剪贴板的sql语句格式是否正确")


def get_clipboard():
    win32clipboard.OpenClipboard()
    text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return text


def set_clipboard(fin_sql):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, fin_sql)
    win32clipboard.CloseClipboard()
    print("已将内容放于剪贴板!")


if __name__ == '__main__':
    format_sql()
    print("按下回车结束程序")
    input()
