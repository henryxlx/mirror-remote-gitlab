import os
import shutil

import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    # 'Authorization': 'token c5696f17d1eac9598f1bc633fb93bca8ee707894'
}

DEFAULT_GITEA_HOST_URL = 'http://localhost:3000'
DEFAULT_GITEA_LOGIN_NAME = 'xulixin'
DEFAULT_GITEA_LOGIN_PWD = 'mfsslsm'
DEFAULT_LOCAL_MIRROR_ROOT_PATH = 'test-local-mirror-dir'  # 当前程序所在目录的子目录作为镜像的测试默认目录


class GiteaProjectMirrorHandler:
    """ 使用Gitea API对Gitea中的仓库和用户进行镜像处理"""

    def __init__(self, gitea_host_url=DEFAULT_GITEA_HOST_URL, login_name=DEFAULT_GITEA_LOGIN_NAME,
                 login_password=DEFAULT_GITEA_LOGIN_PWD):

        self.__gitlab_projects = []
        self.gitlab_api_project_fetcher = None
        self.gitea_host_url = gitea_host_url
        self.__gitea_api_base_url = gitea_host_url + '/api/v1'
        self.gitea_login_name = login_name
        self.gitea_login_password = login_password
        self.__basicAuth = (login_name, login_password)
        self.local_mirror_root_path = DEFAULT_LOCAL_MIRROR_ROOT_PATH
        self.label_message = None

    def __log_work_info(self, message):
        if self.label_message:
            self.label_message.set_label_text(message)
        print(message)

    def __get_gitlab_projects(self):
        if not self.__gitlab_projects and self.gitlab_api_project_fetcher:
            self.__gitlab_projects = self.__gitlab_projects = self.gitlab_api_project_fetcher.get_all_projects()
        return self.__gitlab_projects

    def check_gitea_server_active(self):
        self.__log_work_info('Detect Gitea server connected. It takes long time...')
        try:
            requests.get(self.gitea_host_url, headers=headers, timeout=3)
            return True
        except requests.exceptions.ConnectionError:
            self.__log_work_info('Can not connection Gitlab server. using local cache file.')
            return False

    def has_user_exist(self, username):
        get_user_api_url = self.__gitea_api_base_url + '/users/' + username
        api_resp = requests.get(get_user_api_url, headers=headers, auth=self.__basicAuth)
        if api_resp.status_code == 200:
            user_json = api_resp.json()
            if user_json:
                return True
        else:
            self.__log_work_info('Not exists user: ' + username)

        return False

    def has_repo_exist(self, repo_url):
        api_resp = requests.get(repo_url, headers=headers, auth=self.__basicAuth)
        if api_resp.status_code == 200:
            repo_json = api_resp.json()
            if repo_json:
                return True
        else:
            self.__log_work_info('Not exists repo: ' + repo_url)

        return False

    def delete_project_and_user_by_api(self):
        user_list = []
        for row in self.__get_gitlab_projects():
            repo_path = row['path_with_namespace']
            arr_repo_path = repo_path.split('/')
            username = arr_repo_path[0]
            if username not in user_list:
                user_list.append(username)

            repo_name = arr_repo_path[1]
            if self.has_repo_exist(self.__gitea_api_base_url + '/repos/' + username + '/' + repo_name):
                api_resp = requests.delete(self.__gitea_api_base_url + '/repos/' + username + '/' + repo_name,
                                           headers=headers, auth=self.__basicAuth)
                if api_resp.status_code == 204:
                    self.__log_work_info('Gitea respository has deleted: ' + repo_name)
                else:
                    self.__log_work_info('Fail to delete gitea repository: ' + repo_name)

        for username in user_list:
            if self.has_user_exist(username):
                api_resp = requests.delete(self.__gitea_api_base_url + '/admin/users/' + username,
                                           headers=headers, auth=self.__basicAuth)
                if api_resp.status_code == 204:
                    self.__log_work_info('Delete user: ' + username)
                else:
                    self.__log_work_info('Fail to delete user: ' + username)

    def create_user_by_api(self, username):
        if self.has_user_exist(username):
            return True

        post_create_user_api_url = self.__gitea_api_base_url + '/admin/users'
        data_form = {'email': username + '@jsyy.com', 'password': 'test123', 'username': username}
        api_resp = requests.post(post_create_user_api_url, data=data_form, headers=headers, auth=self.__basicAuth)
        if api_resp.status_code == 201:
            self.__log_work_info('Add new user: ' + username)
            return True

        return False

    def create_user_with_project_by_api(self):
        user_dict = {}
        for row in self.__get_gitlab_projects():
            repo_path = row['path_with_namespace']
            arr_repo_path = repo_path.split('/')
            username = arr_repo_path[0]
            if username not in user_dict:
                if self.create_user_by_api(username):
                    user_dict[username] = username
                else:
                    continue

            repo_name = arr_repo_path[1]
            if self.has_repo_exist(self.__gitea_api_base_url + '/repos/' + username + '/' + repo_name):
                self.__log_work_info('Waring: Gitea repository is exists: ' + repo_name)
                continue

            post_create_repo_api_url = self.__gitea_api_base_url + '/admin/users/' + username + '/repos'
            data_form = {'default_branch': 'main', 'description': repo_name, 'name': repo_name}
            api_resp = requests.post(post_create_repo_api_url, data=data_form, headers=headers, auth=self.__basicAuth)
            if api_resp.status_code == 201:
                self.__log_work_info('Create gitea new project repository: ' + repo_name)
            else:
                self.__log_work_info('Error: Create gitea repository ' + repo_name + str(api_resp.status_code) + api_resp.text)

    def create_mirror_path(self, local_mirror_path=DEFAULT_LOCAL_MIRROR_ROOT_PATH):
        if local_mirror_path != self.local_mirror_root_path:
            self.local_mirror_root_path = local_mirror_path

        project_local_mirror_path = local_mirror_path + '/git-repos-local-mirror/{0}/{1}'
        self.__log_work_info('Starting create mirror gitlab local mirror path...')
        for row in self.__get_gitlab_projects():
            repo_path = row['path_with_namespace']
            arr_repo_path = repo_path.split('/')
            owner_name = arr_repo_path[0]
            project_name = arr_repo_path[1]
            if not project_name.endswith('.git'):
                project_name = project_name + '.git'
            project_path = project_local_mirror_path.format(owner_name, project_name)
            if not os.path.exists(project_path):
                os.makedirs(project_path)
                self.__log_work_info('Create folder: ' + project_path)
            else:
                self.__log_work_info('Folder exists: ' + project_path)

        # 复制更新本地Git镜像文件DOS/Windows批处理文件到本地Git镜像文件夹
        bat_filename = '/update-local-mirror-gitea-remote.bat'
        shutil.copyfile(os.getcwd() + bat_filename, local_mirror_path + bat_filename)
