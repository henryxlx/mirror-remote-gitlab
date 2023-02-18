""" 本程序获取Gitlab仓库中的项目信息，有两种方法，一是对象方式的GitlabApiProjectFetcher通过私有Token方式访问API
另外一种是从保存项目API数据JSON格式文件中获取项目的全部信息 """

import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Accept-Language': 'zh_CN',
}

DEFAULT_GITLIB_HOST_URL = 'http://192.168.6.249:5580'
DEFAULT_GITLIB_API_PRIVATE_TOKEN = 'SGx1NZTzu8Vc35Rqpq3G'


class GitlabApiProjectFetcher:
    """ 使用Gitlab API获取仓库中全部项目的模块，创建GitlabApiProjectFetcher()可以提供最多两个参数：
    host是源代码仓库主机地址，api_private_token访问Gitlab的API需要的私有权限token
    调用get_all_projects方法可以获取仓库中全部的项目自定义简化的信息 """

    # 调试方式控制输出更多信息
    debug_mode = False

    __gitlib_server_active = None

    def __get_gitlab_server_active(self):
        if self.__gitlib_server_active is None:
            self.__log_work_info('Check Gitlab server is connected. It takes long time...')
            try:
                requests.get(self.apiUrl, headers=headers, timeout=3)
                self.__gitlib_server_active = True
            except requests.exceptions.ConnectionError:
                self.__log_work_info('Can not connection Gitlab server. using local cache file.')
                self.__gitlib_server_active = False

        return self.__gitlib_server_active

    def __init__(self, host=DEFAULT_GITLIB_HOST_URL, api_private_token=DEFAULT_GITLIB_API_PRIVATE_TOKEN):
        self.gitlab_host_url = host
        self.apiUrl = host + '/api/v4'
        self.api_private_token = api_private_token
        self.requestClient = requests
        self.label_message = None

    def __log_work_info(self, message):
        if self.label_message:
            self.label_message.set_label_text(message)
        print(message)

    # 根据Gitlab API访问项目分页的内容JSON化的数据条目生成自定义的项目并添加到自己的项目列表中
    def __add_project_list(self, projects, project_json_entries):
        for entry in project_json_entries:            
            project = {'description': entry['description'],
                       'name': entry['name'],
                       'default_branch': entry['default_branch'],
                       'path_with_namespace': entry['path_with_namespace']}
            projects.append(project)

    def get_all_projects(self):
        if self.__get_gitlab_server_active():
            return self.get_all_projects_by_gitlab_api()
        else:
            return self.get_projects_from_api_json_file()

    def get_all_projects_by_gitlab_api(self):
        """ 获取Gitlab仓库中的全部项目 """

        self.__log_work_info('Fetching projects from Gitlab server: ' + self.apiUrl)
    
        projects = []
        # Gitlab API访问使用用户定义的api_private_token才能访问
        get_project_by_page_api_url = self.apiUrl + '/projects?simple=true&page={0}&per_page=100&private_token=' + self.api_private_token
        page_count = 1  # 默认只访问第1页前100个项目

        # 访问Gitlab项目的API，检查能否获取分页页数
        resp = self.requestClient.get(get_project_by_page_api_url.format(1), headers=headers)
        self.__log_work_info('GET' + get_project_by_page_api_url.format(1) + 'Response Code:' + str(resp.status_code))
        self.__add_project_list(projects, resp.json())

        # 获取分页的页数，仓库项目数超过1万条则不提供总页数和总记录数
        if 'x-total-pages' in resp.headers:
            self.__log_work_info('总页数: X-Total-Pages' + resp.headers['x-total-pages'])
            self.__log_work_info('项目总数: X-Total' + resp.headers['x-total'])

        for page in range(2, page_count + 1):
            resp = self.requestClient.get(get_project_by_page_api_url.format(page), headers=headers)
            self.__log_work_info('GET' + get_project_by_page_api_url.format(page) + 'Response Code:' + str(resp.status_code))
            self.__add_project_list(projects, resp.json())
                
        if self.debug_mode:
            print(projects)    
        return projects

    def get_projects_from_api_json_file(self, filename='data4json/projects.json'):
        """ 读取预先保存的API获取的项目信息的JSON格式文件，返回其全部项目信息 """

        self.__log_work_info('Fetching projects from local cache file: ' + filename)
        with open(filename, 'r', encoding='utf-8') as jsonTextFile:
            return json.load(jsonTextFile)


if __name__ == '__main__':
    fetcher = GitlabApiProjectFetcher('http://192.168.6.249:5580')
    fetcher.debug_mode = True
    projects = fetcher.get_all_projects()
    print(projects)
