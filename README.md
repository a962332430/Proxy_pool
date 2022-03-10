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
- 首次爬虫通过给初试分数30分
- 定时测活，ping通过+10分
- 定时测活，ping超时-20分
- 当扣分后分数小于等于0分剔除
- 稳定代理阈值：90分，即超过90分可以认定为稳定
