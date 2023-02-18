@echo off
echo ================================================================================
echo * 本程序更新子目录git-repos-local-mirror克隆远程Gitlab的本地Git镜像仓库，同时同步推送到Gitea服务器对应仓库
echo --------------------------------------------------------------------------------
setlocal enabledelayedexpansion
cd git-repos-local-mirror
for /f %%a in ('dir /ad /b .') do (
  echo Repository Project Owner: %%a
  cd %%a
  for /f %%i in ('dir /ad /b .') do (
    echo Staring update git remote origin of project: %%i
    cd %%i
    git remote update origin
    set gitea_repo_url="admin@localhost:%%a/%%i"
    echo Staring push mirror to gitea repo: !gitea_repo_url!
    git push --mirror !gitea_repo_url!
    cd ..
  )
  cd ..
)
cd ..
echo --------------------------------------------------------------------------------