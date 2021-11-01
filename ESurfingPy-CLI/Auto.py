"""
GitHub: https://github.com/Aixzk/ESurfingPy-CLI
"""

import time
import ESurfingPy
import psutil as p

prints = lambda text: print(f'\r[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] {text}\t', end='  ')
printWithTime = lambda text: print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] {text}')


def get_speed(t_type):
    """获取当前上行或下行速率"""
    if t_type in ['ul', '上传']:
        first = p.net_io_counters().bytes_sent
        time.sleep(1)
        delta = p.net_io_counters().bytes_sent - first
    elif t_type in ['dl', '下载']:
        first = p.net_io_counters().bytes_recv
        time.sleep(1)
        delta = p.net_io_counters().bytes_recv - first
    else:
        return 0
    return round(delta / 1024 / 1024, 2)  # 转为 x.xx MB/s


def speed_mode(mode, value, autostop, esrfingurl, wlanacip, wlanuserip, account, password, details, debug):
    """上行或下载速率低于指定值时自动重登校园网"""

    def get_traffic():
        if mode == '1':
            return p.net_io_counters().bytes_sent
        elif mode == '2':
            return p.net_io_counters().bytes_recv
        else:
            return 0

    if mode == '1':
        typestr = '上传'
    elif mode == '2':
        typestr = '下载'
    else:
        return

    printWithTime('首次登录尝试获取 signature ……')
    firstlogin = ESurfingPy.login(esrfingurl, wlanacip, wlanuserip, account, password, details, debug)
    if firstlogin['result'] == 'succeed':
        signature = firstlogin['signature']
    else:
        printWithTime(f'登录失败：{firstlogin}')
        return

    lowtimes = 0  # 低速次数
    seemdone = 0  # 低于 0.1 MB/s 时判定疑似传输完成的次数
    logtraffic = get_traffic()

    while True:
        speed = get_speed(typestr)
        nowtraffic = round((get_traffic() - logtraffic) / 1024 / 1024, 2)
        prints(
            f'本次流量：{nowtraffic} MB  {typestr}速度：{speed} MB/s  低速触发：{lowtimes}/10  完成触发：{seemdone}/10')
        if autostop:
            if speed <= 0.1:  # 速率低于 0.1 MB/s ，判定疑似传输完成
                seemdone += 1
                if seemdone == 11:
                    print()
                    printWithTime(f'检测到连续 10s {typestr}速率低于 0.1 MB/s，已自动停止')
                    return
                continue
            else:
                seemdone = 0
        if speed < value:  # 速率低于指定值，疑似被限速
            lowtimes += 1
            if lowtimes == 11:
                print()
                printWithTime(f'检测到连续 10s {typestr}速率低于 {value} MB/s，疑似被限速，重新登录中……')
                ESurfingPy.logout(esrfingurl, wlanacip, wlanuserip, account, password, signature, details, debug)
                loginresult = ESurfingPy.login(esrfingurl, wlanacip, wlanuserip, account, password, details, debug)
                if firstlogin['result'] == 'succeed':
                    signature = loginresult['signature']
                else:
                    printWithTime(f'登录失败：{firstlogin}')
                    return

                # 重置
                lowtimes = 0
                seemdone = 0
                logtraffic = get_traffic()
        else:  # 速率高于指定值
            lowtimes = 0
            seemdone = 0


# 传输达到一定量模式
def traffic_mode(mode, value, esrfingurl, wlanacip, wlanuserip, account, password, details, debug):
    """上传或下载流量达到指定值时自动重登校园网"""

    def get_traffic():
        if mode == '3':
            return p.net_io_counters().bytes_sent
        elif mode == '4':
            return p.net_io_counters().bytes_recv

    if mode == '3':
        typestr = '上传'
    elif mode == '4':
        typestr = '下载'
    else:
        return

    printWithTime('首次登录尝试获取 signature ……')
    firstlogin = ESurfingPy.login(esrfingurl, wlanacip, wlanuserip, account, password, details, debug)
    if firstlogin['result'] == 'succeed':
        signature = firstlogin['signature']
    else:
        printWithTime(f'登录失败：{firstlogin}')
        return

    logtraffic = get_traffic()
    while True:
        delta = round((get_traffic() - logtraffic) / 1024 / 1024, 2)
        speed = get_speed(typestr)
        prints(f'{typestr}速率：{speed} MB/s  流量触发：{delta}/{value} MB')
        if delta >= value:
            print()
            printWithTime('重新登录中')
            ESurfingPy.logout(esrfingurl, wlanacip, wlanuserip, account, password, signature, details, debug)
            loginresult = ESurfingPy.login(esrfingurl, wlanacip, wlanuserip, account, password, details, debug)
            if firstlogin['result'] == 'succeed':
                signature = loginresult['signature']
            else:
                printWithTime(f'登录失败：{firstlogin}')
                return
            logtraffic = get_traffic()


def interval_mode(value, esrfingurl, wlanacip, wlanuserip, account, password, details, debug):
    """间隔指定的时间自动重登校园网"""

    printWithTime('首次登录尝试获取 signature ……')
    firstlogin = ESurfingPy.login(esrfingurl, wlanacip, wlanuserip, account, password, details, debug)
    if firstlogin['result'] == 'succeed':
        signature = firstlogin['signature']
    else:
        printWithTime(f'登录失败：{firstlogin}')
        return

    timecal = 0
    while True:
        prints(f'即将于 {value - timecal}s 后重新登录')
        time.sleep(1)
        if value - timecal == 0:
            print()
            prints('正在重新登录\n')

            ESurfingPy.logout(esrfingurl, wlanacip, wlanuserip, account, password, signature, details, debug)
            loginresult = ESurfingPy.login(esrfingurl, wlanacip, wlanuserip, account, password, details, debug)
            if firstlogin['result'] == 'succeed':
                signature = loginresult['signature']
            else:
                printWithTime(f'登录失败：{firstlogin}')
                return
            timecal = 0
        else:
            timecal += 1


def manual_mode(esrfingurl, wlanacip, wlanuserip, account, password, details, debug):
    """手动按回车后自动重登校园网"""

    printWithTime('首次登录尝试获取 signature ……')
    firstlogin = ESurfingPy.login(esrfingurl, wlanacip, wlanuserip, account, password, details, debug)
    if firstlogin['result'] == 'succeed':
        signature = firstlogin['signature']
    else:
        printWithTime(f'登录失败：{firstlogin}')
        return

    while True:
        input(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] 按回车键以重新登录校园网')
        ESurfingPy.logout(esrfingurl, wlanacip, wlanuserip, account, password, signature, details, debug)
        loginresult = ESurfingPy.login(esrfingurl, wlanacip, wlanuserip, account, password, details, debug)
        if firstlogin['result'] == 'succeed':
            signature = loginresult['signature']
        else:
            printWithTime(f'登录失败：{firstlogin}')
            return


def Relogin(mode, value, autostop, esrfingurl, wlanacip, wlanuserip, account, signature, details, debug):
    """
    1. 上传速率低于指定值
    2. 下载速率低于指定值
    3. 上传流量达到指定值
    4. 下载流量达到指定值
    5. 间隔指定时间
    6. 手动模式
    """
    while True:
        if mode not in ['1', '2', '3', '4', '5', '6']:
            print('触发模式：\n'
                  '1. 上传速率低于指定值\n'
                  '2. 下载速率低于指定值\n'
                  '3. 上传流量达到指定值\n'
                  '4. 下载流量达到指定值\n'
                  '5. 间隔指定时间\n'
                  '6. 手动模式')
            mode = input('请选择正确的触发模式：')
            if mode in ['1', '2', '3', '4', '5', '6']:
                break
            else:
                continue
        else:
            if mode != '6':
                while True:
                    try:
                        value = float(value)
                        break
                    except:
                        value = input('请输入正确的触发值（单位：MB/s, MB, s）：')
                        continue

    if mode in ['1', '2']:
        speed_mode(mode, value, autostop, esrfingurl, wlanacip, wlanuserip, account, signature, details, debug)
    elif mode in ['3', '4']:
        traffic_mode(mode, value, esrfingurl, wlanacip, wlanuserip, account, signature, details, debug)
    elif mode == '5':
        interval_mode(value, esrfingurl, wlanacip, wlanuserip, account, signature, details, debug)
    elif mode == '6':
        manual_mode(esrfingurl, wlanacip, wlanuserip, account, signature, details, debug)

    return
