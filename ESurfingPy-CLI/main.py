"""
GitHub: https://github.com/Aixzk/ESurfingPy-CLI
"""

import click
import theocr
import Auto
import ESurfingPy


@click.group()
def main():
    """ (v0.18)基于 Python 实现登录和登出广东天翼校园网网页认证通道的命令行工具。 """
    pass


@main.command()
@click.option('-url', '--esrfingurl', default='', help='校园网登录网址')
@click.option('-acip', '--wlanacip', default='',  help='认证服务器IP')
@click.option('-userip', '--wlanuserip', default='',  help='登录设备IP')
@click.option('-acc', '--account', prompt='Account', help='账号')
@click.option('-pwd', '--password', prompt='Password', help='密码')
@click.option('-details', default=False, type=bool, help='输出详细过程')
@click.option('-debug', default=False, type=bool, help='调试模式')
def login(esrfingurl, wlanacip, wlanuserip, account, password, details, debug):
    """ 发送 GET 请求登录校园网 """
    return ESurfingPy.login(esrfingurl, wlanacip, wlanuserip, account, password, details, debug)


@main.command()
@click.option('-url', '--esrfingurl', default='',  help='校园网登录网址')
@click.option('-acip', '--wlanacip', default='',  help='认证服务器IP')
@click.option('-userip', '--wlanuserip', default='',  help='登录设备IP')
@click.option('-acc', '--account', prompt='Account', help='账号')
@click.option('-pwd', '--password', default='', help='密码')
@click.option('-sign', '--signature', default='', help='签名')
@click.option('-details', default=False, type=bool, help='输出详细过程')
@click.option('-debug', default=False, type=bool, help='调试模式')
def logout(esrfingurl, wlanacip, wlanuserip, account, password, signature, details, debug):
    """ 发送 POST 请求登出校园网 """
    return ESurfingPy.logout(esrfingurl, wlanacip, wlanuserip, account, password, signature, details, debug)


@main.command()
@click.option('-m', '--mode', prompt='Mode', help='触发模式')
@click.option('-v', '--value', prompt='Value', help='触发网速(MB/s)或流量(MB)或时间(s)')
@click.option('-as', '--autostop', default=False, type=bool, help='自动停止')
@click.option('-url', '--esrfingurl', prompt='ESurfingURL', help='校园网登录网址')
@click.option('-acip', '--wlanacip', prompt='WlanACIP', help='认证服务器IP')
@click.option('-userip', '--wlanuserip', prompt='WlanUserIP', help='登录设备IP')
@click.option('-acc', '--account', prompt='Account', help='账号')
@click.option('-pwd', '--password', prompt='Password', help='密码')
@click.option('-details', default=False, type=bool, help='输出详细过程')
@click.option('-debug', default=False, type=bool, help='调试模式')
def auto(mode, value, autostop, esrfingurl, wlanacip, wlanuserip, account, password, details, debug):
    """ 多种模式触发重登校园网 """
    return Auto.Relogin(mode, value, autostop, esrfingurl, wlanacip, wlanuserip, account, password, details, debug)


@main.command()
@click.option('-img', '--imagefile', prompt='Image File:', help='图片路径')
def ocr(imagefile):
    """ 识别验证码（可作调试用） """
    succeed, result = theocr.imageOCR(imagefile)
    if succeed:
        print(f'识别成功，识别结果：{result}')
    else:
        print(f'识别失败，错误信息：{result}')
    return result


if __name__ == '__main__':
    main()
