"""
这是Fishconsole Project的功能模块，所有的比较强大的功能都会放在这里

----

"""

try:
    import re
    from Fishconsole import logs
    # 计时
    import datetime
    # 多线程
    import threading
    # 爬虫
    import requests
    from lxml import html

    etree = html.etree
    import os
    # Fishconsole
    from Fishconsole import fcv
    from Fishconsole import files
    # pip
    from pip._internal import main
    # email
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
except:
    logs.安全退出("Fishsys依赖包导入出错，程序无法运行")

# 导入强制更新系统所需要的内容


FI = files.缓存(2, 变量名='FI')
if FI == "error":
    FI = False
PI = files.缓存(2, 变量名='PI')
if PI == "error":
    PI = False
ZUI = files.缓存(2, 变量名='ZUI')
if ZUI == "error":
    ZUI = False


# 新建这个函数，默认情况下所有的项目都不会运行，通过传递的参数开启相应的功能（其实都一样）
def 系统日志(text, 项目名, 开启状态=False):
    """
    Fishconsole 系统日志

    ----

    :param text: 要显示的文字
    :param 项目名: 这个项目
    :param 开启状态: 每个项目的布尔值状态（由fcc决定）
    :return:
    """
    # 总开关
    if FI:
        import time
        if 开启状态:

            a = logs.颜色(
                f"Fishconsole{fcv.version()}" + "》" + f"{项目名}" + "》" + str(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                色选="紫色") + str(f":{text}")
            print(a)
        else:
            pass
            # a = logs.颜色(
            #     f"Fishconsole{version.version()}" + "》" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
            #     色选="紫色") + str(f":{text}")
            # print(a)


def 官网存活性检测(官网地址: str="http://www.baidu.com", 测试时长=15):
    """
    Fishconsole Fishsys官网存活性检测

    ----

    - 就是判断官网能不能链接，可以用来检测联网，能联返回ture，不能返回False

    :param 官网地址: 官网地址
    :return: 布尔值
    """
    import requests
    # noinspection PyBroadException
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53"
        }
        requests.get(官网地址, headers=headers, timeout=测试时长)
    except:
        return False
    return True


报警器 = False




def Fishconsole_Update():
    # 你要删我也没办法，反正如果出了什么错过了重大更新你就自己乐呵去呗
    # 这个不是模块，我们将会在导入该模块的时候顺序执行此处
    # 你可以去fcv_debug关闭强制更新而不是删代码,删了对你没有多大好处

    # 强制更新系统执行组一期

    # 判断设备是否接入网络
    global 报警器

    def isConnected():
        import requests
        # noinspection PyBroadException
        try:
            requests.get("https://pypi.org/project/Fishconsole/", timeout=7)
        except:
            global 报警器
            报警器 = True
            print(logs.日志("》强制更新系统》isConnected》官网连接失败"))

            return False
        print(logs.日志("》强制更新系统》官网连接成功"))
        return True

    UPI = files.缓存(2, 变量名="UPI")
    if UPI == "error":
        UPI = False
        temp = files.缓存(2)
        temp["UPI"] = False
        files.缓存(1, temp)

    UPI = files.缓存(2, 变量名="UPI")
    if UPI == "error":
        UPI = False
        temp = files.缓存(2)
        temp["UPI"] = False
        files.缓存(1, temp)

    updata = files.缓存(2, 变量名="updata")
    if updata == "error":
        updata = True
        temp = files.缓存(2)
        temp["updata"] = True
        files.缓存(1, temp)

    Forcedupdate = files.缓存(2, 变量名="Forcedupdate")
    if Forcedupdate == "error":
        Forcedupdate = True
        temp = files.缓存(2)
        temp["Forcedupdate"] = True
        files.缓存(1, temp)

    系统日志("获取变量", "强制更新系统", UPI)

    # 查找缓存文件
    config = files.缓存(2)
    # 如果缓存文件不存在
    if not config:
        系统日志("强制更新系统》缓存》缓存文件不存在，创建缓存文件", "强制更新系统", UPI)
        # fup的意思是Fishsys模块判断自己是否在之前检测过一次，如果检测过一次，就是修改为正，让它可
        # +以在下一次检测到版本还是低的话继续保持未检测的状态，如果成功了，那就将False修改为ture，这个fupadta是独立的
        # +而updata是helps.帮助弄过来的，它的用处就是让Fishsys执行强制更新的操作
        # 因为没有文件，所以我们在一开始就要创建文件，这个创建文件有一个规则，就是需要创建啥就写入啥，不要一股脑全写，因为这样就显得不高效
        config = {"updata": True, "fup": True, "year": 2002, "month": 6, "day": 3}
        系统日志("强制更新系统》首次运行，添加fup到缓存", "强制更新系统", UPI)
        # 提取数据，其实也是初始化首次启动时要用的变量，因为是第一次启动，所以提取的值就是首次运行的初始值
        fup = config["fup"]
        updata = config["updata"]
        year = config['year']
        # 当变量有点修改的时候我们就要进行保存，因为这样才能避免出现突如其来的故障
        files.缓存(1, config)
    else:
        # 当缓存文件存在时执行的操作
        系统日志(f"缓存文件存在，尝试读取相关信息", "强制更新系统", UPI)
        # 因为我们有文件了，我们就可以直接提取数据，但是难免会出现一些奇奇怪怪的情况，所以我们还要检测参数是否存在

        fup = config.get("fup")

        year = config.get("year")
        day = config.get("day")
        month = config.get("month")
        系统日志(f"Forcedupdate is {fup}", "强制更新系统", UPI)
        系统日志(f"fup is {fup}", "强制更新系统", UPI)
        系统日志(f"updata is {updata}", "强制更新系统", UPI)
        系统日志(f"year is {year}", "强制更新系统", UPI)

    # 确认开发者模式是否启动了强制更新，但在之前必须导入变量
    if Forcedupdate:
        if updata:
            系统日志("强制更新系统》强制更新系统启动", "强制更新系统", UPI)
            系统日志("强制更新系统》读取缓存信息", "强制更新系统", UPI)
            # 如果get到没有的内容，他就会给你返回False的布尔值
            if year and month and day is None:
                系统日志("year配置不存在，创建", "强制更新系统", UPI)
                config["year"] = 2005
                config["month"] = 6
                config["day"] = 11
                上一年 = config.get("year")
                上一月 = config.get("month")
                上一日 = config.get("day")
                files.缓存(1, config)
            else:
                上一年 = config.get("year")
                上一月 = config.get("month")
                上一日 = config.get("day")

            if updata is None:
                系统日志("updata配置不存在，创建", "强制更新系统", UPI)
                config["updata"] = True
                files.缓存(1, config)

            if fup is None:
                系统日志("fup配置不存在，创建", "强制更新系统", UPI)
                config["fup"] = True
                fup = config["fup"]
                files.缓存(1, config)
            # 计算经过时间，如果经过的时间大于5，我们就要启动自动更新，通过这种被动更新的方式，我们就能确保用户使用的永远是最新版本

        # 强制更新系统执行组二期
        import time
        a = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        a = a.split(" ")[0]
        a = a.split("-")
        年 = int(a[0])
        月 = int(a[1])
        日 = int(a[2])
        上一年 = config.get("year")
        上一月 = config.get("month")
        上一日 = config.get("day")
        if 上一年:
            # 这是有数据时执行的
            # noinspection PyStatementEffect
            1 + 1
        else:
            config["year"] = "2005"
            config["month"] = "6"
            config["day"] = "3"
            上一年 = 2005
            上一月 = 6
            上一日 = 3
        # 结束时间就是今天的时间
        # 开始时间就是自上次记录的时间，首次运行所记录的上次的时间默认为我的生日，不管生活有多么狼狈，生日那天也是要好好奖励自己的
        try:
            结束时间 = datetime.datetime(年, 月, 日)
            开始时间 = datetime.datetime(上一年, 上一月, 上一日)
        except ValueError:
            报警器 = True
            logs.安全退出("强制更新系统》缓存文件遭到非法修改")
        经过时间 = (结束时间 - 开始时间).days
        if 经过时间 >= 5:
            config["updata"] = True
            config["year"] = 年
            config["month"] = 月
            config["day"] = 日
            files.缓存(1, config)
            报警器 = True
            print(logs.日志("强制更新系统》自动更新》Fishconsole Project自动更新已对您设备上的Fishconsole进行了例行的更新检查", "红色"))

            # updata在前面的参数提取中搞就已经好了，现在我们只需要执行操作了
        if updata:
            系统日志("这是updata值为True时执行的操作", "强制更新系统", UPI)
            # 查找fup的变量值，关于fup的介绍在822行，他肯定是存在的，如果不存在的就跑不到这一步了
            # 这是fup开启时执行的操作
            if fup:
                # 这是fup开启时执行的操作
                res = isConnected()
                # 反转变量值，这样就可以在下一次执行的时候触发更新
                config["fup"] = False
                files.缓存(1, config)
                if res:
                    # 返回值不是False，就说明官网存活，也说明我们链接上了官网
                    print(logs.日志(f"》Fishconsole强制更新系统{fcv.version()}》Fishsys 》您的版本过低，我们将尝试自动为您更新", "红色"))
                    # 最原始的操作，大家引以为戒
                    # os.remove("Fishconsole.fcc")
                    系统日志(f"fup is {fup}", "强制更新系统", UPI)
                    try:
                        os.system("python.exe -m pip install --upgrade pip -i https://pypi.douban.com/simple")
                        os.system(f'pip install --upgrade Fishconsole')
                        main(['install', '--upgrade', 'Fishconsole'])
                    except:
                        报警器 = True
                        logs.日志("强制更新系统》pip命令组出现未知错误，程序强制退出", "红色")
                    报警器 = True
                    logs.日志("强制更新系统》更新完毕，请重新运行", "红色")
                else:
                    报警器 = True
                    logs.日志("强制更新系统》官网链接失败", "红色")

            else:
                # 这是Fishsys的复检或者是没有fup变量时执行的操作
                # 反转变量值，这样就可以在下一次时触发警告
                config["fup"] = True
                # 只要缓存出现一次变化，我们就要把他存到fcc当中，只有这样我们才能保证它在异常关闭的时候数据不会丢失
                files.缓存(1, config)

                UPI = files.缓存(2, 变量名="UPI")
                if UPI == "error":
                    UPI = False

                Forcedupdate = files.缓存(2, 变量名="Forcedupdate")
                if Forcedupdate == "error":
                    Forcedupdate = True

                sys = files.缓存(2, 变量名="updata")
                if sys == "error":
                    sys = True

                系统日志(f"读取缓存信息Foreceupdata [{Forcedupdate}]", "强制更新系统help", UPI)
                系统日志(f"读取缓存信息sys[{sys}]", "强制更新系统help", UPI)

                系统日志(f"这是强制更新系统开启时的操作", "强制更新系统help", UPI)
                isConnected = 官网存活性检测("https://pypi.org/project/Fishconsole/")
                if Forcedupdate:
                    if isConnected:
                        系统日志(f"检测到网络连接成功", "强制更新系统help", UPI)
                        print(logs.日志(f"Fishconsole{fcv.version()} 检查更新开始。。。"))
                        v = fcv.version()
                        url = "https://pypi.org/project/Fishconsole/"
                        res = requests.get(url).text
                        res_html = etree.HTML(res)
                        res_v = res_html.xpath("/html/body/main/div[2]/div/div[1]/h1/text()")[0]
                        res_v = str(res_v[21:27])
                        系统日志(f"res_v is {res_v}", "强制更新系统help", UPI)
                        系统日志(f"v is {v}", "强制更新系统help", UPI)
                        # 开启了强制更新系统

                        if res_v == v:
                            print(logs.日志(f"Fishconsole{fcv.version()} 检查更新结束,您的模块为最新版本", "绿色"))
                            print(logs.日志(f"Fishconsole{fcv.version()} 已解锁，您可以使用了", "绿色"))
                            files.缓存(3,{'FHUM': True})
                            def 帮助():
                                from Fishconsole import helps
                                helps.帮助()
                            helps_res = threading.Thread(target=帮助)
                            helps_res.start()

                            # 尝试获取缓存中的值
                            config = files.缓存(2)
                            if config:
                                系统日志("这是缓存获取成功时执行的操作", "强制更新系统helps", UPI)
                                config["updata"] = False
                                files.缓存(1, config)
                                config["year"] = 2002
                                config["month"] = 6
                                config["day"] = 3
                            else:
                                系统日志("这是缓存获取失败时执行的操作", "强制更新系统helps", UPI)
                                config = {"year": 2002, "month": 6, "day": 3, "updata": False}
                                files.缓存(1, config)

                        else:
                            # 对比到版本号不同
                            系统日志(f"对比到版本号不同", "强制更新系统help", UPI)
                            print(logs.日志(f"Fishconsole{fcv.version()} 检查更新结束"))
                            # 尝试获取缓存中的值

                            # 这是没有检查到值或者发现时执行的操作
                            print(logs.日志(f"检测到最新版本号发生了变化({res_v}>{v})，请重新运行本程序，我们将尝试自动安装最新版本", "红色"))
                            print(logs.日志(f"Fishconsole 模块已被禁用，解决方式为更新该模块", "红色"))
                            config = files.缓存(2)
                            系统日志(f"config is {config}", "强制更新系统help", UPI)
                            config["updata"] = True
                            files.缓存(1, config)
                            报警器 = True
                            print(logs.日志(f"Fishconsole 》强制更新启动", "红色"))
                    else:
                        print(logs.日志(f"Fishconsole{fcv.version()} 检查更新结束"))
                        报警器 = True
                        print(logs.日志(f"Fishconsole 》你的设备无法访问互联网，请检查网络连接", "红色"))
                else:
                    print(logs.日志(f"Fishconsole{fcv.version()} 开发者您好,我们已经停止了强制更新。请注意，全局配置已重置", "绿色"))
                    print(logs.日志(f"Fishconsole{fcv.version()} 已解锁，您可以使用了", "绿色"))
                    # 尝试获取缓存中的值
                    config = files.缓存(2)
                    fupdata = config.get("updata")
                    if fupdata:
                        config["updata"] = False
                        files.缓存(1, config)



a = threading.Thread(target=Fishconsole_Update)
a.start()


# 这是一座屎山，能修则修，不能修就算了
# 模式,加密密码,内容
def passwordsys(模式: any, id_protect: str, password_a: str):
    """

    Fishconsole Fishsys passwordsys模块

    ----

    Fishconsole文本加解密核心模块，当然有现成的密码模块，那个很完善，可以加密中文，虽然它也要调用这个，毕竟是Fishconsole Project独家加密方式

    """
    import re
    import base64
    password = str(password_a)
    password_a = str(password_a)
    id_protect = str(id_protect)

    def encrypt(en_str):
        en_str = base64.b64encode(bytes(en_str, "utf-8"))
        return en_str.decode("utf-8")

    def decrypt(de_str):
        de_str = base64.b64decode(de_str.encode("utf-8"))
        return de_str.decode("utf-8")

    模式 = str(模式)
    if 模式 == "1":

        系统日志("判断用户输入的值有没有致命问题,顺便拼接一下内容", "passwordsys", PI)
        res_a = ""
        res_b = ""
        for a in password:
            res_a = res_a + a
            if a == "@":
                print(logs.颜色(logs.日志(""), 色选="红色"))
                报警器 = True
                logs.安全退出("你的密码中不允许有@符号，请重新输入")

        for b in id_protect:
            res_b = res_b + b
            if b == "@":
                报警器 = True
                logs.安全退出(logs.日志("你的原文中不允许有@符号，请重新输入", 色选="红色"))

        else:
            系统日志("确认成功", "passwordsys", PI)
        系统日志("转移变量的数据", "passwordsys", PI)
        password = res_b
        id_protect = res_a
        系统日志("拼接用户输入的内容", "passwordsys", PI)
        res = password + "@" + id_protect
        系统日志("对用户输入的内容进行加密", "passwordsys", PI)
        jiami_last = ""
        count = 0
        counta = 0
        for a in res:
            counta = counta + 1
            if a == "1":
                jiami_last = jiami_last + "aaa"
                count = count + 1
            if a == "2":
                jiami_last = jiami_last + "aab"
                count = count + 1
            if a == "3":
                jiami_last = jiami_last + "aac"
                count = count + 1
            if a == "4":
                jiami_last = jiami_last + "aad"
                count = count + 1
            if a == "5":
                jiami_last = jiami_last + "aae"
                count = count + 1
            if a == "6":
                jiami_last = jiami_last + "aaf"
                count = count + 1
            if a == "7":
                jiami_last = jiami_last + "aba"
                count = count + 1
            if a == "8":
                jiami_last = jiami_last + "abb"
                count = count + 1
            if a == "9":
                jiami_last = jiami_last + "abc"
                count = count + 1
            if a == "0":
                jiami_last = jiami_last + "abd"
                count = count + 1
            if a == "a":
                jiami_last = jiami_last + "abe"
                count = count + 1
            if a == "b":
                jiami_last = jiami_last + "abf"
                count = count + 1
            if a == "c":
                jiami_last = jiami_last + "aca"
                count = count + 1
            if a == "d":
                jiami_last = jiami_last + "acb"
                count = count + 1
            if a == "e":
                jiami_last = jiami_last + "acc"
                count = count + 1
            if a == "f":
                jiami_last = jiami_last + "acd"
                count = count + 1
            if a == "g":
                jiami_last = jiami_last + "ace"
                count = count + 1
            if a == "h":
                jiami_last = jiami_last + "acf"
                count = count + 1
            if a == "i":
                jiami_last = jiami_last + "ada"
                count = count + 1
            if a == "j":
                jiami_last = jiami_last + "adb"
                count = count + 1
            if a == "k":
                jiami_last = jiami_last + "adc"
                count = count + 1
            if a == "l":
                jiami_last = jiami_last + "add"
                count = count + 1
            if a == "m":
                jiami_last = jiami_last + "ade"
                count = count + 1
            if a == "n":
                jiami_last = jiami_last + "adf"
                count = count + 1
            if a == "o":
                jiami_last = jiami_last + "aea"
                count = count + 1
            if a == "p":
                jiami_last = jiami_last + "aeb"
                count = count + 1
            if a == "q":
                jiami_last = jiami_last + "aec"
                count = count + 1
            if a == "r":
                jiami_last = jiami_last + "aed"
                count = count + 1
            if a == "s":
                jiami_last = jiami_last + "aee"
                count = count + 1
            if a == "t":
                jiami_last = jiami_last + "aef"
                count = count + 1
            if a == "u":
                jiami_last = jiami_last + "afa"
                count = count + 1
            if a == "v":
                jiami_last = jiami_last + "afb"
                count = count + 1
            if a == "w":
                jiami_last = jiami_last + "afc"
                count = count + 1
            if a == "x":
                jiami_last = jiami_last + "afd"
                count = count + 1
            if a == "y":
                jiami_last = jiami_last + "afe"
                count = count + 1
            if a == "z":
                jiami_last = jiami_last + "aff"
                count = count + 1
            if a == "A":
                jiami_last = jiami_last + "baa"
                count = count + 1
            if a == "B":
                jiami_last = jiami_last + "bab"
                count = count + 1
            if a == "C":
                jiami_last = jiami_last + "bac"
                count = count + 1
            if a == "D":
                jiami_last = jiami_last + "bad"
                count = count + 1
            if a == "E":
                jiami_last = jiami_last + "bae"
                count = count + 1
            if a == "F":
                jiami_last = jiami_last + "baf"
                count = count + 1
            if a == "G":
                jiami_last = jiami_last + "bba"
                count = count + 1
            if a == "H":
                jiami_last = jiami_last + "bbb"
                count = count + 1
            if a == "I":
                jiami_last = jiami_last + "bbc"
                count = count + 1
            if a == "J":
                jiami_last = jiami_last + "bbd"
                count = count + 1
            if a == "K":
                jiami_last = jiami_last + "bbe"
                count = count + 1
            if a == "L":
                jiami_last = jiami_last + "bbf"
                count = count + 1
            if a == "M":
                jiami_last = jiami_last + "bca"
                count = count + 1
            if a == "N":
                jiami_last = jiami_last + "bcb"
                count = count + 1
            if a == "O":
                jiami_last = jiami_last + "bcc"
                count = count + 1
            if a == "P":
                jiami_last = jiami_last + "bcd"
                count = count + 1
            if a == "Q":
                jiami_last = jiami_last + "bce"
                count = count + 1
            if a == "R":
                jiami_last = jiami_last + "bcf"
                count = count + 1
            if a == "S":
                jiami_last = jiami_last + "bda"
                count = count + 1
            if a == "T":
                jiami_last = jiami_last + "bdb"
                count = count + 1
            if a == "U":
                jiami_last = jiami_last + "bdc"
                count = count + 1
            if a == "V":
                jiami_last = jiami_last + "bdd"
                count = count + 1
            if a == "W":
                jiami_last = jiami_last + "bce"
                count = count + 1
            if a == "X":
                jiami_last = jiami_last + "dbf"
                count = count + 1
            if a == "Y":
                jiami_last = jiami_last + "bea"
                count = count + 1
            if a == "Z":
                jiami_last = jiami_last + "beb"
                count = count + 1
            if a == "@":
                jiami_last = jiami_last + "bec"
                count = count + 1
            if a == " ":
                jiami_last = jiami_last + "bed"
                count = count + 1
            if a == "[":
                jiami_last = jiami_last + "bee"
                count = count + 1
            if a == "]":
                jiami_last = jiami_last + "bef"
                count = count + 1
            if a == ",":
                jiami_last = jiami_last + "bfa"
                count = count + 1
            if a == "{":
                jiami_last = jiami_last + "bfb"
                count = count + 1
            if a == "}":
                jiami_last = jiami_last + "bfc"
                count = count + 1
            if a == ":":
                jiami_last = jiami_last + "bfd"
                count = count + 1
            if a == "'":
                jiami_last = jiami_last + "bfe"
                count = count + 1
            if a == "\\":
                jiami_last = jiami_last + "bff"
                count = count + 1
        if count == 1:
            logs.安全退出(logs.日志("你输入了非法字符（除1-0，a-z，空格以外其他全是），请检查后重新开始，加密失败", 色选="红色"))

        if counta == count:
            系统日志("通过检查", "passwordsys", PI)
            系统日志(f"Fishconsole》passwordsys》count is {count}", "passwordsys", PI)
            系统日志(f"Fishconsole》passwordsys》counta is {counta}", "passwordsys", PI)
        else:
            系统日志(f"Fishconsole》passwordsys》count is {count}", "passwordsys", PI)
            系统日志(f"Fishconsole》passwordsys》counta is {counta}", "passwordsys", PI)
            logs.安全退出(logs.日志("你输入了非法字符（除1-0，a-z,空格以外其他全是），请检查后重新开始，加密失败", 色选="红色"))

        系统日志("查看加密后的内容", "passwordsys", PI)

        jiami_last = encrypt(jiami_last)
        系统日志(f"Fishconsole》passwordsys》jiami_last is {jiami_last}", "passwordsys", PI)
        系统日志(f"加密成功", "passwordsys", PI)
        return jiami_last
    else:
        # 解密

        系统日志("验证密码", "passwordsys", PI)
        password_res = [f"{id_protect}"] + [f"{password_a}"]
        系统日志(f"Fishconsole》passwordsys》password_res is {password_res}", "passwordsys", PI)
        p_res = ""
        t_res = ""
        for a in password_res[0]:
            p_res = p_res + a
        for a in password_res[1]:
            t_res = t_res + a
        jiemi_last = decrypt(t_res)

        系统日志("查看解密加密的内容", "passwordsys", PI)
        pattern = re.compile('.{3}')
        a = str(' '.join(pattern.findall(jiemi_last)))
        系统日志(f"Fishconsole》passwordsys》pattern is {pattern}""passwordsys", PI)
        系统日志(f"Fishconsole》passwordsys》a is {a}""passwordsys", PI)
        # 重新合并加密后的内容
        系统日志("重新合并数据""passwordsys", PI)
        系统日志("先将每个转化后的值进行拆分""passwordsys", PI)
        pattern_jiemi = (' '.join(pattern.findall(jiemi_last)))
        pattern_jiemi = pattern_jiemi.split(' ')
        pattern_resa = ""
        系统日志(f"Fishconsole》passwordsys》pattern_jiemi is {pattern_jiemi}""passwordsys", PI)
        for a in pattern_jiemi:
            if a == "aaa":
                pattern_resa = pattern_resa + "1"
            if a == "aab":
                pattern_resa = pattern_resa + "2"
            if a == "aac":
                pattern_resa = pattern_resa + "3"
            if a == "aad":
                pattern_resa = pattern_resa + "4"
            if a == "aae":
                pattern_resa = pattern_resa + "5"
            if a == "aaf":
                pattern_resa = pattern_resa + "6"
            if a == "aba":
                pattern_resa = pattern_resa + "7"
            if a == "abb":
                pattern_resa = pattern_resa + "8"
            if a == "abc":
                pattern_resa = pattern_resa + "9"
            if a == "abd":
                pattern_resa = pattern_resa + "0"
            if a == "abe":
                pattern_resa = pattern_resa + "a"
            if a == "abf":
                pattern_resa = pattern_resa + "b"
            if a == "aca":
                pattern_resa = pattern_resa + "c"
            if a == "acb":
                pattern_resa = pattern_resa + "d"
            if a == "acc":
                pattern_resa = pattern_resa + "e"
            if a == "acd":
                pattern_resa = pattern_resa + "f"
            if a == "ace":
                pattern_resa = pattern_resa + "g"
            if a == "acf":
                pattern_resa = pattern_resa + "h"
            if a == "ada":
                pattern_resa = pattern_resa + "i"
            if a == "adb":
                pattern_resa = pattern_resa + "j"
            if a == "adc":
                pattern_resa = pattern_resa + "k"
            if a == "add":
                pattern_resa = pattern_resa + "l"
            if a == "ade":
                pattern_resa = pattern_resa + "m"
            if a == "adf":
                pattern_resa = pattern_resa + "n"
            if a == "aea":
                pattern_resa = pattern_resa + "o"
            if a == "aeb":
                pattern_resa = pattern_resa + "p"
            if a == "aec":
                pattern_resa = pattern_resa + "q"
            if a == "aed":
                pattern_resa = pattern_resa + "r"
            if a == "aee":
                pattern_resa = pattern_resa + "s"
            if a == "aef":
                pattern_resa = pattern_resa + "t"
            if a == "afa":
                pattern_resa = pattern_resa + "u"
            if a == "afb":
                pattern_resa = pattern_resa + "v"
            if a == "afc":
                pattern_resa = pattern_resa + "w"
            if a == "afd":
                pattern_resa = pattern_resa + "x"
            if a == "afe":
                pattern_resa = pattern_resa + "y"
            if a == "aff":
                pattern_resa = pattern_resa + "z"
            if a == "baa":
                pattern_resa = pattern_resa + "A"
            if a == "bab":
                pattern_resa = pattern_resa + "B"
            if a == "bac":
                pattern_resa = pattern_resa + "C"
            if a == "bad":
                pattern_resa = pattern_resa + "D"
            if a == "bae":
                pattern_resa = pattern_resa + "E"
            if a == "baf":
                pattern_resa = pattern_resa + "F"
            if a == "bba":
                pattern_resa = pattern_resa + "G"
            if a == "bbb":
                pattern_resa = pattern_resa + "H"
            if a == "bbc":
                pattern_resa = pattern_resa + "I"
            if a == "ddb":
                pattern_resa = pattern_resa + "J"
            if a == "bbe":
                pattern_resa = pattern_resa + "K"
            if a == "bbf":
                pattern_resa = pattern_resa + "L"
            if a == "bca":
                pattern_resa = pattern_resa + "M"
            if a == "bcb":
                pattern_resa = pattern_resa + "N"
            if a == "bcc":
                pattern_resa = pattern_resa + "O"
            if a == "bcd":
                pattern_resa = pattern_resa + "P"
            if a == "bce":
                pattern_resa = pattern_resa + "Q"
            if a == "bcf":
                pattern_resa = pattern_resa + "R"
            if a == "bda":
                pattern_resa = pattern_resa + "S"
            if a == "bdb":
                pattern_resa = pattern_resa + "T"
            if a == "bdc":
                pattern_resa = pattern_resa + "U"
            if a == "bdd":
                pattern_resa = pattern_resa + "V"
            if a == "bce":
                pattern_resa = pattern_resa + "W"
            if a == "bdf":
                pattern_resa = pattern_resa + "X"
            if a == "bea":
                pattern_resa = pattern_resa + "Y"
            if a == "beb":
                pattern_resa = pattern_resa + "Z"
            if a == "bed":
                pattern_resa = pattern_resa + " "
            if a == "bec":
                pattern_resa = pattern_resa + "@"
            if a == "bee":
                pattern_resa = pattern_resa + "["
            if a == "bef":
                pattern_resa = pattern_resa + "]"
            if a == "bfa":
                pattern_resa = pattern_resa + ","
            if a == "bfb":
                pattern_resa = pattern_resa + "{"
            if a == "bfc":
                pattern_resa = pattern_resa + "}"
            if a == "bfd":
                pattern_resa = pattern_resa + ":"
            if a == "bfe":
                pattern_resa = pattern_resa + "'"
            if a == "bff":
                pattern_resa = pattern_resa + "\\"

        系统日志("读取加密信息", "passwordsys", PI)
        text = pattern_resa.split("@", 1)[0]
        password = pattern_resa.split("@", 1)[1]
        系统日志(f"Fishconsole》passwordsys》text is {text}", "passwordsys", PI)
        系统日志(f"Fishconsole》passwordsys》password is {password}", "passwordsys", PI)
        if password == p_res:
            系统日志("密码验证成功", "passwordsys", PI)
            return f"{text}"
        else:
            logs.安全退出(logs.日志("您的密码是错误的，请核对后重新输入"))


def 密码(模式, 原文, 密码: str = ""):
    """

    Fishconsole Fishsys密码模块

    ----

    - 这个就是文字加解密模块了

    - 它能将几乎可以加密所有的文字（其实就是转了个二进制哈哈），嗯，就这样

    :param 模式: 选择加密（1）还是解密（2）
    :param 原文: 原来的文字
    :param 密码:  你说是啥子麻
    :return:    操作后的文本
    """

    if 模式 == 1:
        a = 字符转unicode(1, 原文)
        系统日志(f"a is {a}", "passwordsys", PI)
        b = passwordsys(1, a, 密码)
        系统日志(f"b is {b}", "passwordsys", PI)
        return b
    else:
        c = passwordsys(2, 密码, 原文)
        系统日志(f"c is {c}", "passwordsys", PI)

        return c


# 模式,加密密码,内容
# a = password(1, 3, "1234567890")
# b = password(2, 3, a)


def 排名(数据源: list, 第几个: int):
    b = files.强制类型检测(数据源, "list")
    if b:
        第几个 = int(第几个)
        第几个 = 第几个 - 1
        a = 数据源
        for i in range(len(a)):
            for j in range(0, len(a) - 1):
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
        return a[第几个]
    else:
        logs.安全退出("Fishsys》排名》强制类型检测》请指定list类型的数据源")


def 字符转unicode(模式, 原文: str):
    """
    Fishconsole 字符转unicode 模块

    ----

     顾名思义，就是这个（肝不动了。。）

    :param 模式: 1是加密，2是解密
    :param 原文: 原始文字
    :return: 加工过后的str类型的文字
    """
    模式 = str(模式)
    原文 = str(原文)
    if 模式 == "1":
        原文 = 原文.encode('unicode_escape')
        系统日志(f"》Fishconsole》字符串转unicode》type 原文 is {type(原文)}", "字符转unicode", ZUI)
        系统日志(f"》Fishconsole》字符串转unicode》原文 is {原文}", ZUI)
        原文 = str(原文)
        系统日志(f"》Fishconsole》字符串转unicode》type 原文 is {type(原文)}", "字符转unicode", ZUI)
        系统日志(f"》Fishconsole》字符串转unicode》原文 is {原文}", "字符转unicode", ZUI)
        return 原文
    elif 模式 == "2":
        系统日志(f"》Fishconsole》字符串转unicode》type 原文 is {type(原文)}", "字符转unicode", ZUI)
        系统日志(f"》Fishconsole》字符串转unicode》原文 is {原文}", "字符转unicode", ZUI)
        b = 原文.replace("b'", "")
        c = b.replace("'", '')
        d = c.encode('utf-8').decode('unicode_escape')
        e = d.replace("nui", r"\u").encode('utf-8').decode('unicode_escape')
        系统日志(f"》Fishconsole》字符串转unicode》type e is {type(e)}", "字符转unicode", ZUI)
        系统日志(f"》Fishconsole》字符串转unicode》e is {e}", "字符转unicode", ZUI)
        return e
    else:
        logs.错误跟踪(["Fishconsole", "字符串转unicode", "模式"], "请选择正确的模式", {模式})


def 讯飞云控(fid):
    """

    - 我记忆中对云控最字面的理解就是云端控制，也就是从服务器中下载需要的数据

    - 这时，就要白嫖服务器了，这里选择讯飞（感谢Coolapk@寒鸽的FusionApp让我在初一时第一次体验了更新弹窗的实现方式）

    ----
    FishConsole Fishsys 讯飞云控模块
    ----
    ----

    :param fid: 讯飞语记fid（如何获得？使用检查，找到相关的json数据就可以拿走fid）


    :return: 字典或列表
    """
    import json
    import requests
    import chardet
    if 官网存活性检测("https://iflynote.com/i/"):
        fid = str(fid)
        url = f"https://api.iflynote.com/notes/share/doc/shareFileDetail?fid={fid}"
        header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Mobile Safari/537.36 Edg/101.0.1210.47'}
        res = requests.get(url, headers=header).text

        # noinspection PyBroadException
        # print(chardet.detect(res))

        try:
            res = re.findall(r'【(.*)】', res)[0]
            res = res.replace("\\n","")
            res = res.replace("\\", "")
            res = eval(res)

        except:
            logs.变量查看("res", res)
            logs.安全退出("Fishsys》讯飞云控》类型转换器》出现意外，可能是解析模式错误或json文档版本过低或者你在云控乱敲")
    else:
        logs.安全退出("Fishsys》讯飞云控》网络链接失败")
    return res


def 邮件发送(
        邮件接收账号,
        邮件发送账号=None,
        授权码=None,
        SMTP服务器地址="smtp.qq.com",
        端口号=465,
        HTML正文内容='<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible"content="IE=edge"><meta name="viewport"content="width=device-width, initial-scale=1.0"><title>Document</title><style></style></head><body><div style="width:100%;background-color:#12001ed2;height:157vw"><div class="顶栏"style="box-shadow: rgb(178,178,253)15px 15px 40px -10px;background-image:linear-gradient(157deg,#e0c3fc 0%,#8ec5fc 100%);height:9vw;width:100%;box-shadow:rgb(178,178,253)15vw 15vw 40vw-10vw;overflow:hidden"><p style="font-size:3vw;font-weight:bold;position:relative;top:-1vw;left:8vw;color:rgb(84,52,79);width:500vw;background: none;">''Fishconsole Project Email''</p></div><div style="height:11vw;width:70%;margin:10vw 0vw 1vw 16%;border:0.2vw solid#a1a1a1;border-radius:10px;overflow:hidden"><p style="text-align:center;margin:4%;font-size:3vw;font-weight:bold;color:rgb(219,203,255)">'f'目标IP：000.00.000.00''</p><div style="margin: -8vw -0.2vw;height:6vw;width:1vw;background-color:rgb(255,194,255);border:2px;border-radius:1vw"></div></div><div style="height:84vw;width:71%;margin:7vw 0vw 0vw 16%;border:0.2vw solid#a1a1a1;border-radius:15px;padding:6vw 6vw 0vw 6vw;box-sizing:border-box;overflow:hidden;line-height: 6vw;"><p><h1 style="font-size:7vw;margin-bottom:6vw;color:rgb(250,219,255)">'f'正文''</h1></p><p style="font-size:3vw;Text-indent:2em;word-wrap:break-word;color:#f2e5ff">'f'这是一封来自Fishconsole Project的预设邮件，仅供测试使用，如有需要，请将HTML正文内容变量修改为自己的HTML文档''</p><p style="font-size:3vw;Text-indent:2em;word-wrap:break-word;color:#f2e5ff">''This is a test email for the Fishconsole Project. If you need to modify the HTML document, please do so yourself''</p><div style="height:1%;width:44%;position:relative;bottom:-29vw;left:11vw;background-color:rgb(217,215,215);border:2px;border-radius:3px"></div></div></div></body></html>',
        收件人姓名="Fishconsole 开发者",
        邮件标题="Fishconsole Project System - 数据传送器",
        附件地址=None,
        发件人姓名=None
):
    """

    Fishconsole Fishsys 邮件发送模块

    ----

    - 就是一个发邮件的


    :param 邮件发送账号:邮件发送账号
    :param 邮件接收账号:邮件接收账号
    :param 授权码:授权码
    :param SMTP服务器地址:SMTP服务器地址
    :param 端口号:端口号
    :param HTML正文内容:HTML正文内容
    :param 收件人姓名:收件人姓名
    :param 邮件标题:邮件标题
    :param 附件地址:附件地址
    :param 发件人姓名:发件人姓名
    :return: None
    """

    res = 官网存活性检测("http://www.baidu.com")
    if res:
        try:
            from_addr = 邮件发送账号  # 邮件发送账号
            to_addrs = 邮件接收账号  # 接收邮件账号


            if 授权码==None:
                temp=files.缓存(2,变量名="AC")
                if temp=="error":
                    logs.安全退出("未指定授权码")
                else:
                    print(logs.日志("Fishsys邮件发送》检测到预设的授权码，导入"))
                    授权码=temp


            if 邮件发送账号==None:
                temp=files.缓存(2,变量名="FESA")
                if temp=="error":
                    logs.安全退出("未指定邮件发送账号")
                else:
                    print(logs.日志("Fishsys邮件发送》检测到预设的邮件发送账号，导入"))
                    from_addr=temp

            if 发件人姓名==None:
                temp=files.缓存(2,变量名="Sender")
                if temp=="error":
                    logs.安全退出("未指定发件人姓名")
                else:
                    print(logs.日志("Fishsys邮件发送》检测到预设的发件人姓名，导入"))
                    发件人姓名=temp

            qqCode = 授权码  # 授权码（这个要填自己获取到的）
            smtp_server = SMTP服务器地址  # 固定写死
            smtp_port = 端口号  # 固定端口
            # 配置服务器
            try:
                stmp = smtplib.SMTP_SSL(smtp_server, smtp_port)
                stmp.login(from_addr, qqCode)
            except:
                print(logs.日志("Fishsys邮件发送》尝试登录操作失败", "红色"))
            # 组装发送内容
            if 附件地址 != None:
                TXT = MIMEApplication(open(附件地址, 'rb').read())
                TXT.add_header('Content-Disposition', 'attachment', filename=附件地址)
            message = MIMEMultipart()
            message['From'] = Header(发件人姓名, 'utf-8')  # 发件人
            message['To'] = Header(收件人姓名, 'utf-8')  # 收件人
            subject = 邮件标题
            message['Subject'] = Header(subject, 'utf-8')  # 邮件标题
            if 附件地址 != None:
                message.attach(TXT)
            message.attach(MIMEText(HTML正文内容, 'HTML', 'utf-8'))  # 把正文附在邮件上
            try:
                stmp.sendmail(from_addr, to_addrs, message.as_string())
            except Exception as e:
                logs.变量查看('from_addr',from_addr)
                logs.变量查看('to_addrs',to_addrs)
                logs.变量查看('message',message)
                print('邮件发送失败--' + str(e))
            print('邮件发送成功')
        finally:
            files.缓存(3,数据={"AC":授权码})
            files.缓存(3,数据={"Sender":收件人姓名})
            files.缓存(3,数据={"FESA":from_addr})
    else:
        print(logs.日志("Fishsys邮件发送》官网连接失败》邮件发送失败", "红色"))



def 数字字母化(模式, 数据源):
    模式 = str(模式)
    if 模式 == "1":
        强制类型检测 = files.强制类型检测(数据源, "int")
        if 强制类型检测:
            空容器 = ""
            数据源 = list(str(数据源))
            for a in 数据源:
                if a == "0":
                    空容器 = 空容器 + "A"
                if a == "1":
                    空容器 = 空容器 + "B"
                if a == "2":
                    空容器 = 空容器 + "C"
                if a == "3":
                    空容器 = 空容器 + "D"
                if a == "4":
                    空容器 = 空容器 + "E"
                if a == "5":
                    空容器 = 空容器 + "F"
                if a == "6":
                    空容器 = 空容器 + "G"
                if a == "7":
                    空容器 = 空容器 + "H"
                if a == "8":
                    空容器 = 空容器 + "I"
                if a == "9":
                    空容器 = 空容器 + "J"
                return 空容器
        else:
            logs.安全退出("类型错误")
    if 模式 == "2":
        空容器 = ""
        强制类型检测 = files.强制类型检测(数据源, "str")
        if 强制类型检测:
            数据源 = list(str(数据源))
            计数器 = 0
            计数器a = 0
            for a in 数据源:
                计数器a = 计数器a + 1
            for a in 数据源:
                if a == "A":
                    计数器 = 计数器 + 1
                    空容器 = 空容器 + "0"
                if a == "B":
                    计数器 = 计数器 + 1
                    空容器 = 空容器 + "1"
                if a == "C":
                    计数器 = 计数器 + 1
                    空容器 = 空容器 + "2"
                if a == "D":
                    计数器 = 计数器 + 1
                    空容器 = 空容器 + "3"
                if a == "E":
                    计数器 = 计数器 + 1
                    空容器 = 空容器 + "4"
                if a == "F":
                    计数器 = 计数器 + 1
                    空容器 = 空容器 + "5"
                if a == "G":
                    计数器 = 计数器 + 1
                    空容器 = 空容器 + "6"
                if a == "H":
                    计数器 = 计数器 + 1
                    空容器 = 空容器 + "7"
                if a == "I":
                    计数器 = 计数器 + 1
                    空容器 = 空容器 + "8"
                if a == "J":
                    计数器 = 计数器 + 1
                    空容器 = 空容器 + "9"
                if 计数器 == 计数器a:
                    return 空容器
                else:
                    logs.安全退出("数据源错误")
        else:
            logs.安全退出("类型错误")
        return 数据源


def 任务平均分配(任务数量, 数据源: list):
    计数器 = 0  # 统计数据源列表的元素个数
    计数器a = 0
    计数器c = 0  # 统计完成列表的元素总个数
    计数器d = 0  # 统计完成列表的元素个数
    计数器e = 0  # 最后一次统计完成列表的元素个数
    完成列表 = []
    空列表 = []
    try:
        任务数量 = int(任务数量)
    except:
        logs.安全退出("任务平均分配》任务数量类型检测》请指定正确的类型")
    if files.强制类型检测(数据源, "list"):
        for _ in 数据源:
            计数器 = 计数器 + 1
        try:
            str(计数器 / 任务数量).split(".")[1]
        except ZeroDivisionError:
            logs.安全退出("任务平均分配》检测》错误的分配")
        if str(计数器 / 任务数量).split(".")[0] == "0":
            logs.安全退出("任务平均分配》检测》分配数量大于池数量")
        if str(计数器 / 任务数量).split(".")[1] >= "5":
            print(logs.日志("任务平均分配》检测》分配数量过大，输出结果已受到干扰 [！！！警告！！！]", "红色"))
            任务分配数量 = int(计数器 / 任务数量) + 1
        else:
            任务分配数量 = int(计数器 / 任务数量)
        if 任务分配数量 == 1:
            logs.安全退出("任务平均分配》检测》不允许切分的太多，请调低任务数量")
        for b in 数据源:
            空列表.append(b)
            计数器a = 计数器a + 1
            if 计数器a == 任务分配数量:
                完成列表.append(空列表)
                空列表 = []
                计数器a = 0
        for a in 完成列表:
            for b in a:
                计数器c = 计数器c + 1
        for _ in 完成列表:
            计数器d = 计数器d + 1
        if 计数器d != int(任务数量):
            if 计数器c < 计数器:
                相差的值 = 计数器 - 计数器c
                完成列表.append(数据源[-相差的值:])
        else:
            if 计数器c < 计数器:
                相差的值 = 计数器 - 计数器c
                for a in 数据源[-相差的值:]:
                    完成列表[-1].append(a)

        for _ in 完成列表:
            计数器e = 计数器e + 1
        if 计数器e != 任务数量:
            完成列表.append([])


        logs.变量查看("计数器e",计数器e)
        logs.变量查看("任务数量",任务数量)
        return 完成列表
    else:
        logs.安全退出("任务平均分配》数据源类型检测》请指定正确的类型")


