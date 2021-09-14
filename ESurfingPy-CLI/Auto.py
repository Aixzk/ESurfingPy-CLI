import time
import ESurfingPy
import psutil as p

timeformat = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
prints = lambda text: print('\r[{}] {}\t'.format(timeformat, text), end='  ')
printWithTime = lambda text: print('[{}] {}'.format(timeformat, text))


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
        printWithTime('登录失败：{}'.format(firstlogin))
        return

    lowtimes = 0  # 低速次数
    seemdone = 0  # 低于 0.1 MB/s 时判定疑似传输完成的次数
    logtraffic = get_traffic()

    while True:
        speed = get_speed(typestr)
        nowtraffic = round((get_traffic() - logtraffic) / 1024 / 1024, 2)
        prints(
            '本次流量：{} MB  {}速度：{} MB/s  低速触发：{}/10  完成触发：{}/10'.format(nowtraffic, typestr, speed, lowtimes, seemdone))
        if autostop:
            if speed <= 0.1:  # 速率低于 0.1 MB/s ，判定疑似传输完成
                seemdone += 1
                if seemdone == 11:
                    print()
                    printWithTime('检测到连续 10s {}速率低于 0.1 MB/s，已自动停止'.format(typestr))
                    return
                continue
            else:
                seemdone = 0
        if speed < value:  # 速率低于指定值，疑似被限速
            lowtimes += 1
            if lowtimes == 11:
                print()
                printWithTime('检测到连续 10s {}速率低于 {} MB/s，疑似被限速，重新登录中……'.format(typestr, value))
                ESurfingPy.logout(esrfingurl, wlanacip, wlanuserip, account, password, signature, details, debug)
                loginresult = ESurfingPy.login(esrfingurl, wlanacip, wlanuserip, account, password, details, debug)
                if firstlogin['result'] == 'succeed':
                    signature = loginresult['signature']
                else:
                    printWithTime('登录失败：{}'.format(firstlogin))
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
        printWithTime('登录失败：{}'.format(firstlogin))
        return

    logtraffic = get_traffic()
    while True:
        delta = round((get_traffic() - logtraffic) / 1024 / 1024, 2)
        speed = get_speed(typestr)
        prints('{}速率：{} MB/s  流量触发：{}/{} MB'.format(typestr, speed, delta, value))
        if delta >= value:
            print()
            printWithTime('重新登录中')
            ESurfingPy.logout(esrfingurl, wlanacip, wlanuserip, account, password, signature, details, debug)
            loginresult = ESurfingPy.login(esrfingurl, wlanacip, wlanuserip, account, password, details, debug)
            if firstlogin['result'] == 'succeed':
                signature = loginresult['signature']
            else:
                printWithTime('登录失败：{}'.format(firstlogin))
                return
            logtraffic = get_traffic()


def interval_mode(value, esrfingurl, wlanacip, wlanuserip, account, password, details, debug):
    """间隔指定的时间自动重登校园网"""

    printWithTime('首次登录尝试获取 signature ……')
    firstlogin = ESurfingPy.login(esrfingurl, wlanacip, wlanuserip, account, password, details, debug)
    if firstlogin['result'] == 'succeed':
        signature = firstlogin['signature']
    else:
        printWithTime('登录失败：{}'.format(firstlogin))
        return

    timecal = 0
    while True:
        prints('即将于 {}s 后重新登录'.format(value - timecal))
        time.sleep(1)
        if value - timecal == 0:
            print()
            prints('正在重新登录\n')

            ESurfingPy.logout(esrfingurl, wlanacip, wlanuserip, account, password, signature, details, debug)
            loginresult = ESurfingPy.login(esrfingurl, wlanacip, wlanuserip, account, password, details, debug)
            if firstlogin['result'] == 'succeed':
                signature = loginresult['signature']
            else:
                printWithTime('登录失败：{}'.format(firstlogin))
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
        printWithTime('登录失败：{}'.format(firstlogin))
        return

    while True:
        input('[{}] 按回车键以重新登录校园网'.format(timeformat))
        ESurfingPy.logout(esrfingurl, wlanacip, wlanuserip, account, password, signature, details, debug)
        loginresult = ESurfingPy.login(esrfingurl, wlanacip, wlanuserip, account, password, details, debug)
        if firstlogin['result'] == 'succeed':
            signature = loginresult['signature']
        else:
            printWithTime('登录失败：{}'.format(firstlogin))
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
    if mode not in ['1', '2', '3', '4', '5', '6']:
        print('请选择正确的触发模式。')
        return
    else:
        if mode != '6':
            try:
                value = float(value)
            except:
                print('请输入正确的触发值。')
                return
    if mode in ['1', '2']:
        speed_mode(mode, value, autostop, esrfingurl, wlanacip, wlanuserip, account, signature, details, debug)
    elif mode in ['3', '4']:
        traffic_mode(mode, value, esrfingurl, wlanacip, wlanuserip, account, signature, details, debug)
    elif mode == '5':
        interval_mode(value, esrfingurl, wlanacip, wlanuserip, account, signature, details, debug)
    elif mode == '6':
        manual_mode(esrfingurl, wlanacip, wlanuserip, account, signature, details, debug)
    return
