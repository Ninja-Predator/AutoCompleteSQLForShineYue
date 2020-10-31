# -*- coding: UTF-8 -*-

import win32clipboard
import win32con


def format_sql():
    try:
        p = "Preparing: "
        ps = "Parameters: "
        finalSQL = ""

        clipboard = get_clipboard()
        lines = clipboard.split('\n')
        for line in lines:
            if p in line:
                PSQL = line.split(p)[-1].split('?')
            elif ps in line:
                Parameters = line.split(ps)[-1].split('), ')
        state = "从剪贴板取"
        complete_sql(PSQL, Parameters, finalSQL, state)

    except UnboundLocalError:
        print("剪贴板中没有发现东西哦")
        try:
            f = open("sql.txt", "r", encoding="utf-8")
            for line in f:
                if p in line:
                    PSQL = line.split(p)[-1].split('?')
                elif ps in line:
                    Parameters = line.split(ps)[-1].split('), ')
            f.close()
            state = "从文件中取"
            complete_sql(PSQL, Parameters, finalSQL, state)
        except FileNotFoundError:
            print("文件也妹找到。需要用文件功能的话，将需要拼接的语句放在同目录下的sql.txt中")


def complete_sql(psql, parameters, final_sql, state):
    if len(psql) != len(parameters) + 1:
        print("拆分长度出错")
        print("SQL长度: ", len(psql))
        print("参数长度: ", len(parameters))
        print("是", state, "的哦")
    else:
        final_sql += psql[0]
        for index, ParameterW in enumerate(parameters):
            Parameter = ParameterW[:ParameterW.rfind('(')]
            St = ParameterW.split('(')[-1]
            if 'String' in St:
                Parameter = '\'' + Parameter + '\''
            final_sql += Parameter
            final_sql += psql[index + 1]
        final_sql = final_sql.rstrip('\r')
        final_sql = final_sql.rstrip('\n')
        final_sql = final_sql.rstrip(' ')
        final_sql += ';'
        print(final_sql)
        print("是", state, "的哦")
        set_clipboard(final_sql)


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
