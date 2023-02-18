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

首先在Windows 10系统中安装Git

```
Give the example
```

然后安装Python

```
Give the example
```

上述软件安装完成后，从Gitee或Github仓库中下载本软件源代码，具体使用方法如下：

```
until finished
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