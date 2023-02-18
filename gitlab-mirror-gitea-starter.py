from tkinter import *
from tkinter import messagebox, filedialog

from gitlab_api_project_fetcher import GitlabApiProjectFetcher
from gitea_project_mirror_handler import GiteaProjectMirrorHandler


class LabelMessageUpdater:

    def __init__(self, tk_root, label_text_var):
        self.__tkRoot = tk_root
        self.__labelTextVar = label_text_var

    def set_label_text(self, text):
        self.__labelTextVar.set(text)
        self.__tkRoot.update()


def choose_local_mirror_dir():
    selected_folder = filedialog.askdirectory()
    if selected_folder != '':
        es_gitlab_local_mirror_dir.set(selected_folder)


def on_create_local_mirror_path():
    b_create_local_mirror_path.config(state=DISABLED)
    mirror_handler.create_mirror_path(es_gitlab_local_mirror_dir.get())
    messagebox.showinfo("Info", "本地Git镜像目录结构建立成功！")
    b_create_local_mirror_path.config(state=NORMAL)


def on_delete_gitea_user_and_project():
    b_delete_gitea_user_and_project.config(state=DISABLED)
    mirror_handler.delete_project_and_user_by_api()
    messagebox.showinfo("Info", "清除Gitea中的仓库与用户信息成功！")
    b_delete_gitea_user_and_project.config(state=NORMAL)


def on_create_gitea_user_project_by_gitlab():
    b_mirror.config(state=DISABLED)
    mirror_handler.create_user_with_project_by_api()
    messagebox.showinfo("Info", "Gitea镜像Gitlab仓库与用户信息成功！")
    b_mirror.config(state=NORMAL)


fetcher = GitlabApiProjectFetcher()
mirror_handler = GiteaProjectMirrorHandler()
mirror_handler.gitlab_api_project_fetcher = fetcher

root = Tk()
i = 0

# 第一行，Git本地镜像根目录/文件夹标签及输入框
l_gitlab_local_mirror_dir = Label(root, text='Git本地镜像根目录/文件夹：')
l_gitlab_local_mirror_dir.grid(row=i, sticky=W)
es_gitlab_local_mirror_dir = StringVar()
e_gitlab_local_mirror_dir = Entry(root, width=46, textvariable=es_gitlab_local_mirror_dir)
es_gitlab_local_mirror_dir.set(mirror_handler.local_mirror_root_path)
e_gitlab_local_mirror_dir.grid(row=i, column=1, sticky=E)
b_choose_dir = Button(root, text='...', command=choose_local_mirror_dir)
b_choose_dir.grid(row=i, column=2, sticky=E)

i = i + 1
# 按扭，command绑定事件
b_create_local_mirror_path = Button(root, text='根据项目信息创建Git本地镜像目录结构', command=on_create_local_mirror_path)
b_create_local_mirror_path.grid(row=i, sticky=E)

i = i + 1
# 空行
l_blank = Label(root, text='')
l_blank.grid(row=i, sticky=W)

i = i + 1
# 第一行，Gitlab服务器地址标签及输入框
l_gitlab_host_url = Label(root, text='Gitlab服务器地址：')
l_gitlab_host_url.grid(row=i, sticky=W)
e = StringVar()
e_gitlab_host_url = Entry(root, width=46, textvariable=e)
e.set(fetcher.gitlab_host_url)
e_gitlab_host_url.grid(row=i, column=1, sticky=E)

i = i + 1
# 第二行，Gitlab API访问令牌标签及输入框
l_gitlab_api_token = Label(root, text='Gitlab API访问令牌：')
l_gitlab_api_token.grid(row=i, sticky=W)
e = StringVar()
e_gitlab_api_token = Entry(root, width=46, textvariable=e)
e_gitlab_api_token.grid(row=i, column=1, sticky=E)

i = i + 1
# 空行
l_blank = Label(root, text='')
l_blank.grid(row=i, sticky=W)

i = i + 1
# 第四行，Gitea镜像服务器地址标签及输入框
l_gitea_host_url = Label(root, text='Gitea镜像服务器地址：')
l_gitea_host_url.grid(row=i, sticky=W)
e = StringVar()
e_gitea_host_url = Entry(root, width=46, textvariable=e)
e.set(mirror_handler.gitea_host_url)
e_gitea_host_url.grid(row=i, column=1, sticky=E)

i = i + 1
# 删除Gitea中用户与仓库信息按扭，command绑定事件
b_delete_gitea_user_and_project = Button(root, text='>>>清除Gitea中的仓库与用户信息', command=on_delete_gitea_user_and_project)
b_delete_gitea_user_and_project.grid(row=i, sticky=E)

i = i + 1
# 第六行，Gitea登录用户名标签及输入框
l_gitea_login_name = Label(root, text='Gitea登录用户名：')
l_gitea_login_name.grid(row=i, sticky=W)
e = StringVar()
e_gitea_login_name = Entry(root, textvariable=e)
e.set(mirror_handler.get_login_name())
e_gitea_login_name.grid(row=i, column=1, sticky=W)

i = i + 1
# 第七行，Gitea登录密码标签及输入框
l_gitea_login_password = Label(root, text='Gitea登录密码：')
l_gitea_login_password.grid(row=i, sticky=W)
e = StringVar()
e_gitea_login_password = Entry(root, textvariable=e)
e.set(mirror_handler.get_login_password())
e_gitea_login_password.grid(row=i, column=1, sticky=W)

i = i + 1
# 空行
l_blank = Label(root, text='')
l_blank.grid(row=i, sticky=W)

i = i + 1
# Gitlab与Gitea用户与仓库信息同步按扭，command绑定事件
b_mirror = Button(root, text='Gitea镜像Gitlab仓库与用户信息', command=on_create_gitea_user_project_by_gitlab)
b_mirror.grid(row=i, column=1, sticky=E)

i = i + 1
# 操作过程中输出信息提示
ls_process_msg = StringVar()
l_process_msg = Label(root, textvariable=ls_process_msg)
l_process_msg.grid(row=i, columnspan=2, sticky=W)
labelMessageUpdater = LabelMessageUpdater(root, ls_process_msg)

mirror_handler.label_message = labelMessageUpdater
fetcher.label_message = labelMessageUpdater
root.mainloop()
