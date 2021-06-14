@[TOC](使用nat123远程ssh连接WSL Ubuntu系统)

# Multivation

办公室安装了WSL2 Windows Subsystem for Linux的Ubuntu系统（安装方法参考：[适用于 Linux 的 Windows 子系统安装指南 (Windows 10)](https://docs.microsoft.com/zh-cn/windows/wsl/install-win10#for-anniversary-update-and-creators-update-install-using-lxrun)或者[WSL(Windows Subsystem for Linux)的安装与使用](https://www.jianshu.com/p/1da2ef53497e)），然而我想在家也能连接到办公室的电脑进行工作，怎么才能从外网访问这台内网的电脑呢？


# 给WSL开启ssh服务
[参考这里](https://blog.csdn.net/yuyuena/article/details/108335464) 或者 [这里](https://www.bilibili.com/read/cv5170803/)。

#安装openssh-server

```
sudo apt remove openssh-server
sudo apt install openssh-client openssh-server
```

#备份原始的sshd_config

```
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
sudo cp /etc/ssh/ssh_config /etc/ssh/ssh_config.bak
```

#使用vim进行编辑，按i进入insert模式

```
sudo vim /etc/ssh/sshd_config
```

在vim中*找到* 对应项并修改，ESC，输入`:wq`保存退出：

> 	Port 222
>  PasswordAuthentication yes    # 将 no 改为 yes 表示使用帐号密码方式登录
> 	ListenAddress 0.0.0.0        #如果需要指定监听的IP则去除最左侧的井号，并配置对应IP，默认即监听PC所有IP 	
> PermitRootLogin no        # 如果你需要用 root 直接登录系统则此处改为 yes

#启动ssh，查看status

```
sudo service ssh start             #启动SSH服务
sudo service ssh status            #检查状态
```
重启WSL后启用ssh服务。

```
sudo service ssh --full-restart
```
查看ip

```
ifconfig
```
我使用127.0.0.1这个地址。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210530043122962.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDc1MjEx,size_16,color_FFFFFF,t_70#pic_center)
Windows防火墙设置:

因为在前面设置的ssh端口是222（22端口在Windows下有其他占用了），所以还需要去防火墙中设置一下这个端口的拨入，win+防火墙，进入防火墙页面，按如下操作：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210530043313683.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDc1MjEx,size_16,color_FFFFFF,t_70#pic_center)
操作：
```
端口–>TCP–>特点本地端口222–>允许连接–>下一步确定；设置完成。
```

# 测试一下SSH能不能连接
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210530043534573.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDc1MjEx,size_16,color_FFFFFF,t_70#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210530043627202.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDc1MjEx,size_16,color_FFFFFF,t_70#pic_center)

这样就可以在本机用ssh连接WSL系统了。

# 外网ssh访问WSL（nat123）
按照这个步骤完成：http://www.nat123.com/Pages_23_540.jsp ，其中注意，添加映射的时候请参考我是这样做的：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210530044046262.jpeg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDc1MjEx,size_16,color_FFFFFF,t_70#pic_center)
另注意：访问者添加访问端口的时候是222。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210530044259996.png#pic_center)
现在，在访问者电脑（我家）中，ssh连接上图的访问域名和访问端口，就能控制办公室的WSL了。

# WSL自动启动ssh服务
由于每次打开WSL都要手动启动ssh服务（sudo service ssh --full-restart），解决这个问题请参考：[win10子系统 wsl开机启动ssh服务
](https://blog.csdn.net/shenbururen/article/details/106133150)

这样，只要同事打开办公室电脑的WSL和nat123，我就能在家ssh控制了。
