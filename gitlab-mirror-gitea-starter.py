from tkinter import *
from tkinter import messagebox, filedialog

from gitlab_api_project_fetcher import GitlabApiProjectFetcher
from gitea_project_mirror_handler import GiteaProjectMirrorHandler


class LabelMessageUpdater:

    def __init__(self, tk_root, label_str_var):
        self.__tkRoot = tk_root
        self.__labelStringVar = label_str_var

    def set_label_text(self, text):
        self.__labelStringVar.set(text)
        self.__tkRoot.update()


def choose_local_mirror_dir():
    selected_folder = filedialog.askdirectory()
    if selected_folder != '':
        str_var_gitlab_local_mirror_dir.set(selected_folder)


def on_create_local_mirror_path():
    btn_create_local_mirror_path.config(state=DISABLED)
    verify_gitlab_gitea_config()
    mirror_handler.create_mirror_path(str_var_gitlab_local_mirror_dir.get())
    messagebox.showinfo("信息", "本地Git镜像目录结构建立成功！")
    btn_create_local_mirror_path.config(state=NORMAL)


def on_delete_gitea_user_and_project():
    btn_delete_gitea_user_and_project.config(state=DISABLED)
    if messagebox.askyesno("提示", "你确定要删除Gitea服务器中的仓库和用户信息吗？"):
        verify_gitlab_gitea_config()
        if mirror_handler.check_gitea_server_active():
            mirror_handler.delete_project_and_user_by_api()
            messagebox.showinfo("信息", "清除Gitea中的仓库与用户信息成功！")
        else:
            messagebox.showerror("错误", '操作失败！无法访问Gitea服务器.')
    btn_delete_gitea_user_and_project.config(state=NORMAL)


def on_create_gitea_user_project_by_gitlab():
    btn_mirror.config(state=DISABLED)
    verify_gitlab_gitea_config()
    if mirror_handler.check_gitea_server_active():
        mirror_handler.create_user_with_project_by_api()
        messagebox.showinfo("信息", "Gitea镜像Gitlab仓库与用户信息成功！")
    else:
        messagebox.showerror("错误", '操作失败！无法访问Gitea服务器.')
    btn_mirror.config(state=NORMAL)


def verify_gitlab_gitea_config():
    if str_var_gitlab_host_url.get() != fetcher.gitlab_host_url:
        fetcher.reset_gitlab_server().gitlab_host_url = str_var_gitlab_host_url.get()

    gitlab_api_private_token = str_var_gitlab_api_private_token.get()
    if len(gitlab_api_private_token) > 0 and gitlab_api_private_token != fetcher.api_private_token:
        fetcher.reset_gitlab_server().api_private_token = gitlab_api_private_token

    if str_var_gitea_host_url.get() != mirror_handler.gitea_host_url:
        mirror_handler.reset_gitea_server().gitea_host_url = str_var_gitea_host_url.get()

    if str_var_gitea_login_name.get() != mirror_handler.gitea_login_name:
        mirror_handler.reset_gitea_server().gitea_login_name = str_var_gitea_login_name.get()

    if str_var_gitea_login_password.get() != mirror_handler.gitea_login_password:
        mirror_handler.reset_gitea_server().gitea_login_password = str_var_gitea_login_password.get()


fetcher = GitlabApiProjectFetcher()
mirror_handler = GiteaProjectMirrorHandler()
mirror_handler.gitlab_api_project_fetcher = fetcher

root = Tk()
i = 0

# 第一行，Gitlab服务器地址标签及输入框
lbl_gitlab_host_url = Label(root, text='Gitlab服务器地址：')
lbl_gitlab_host_url.grid(row=i, sticky=W)
str_var_gitlab_host_url = StringVar()
entry_gitlab_host_url = Entry(root, width=46, textvariable=str_var_gitlab_host_url)
str_var_gitlab_host_url.set(fetcher.gitlab_host_url)
entry_gitlab_host_url.grid(row=i, column=1, sticky=E)

i = i + 1
# 第二行，Gitlab API访问令牌标签及输入框
lbl_gitlab_api_private_token = Label(root, text='Gitlab API访问令牌：')
lbl_gitlab_api_private_token.grid(row=i, sticky=W)
str_var_gitlab_api_private_token = StringVar()
entry_gitlab_api_private_token = Entry(root, width=46, textvariable=str_var_gitlab_api_private_token)
entry_gitlab_api_private_token.grid(row=i, column=1, sticky=E)

i = i + 1
# 空行
lbl_blank = Label(root, text='')
lbl_blank.grid(row=i, sticky=W)

i = i + 1
# 第四行，Git本地镜像根目录/文件夹标签及输入框
lbl_gitlab_local_mirror_dir = Label(root, text='Git本地镜像根目录/文件夹：')
lbl_gitlab_local_mirror_dir.grid(row=i, sticky=W)
str_var_gitlab_local_mirror_dir = StringVar()
entry_gitlab_local_mirror_dir = Entry(root, width=46, textvariable=str_var_gitlab_local_mirror_dir)
str_var_gitlab_local_mirror_dir.set(mirror_handler.local_mirror_root_path)
entry_gitlab_local_mirror_dir.grid(row=i, column=1, sticky=E)
btn_choose_dir = Button(root, text='...', command=choose_local_mirror_dir)
btn_choose_dir.grid(row=i, column=2, sticky=E)

i = i + 1
# 按扭，command绑定事件
btn_create_local_mirror_path = Button(root, text='获取Gitlab项目信息创建Git本地镜像目录结构', command=on_create_local_mirror_path)
btn_create_local_mirror_path.grid(row=i, column=1, sticky=W)

i = i + 1
# 空行
lbl_blank = Label(root, text='')
lbl_blank.grid(row=i, sticky=W)

i = i + 1
# 第五行，Gitea镜像服务器地址标签及输入框
lbl_gitea_host_url = Label(root, text='Gitea镜像服务器地址：')
lbl_gitea_host_url.grid(row=i, sticky=W)
str_var_gitea_host_url = StringVar()
entry_gitea_host_url = Entry(root, width=46, textvariable=str_var_gitea_host_url)
str_var_gitea_host_url.set(mirror_handler.gitea_host_url)
entry_gitea_host_url.grid(row=i, column=1, sticky=E)

i = i + 1
# 第六行，Gitea登录用户名标签及输入框
lbl_gitea_login_name = Label(root, text='Gitea登录用户名：')
lbl_gitea_login_name.grid(row=i, sticky=W)
str_var_gitea_login_name = StringVar()
entry_gitea_login_name = Entry(root, textvariable=str_var_gitea_login_name)
str_var_gitea_login_name.set(mirror_handler.gitea_login_name)
entry_gitea_login_name.grid(row=i, column=1, sticky=W)

i = i + 1
# 第七行，Gitea登录密码标签及输入框
lbl_gitea_login_password = Label(root, text='Gitea登录密码：')
lbl_gitea_login_password.grid(row=i, sticky=W)
str_var_gitea_login_password = StringVar()
entry_gitea_login_password = Entry(root, textvariable=str_var_gitea_login_password)
str_var_gitea_login_password.set(mirror_handler.gitea_login_password)
entry_gitea_login_password.grid(row=i, column=1, sticky=W)

i = i + 1
# 删除Gitea中用户与仓库信息按扭，command绑定事件
btn_delete_gitea_user_and_project = Button(root, text='清除Gitea仓库与用户信息，慎用！', command=on_delete_gitea_user_and_project)
btn_delete_gitea_user_and_project.grid(row=i, sticky=E)

i = i + 1
# Gitlab与Gitea用户与仓库信息同步按扭，command绑定事件
btn_mirror = Button(root, text='Gitea镜像Gitlab仓库与用户信息', command=on_create_gitea_user_project_by_gitlab)
btn_mirror.grid(row=i, column=1, sticky=E)

i = i + 1
# 操作过程中输出信息提示
str_var_process_msg = StringVar()
lbl_process_msg = Label(root, textvariable=str_var_process_msg)
lbl_process_msg.grid(row=i, columnspan=2, sticky=W)
labelMessageUpdater = LabelMessageUpdater(root, str_var_process_msg)

mirror_handler.label_message = labelMessageUpdater
fetcher.label_message = labelMessageUpdater
root.mainloop()
