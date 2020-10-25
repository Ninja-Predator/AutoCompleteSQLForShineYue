# -*- coding: UTF-8 -*-


def formatSql():
    try:
        f = open("sql.txt", "r", encoding="utf-8")
        p = "Preparing: "
        ps = "Parameters: "
        finalSQL = ""
        for line in f:
            if p in line:
                PSQL = line.split(p)[-1].split('?')
            elif ps in line:
                Parameters = line.split(ps)[-1].split('),')
        f.close()
        if len(PSQL) != len(Parameters) + 1:
            print("拆分长度出错")
            print("SQL长度: ", len(PSQL))
            print("参数长度", len(Parameters))
        else:
            finalSQL += PSQL[0]
            for index, ParameterW in enumerate(Parameters):
                Parameter = ParameterW[:ParameterW.rfind('(')]
                St = ParameterW.split('(')[-1]
                if St == 'String':
                    Parameter = '\'' + Parameter + '\''
                finalSQL += Parameter
                finalSQL += PSQL[index + 1]
            print(finalSQL)
    except FileNotFoundError:
        print("将需要拼接的语句放在同目录下的sql.txt中")


if __name__ == '__main__':
    formatSql()
    print("按下回车结束程序")
    input()
