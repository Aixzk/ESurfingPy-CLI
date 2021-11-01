# ESurfingPy-CLI

------

## 简介

基于 Python 实现登录和登出广东天翼校园网网页认证的命令行工具。可以用该工具来快速登录或登出广东天翼校园网，或者反复重新登录来重置限速状态，以 “破解” 限速。

![4S13ct.png](https://z3.ax1x.com/2021/09/11/4S13ct.png)

<br />

## 动图演示

![效果演示动图](https://z3.ax1x.com/2021/09/24/4DjH8U.gif)

<br />

## 适用学校

> 小道消息，广东天翼校园网于2021年10月20日，凌晨期间“优化”了校园网，实则是关闭了部分学校的网页认证通道。一些学校原本只是前端网页删除或屏蔽了登录相关组件的学校，其实还是可以使用类似此项目相关的基于网页认证的程序实现网页登录，但关闭认证通道后就彻底用不了（提示 `已办理一人一号多终端业务的用户，请使用客户端登录` 或 `当前该账号的拨号方式错误` ）。此项目不再适用于这些学校，目前只适用于没有关闭网页认证通道的广东天翼校园网。

如果你的学校校园网是广东天翼校园网，欢迎使用并反馈项目适用情况：[discussion#3](https://github.com/Aixzk/ESurfingPy-CLI/discussions/3)

<br />

## 下载运行

+ 如果要运行已经编译好的可执行文件，无需安装任何第三方程序。可以在 [Releases(发行版)](https://github.com/Aixzk/ESurfingPy-CLI/releases) 中找到最新编译的可执行文件，目前仅编译了 Win 平台的，其他平台的可以自行编译。
+ 如果要运行此项目的 python 文件，需要安装包括但不仅限于以下模块：

执行以下命令安装第三方模块，Linux 可能需要将 `pip` 换成 `pip3` ：

```
pip install click
pip install psutil
pip install ddddocr
pip install PyExecJS
pip install requests
```

网络不畅通可以用豆瓣镜像源等国内镜像源，例如：

````
pip install click -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
````

其他的模块替换上述命令中的 `click` 即可。

<br />

## 参数说明

设备刚连上校园网络时自动弹出的，或者已经连上但未登录时打开任意网页跳转到下面这个登录网页，其中有此程序要的参数：

![4S1YB8.png](https://z3.ax1x.com/2021/09/11/4S1YB8.png)

1. `ESurfingURL` ：校园网登录网址（部分），需要带端口。未登录时可能会出现域名解析错误（未能连接DNS服务器），可以先手动登录校园网后，使用 ping 等网络工具解析，然后用 `IP:端口` 代替，例如：`125.88.59.131:10001`
2. `WlanACIP` ：校园网的认证服务器IP，应该每个学校都不同；
3. `WlanUserIP` ：要登录的设备的IP，**可以不是本机的，实现远程登录**；
4. `Account` ：校园网账号
5. `Password` ：校园网账号的密码

<br />

## 命令行（CLI）

可以通过调用 main.py 或已经编译好的可执行文件（没有适合自己架构的可以自行编译）来快速使用。

```
./ESurfingPy-CLI.exe --help
Usage: ESurfingPy-CLI.exe [OPTIONS] COMMAND [ARGS]...

  基于 Python 实现登录和登出广东天翼校园网网页认证通道的命令行工具。

Options:
  --help  Show this message and exit.

Commands:
  auto    多种模式触发重登校园网
  login   发送 GET 请求登录校园网
  logout  发送 POST 请求登出校园网
  ocr     识别验证码（可作调试用）
```

### 登录

``` 
./ESurfingPy-CLI.exe login --help
Usage: ESurfingPy-CLI.exe login [OPTIONS]

  发送 GET 请求登录校园网

Options:
  -url, --esrfingurl TEXT     校园网登录网址
  -acip, --wlanacip TEXT      认证服务器IP
  -userip, --wlanuserip TEXT  登录设备IP
  -acc, --account TEXT        账号
  -pwd, --password TEXT       密码
  -details BOOLEAN            输出详细过程
  -debug BOOLEAN              调试模式
  --help                      Show this message and exit.
```

**本机登录校园网的话，`-url`, `-acip`, `-userip` 可以不填，程序会尝试自动获取。**

示例：`./ESurfingPy-CLI.exe login -url 125.88.59.131:10001 -acip 123.123.123.123 -userip 234.234.234.234 -acc 15012341234 -pwd 12345678 -details true`

### 登出

```
./ESurfingPy-CLI.exe logout --help
Usage: ESurfingPy-CLI.exe logout [OPTIONS]

  发送 POST 请求登出校园网

Options:
  -url, --esrfingurl TEXT     校园网登录网址
  -acip, --wlanacip TEXT      认证服务器IP
  -userip, --wlanuserip TEXT  登录设备IP
  -acc, --account TEXT        账号
  -pwd, --password TEXT       密码
  -sign, --signature TEXT     签名
  -details BOOLEAN            输出详细过程
  -debug BOOLEAN              调试模式
  --help                      Show this message and exit.
```

登出需要 `signature` ，不需要 `password`，因此填了签名可以不填密码；

但是如果没有签名，可以不填签名，填密码，程序会尝试登陆来获取 `signature` 然后再登出。

`signature` 可以登录获得（即使重复登录），可以自己写程序将登录时返回的 `signature` 保存下来，需要时再读取使用。

示例：`./ESurfingPy-CLI.exe logout -url 125.88.59.131:10001 -acip 123.123.123.123 -userip 234.234.234.234 -acc 15012341234 -sign XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX -details true`

### 识别验证码

``` ESurfingPy-CLI.exe ocr --help
Usage: ESurfingPy-CLI.exe ocr [OPTIONS]

  识别验证码（可作调试用）

Options:
  -img, --imagefile TEXT  图片路径
  --help                  Show this message and exit.
```

示例：

识别当前目录下的 code.png ：`./ESurfingPy-CLI.exe ocr -img code.png`

### 多种模式自动重登

```
./ESurfingPy-CLI.exe auto --help
Usage: ESurfingPy-CLI.exe auto [OPTIONS]

  多种模式触发重登校园网

Options:
  -m, --mode TEXT             触发模式
  -v, --value TEXT            触发网速(MB/s)或流量(MB)或时间(s)
  -as, --autostop BOOLEAN     自动停止
  -url, --esrfingurl TEXT     校园网登录网址
  -acip, --wlanacip TEXT      认证服务器IP
  -userip, --wlanuserip TEXT  登录设备IP
  -acc, --account TEXT        账号
  -pwd, --password TEXT       密码
  -details BOOLEAN            输出详细过程
  -debug BOOLEAN              调试模式
  --help                      Show this message and exit.
```

触发模式：

| 值   | 说明                                                         |
| ---- | ------------------------------------------------------------ |
| 1    | 实时监控**上传**速率（MB/s），连续 10s 低于指定值时自动重登校园网。 |
| 2    | 实时监控**下载**速率（MB/s），连续 10s 低于指定值时自动重登校园网。 |
| 3    | 实时监控**上传**流量（MB），达到指定值时自动重登校园网。     |
| 4    | 实时监控**下载**流量（MB），达到指定值时自动重登校园网。     |
| 5    | 每间隔指定的时间（s）自动重登校园网。                        |
| 6    | 手动回车后重登校园网。                                       |

示例：

+ 实时监控上传速率，连续 10s 低于 3MB/s 时自动重登：

`./ESurfingPy-CLI.exe auto -m 1 -v 3 -as true -url 125.88.59.131:10001 -acip 123.123.123.123 -userip 234.234.234.234 -acc 15012341234 -pwd 12345678 -details true`

+ 实时监控下载流量，达到 600MB 时自动重登：（-as 在此无效，随意输入就行）

`./ESurfingPy-CLI.exe auto -m 4 -v 600 -as true -url 125.88.59.131:10001 -acip 123.123.123.123 -userip 234.234.234.234 -acc 15012341234 -pwd 12345678 -details true`

<br />

## 应用示例

### 1. Win10 快速一键登录/登出

利用快捷方式，可以实现带参数启用程序：

![4S1dhj.png](https://z3.ax1x.com/2021/09/11/4S1dhj.png)

记得不要移动原文件，否则快捷方式会不可用。

### 2. Win10 开机自动登录校园网

根据上一个制作一个登录的快捷方式，然后按下 `Win` + `R` 输入 `shell:startup` 并确定，将登录的快捷方式拖进弹出的窗口，如果杀毒软件提示有程序想自启就点允许就可以了。

### 3. 更多

你可以自己开发程序，设定特定条件后调用此程序，来实现更多的功能等等……

<br />

## 框架

以下是各个 py 文件的作用：

- `main.py` - 提供命令行功能；
- `ESurfingPy.py` - 实现登录和登出校园；
- `theocr.py` - 识别验证码；
- `RSA.py` - 拼接并 RSA 加密文本；
- `Auto.py` - 自动模式；

例如想修改验证码的识别方法，可以编辑 `theocr.py` 文件。

<br />

## 不足

登录校园网过程中需要将 `账号`、`密码`和`验证码` 三者拼接后经 RSA 加密计算得到 `loginkey` 发送到服务器请求登录，但我不懂 RSA 加密算法，因此项目通过将校园网的实现 RSA 加密的原 js 文件魔改后，使用 `execjs` 模块传参执行 js 来获得 `loginkey`，缺点是效率可能会低一点。欢迎 PR 更好的计算方法！

<br />

## 其他

如果此项目对你有帮助，求点个 ★ ！

项目QQ群讨论群：791455104

