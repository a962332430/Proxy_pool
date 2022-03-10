# Proxy_pool
`https://github.com/a962332430/Proxy_pool`
``https://blog.csdn.net/weixin_44613063/article/details/102538757``
### 安装MySQL

安装好之后将MySQL服务开启

#### 安装依赖

```
pip3 install -r requirements.txt
```

#### 打开代理池和API

运行 run.py

#### 定时测活逻辑
- 每次爬虫后初始化为10分
- 定时测活，ping通过置为满分30分
- 定时测活，ping超时时每次扣10分
- 当扣分后分数为0分清除该代理
