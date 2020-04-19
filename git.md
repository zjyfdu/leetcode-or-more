这里关于git的命令也记一下

```shell
git pull <远程库名> <远程分支名>:<本地分支名>  
git push <远程库名> <本地分支名>:<远程分支名>  

```
这里的`git push -u origin master` -u指定默认是origin

删除已经commit的文件，`git rm -r --cached _book/`