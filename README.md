# Mirror Gitlab 是什么

本项目是将Gitlab服务器上的源代码仓库迁移到Gitea服务器，并保持同步的小工具

## 原理

主要利用Git的镜像功能，将Gitlab服务器上的源代码仓库先克隆到本地，然后再镜像到Gitea服务器上

## 主要技术

Git 命令操作（git mirror, remote, push...
DOS/Windows批处理文件
Python 调用Gitlab和Gitea的API，同步两个服务器的用户与项目信息

## 使用方法

首先运行Python程序同步Gitlab和Gitea服务器上的用户和项目信息，同时在本地建立Git镜像的目录结构

### 环境要求

使用本工具你机器必须是Windows操作系统，并提前安装git软件包和Python环境

```
Windows 10
Git for windows 2.x
PYthon 3.8 及以上版本
```

### 工具使用环境安装

下面是使用Git和Python软件的安装过程

首先在Windows 10系统中安装Git, 可以直接使用Git网站提供的便捷的压缩包文件64-bit Git for Windows Portable.
下载地址：https://git-scm.com/download
国内镜像：https://registry.npmmirror.com/binary.html?path=git-for-windows/
```
下载后，解压缩到D:\git目录，
然后在Windows环境变量定义GIT_HOME=D:\git
在Windows搜索路径变量添加Git可执行文件的目录bin，使用GIT_HOME变量定义搜索路径为%GIT_HOME%\bin
```

然后安装Python，首先下载Python在Windows环境下的安装程序.
下载地址：
国内镜像：https://registry.npmmirror.com/binary.html?path=python/

```
执行安装程序，例如安装到C:\python\python3
同样定义Windows环境变量PYTHON_HOME=C:\python\python3
在Windows搜索路径变量添加Python可执行文件所在的目录，搜索路径值为%PYTHON_HOME%，因为python.exe在安装根目录下
```

上述软件安装完成后，从Gitee仓库（https://gitee.com/henryxpx/mirror-remote-gitlab.git）中下载本软件源代码开始Gitlab与Gitea的镜像，具体使用方法如下：

```
进入到本软件的目录中，比如位于D:\mirror-remote-gitlab，运行python管理程序gitlab-mirror-gitea-starter.py
可以使用命令行方式执行：python gitlab-mirror-gitea-starter.py
在显示的图形界面中会出现镜像功能所需要的参数，其中有些内容显示程序的默认值，你的配置不同需要进行修改，修改的参数说明如下：
首先需要指定要镜像的Gitlab服务器的主机地址（带端口号）和Gitlab API访问需要的私有令牌（该令牌需要在Gitlab授权用户的管理后台设置）
Gitlab服务器地址：
Gitlab API访问令牌：
其次需要选择在Windows操作系统本地镜像的根目录，该目录根据Gitlab中的项目建立目录结构用于Git程序镜像Gitlab中的仓库
Git本地镜像根目录/文件夹：
上述参数定义好后点击《获取Gitlab项目信息创建Git本地镜像目录结构》按钮，在本机创建用于镜像源代码仓库的项目目录结构

下一步设置同步备份镜像的Gitea服务器参数，主要是Gitea服务器主机地址（带端口号)和登录Gitea服务器的管理员登录名称和密码：
Gitea镜像服务器地址
Gitea登录用户名
Gitea登录密码
然后点击《Gitea镜像Gitlab仓库与用户信息》按钮将Gitlab服务器中源代码仓库和用户的信息全部同步到Gitea服务器上。
这些操作都成功完成后，使用Windows系统命令行界面，进入到Python程序设置的”Git本地镜像根目录/文件夹“，
发现其中包含一个名字为update-local-mirror-gitea-remote.bat的批处理文件，
修改其中关于两个服务器SSH方式连接的用户名与地址，一切设置正确后执行此批处理文件则将Gitlab中源代码仓库中的代码同步到Gitea服务器中
至此就完成了Gitlab服务器到Gitea服务器源代码的迁移。如果后续Gitlab中的代码依然有新的提交，可重新执行此批处理程序就能继续更新代码
如果Gitlab服务器中新增加的仓库，则需要重新运行前面的Python程序，再次生成本地镜像目录和同步Gitlab和Gitea仓库的用户和项目信息
```

## Built With

* [PyCharm Community](https://www.jetbrains.com.cn/pycharm/download "PyCharm") - IDE for Python source code.

## Author

* **Lixin Xu** - *Initial work* - [xupeixuan cnblogs](https://www.cnblogs.com/xupeixuan/ "xupeixuan cnblogs")

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md "LICENSE.md") file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc