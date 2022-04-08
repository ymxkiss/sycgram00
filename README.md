# sycgram

## 安装与更新

```shell
# 脚本的【安装】都是前台运行，完成安装后如无报错可先后使用Ctrl+P、Ctrl+Q挂到后台运行
bash <(curl -fsL "https://raw.githubusercontent.com/iwumingz/sycgram/main/install.sh")
```



## 迁移备份

1. 停止容器
2. 打包`/opt/sycgram`文件夹到新环境相同位置
3. 在新环境运行sycgram管理脚本



## 自定义指令前缀及指令别名

- 每次通过脚本更新【建议v1.1.0版本后使用指令更新】都会覆盖本地的`command.yml`，原文件会备份到`command目录`
- 可以通过指令修改前缀和别名
- 指令别名只支持单别名和源名（不再支持多别名）



## 注意事项

- 脚本仅适用于Ubuntu/Debian，其它系统自行解决~
- 按个人需求随缘更，仅用于学习用途
- 如果号码等输入错误了，重新安装即可
