# fastweixin

#### 介绍
快速使用微信的工具集

#### 软件架构
软件架构说明


#### 安装教程

1.  pip安装
```shell script
pip install fastweixin
```
2.  pip安装（使用阿里云镜像加速）
```shell script
pip install fastweixin -i https://mirrors.aliyun.com/pypi/simple
```


#### 使用说明

1.  demo
```python
import fastweixin
res = fastweixin.login_info('aaa', 'bbb')
```

2. account_state状态整理
```text
-2: invalid session（请重试）
-1：帐号/密码错误
0：帐号正常
1：帐号迁移
2：帐号永封
4：帐号注销
```
