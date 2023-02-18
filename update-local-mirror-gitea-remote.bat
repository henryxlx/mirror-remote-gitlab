@echo off
echo ================================================================================
echo * �����������Ŀ¼git-repos-local-mirror��¡Զ��Gitlab�ı���Git����ֿ⣬ͬʱͬ�����͵�Gitea��������Ӧ�ֿ�
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