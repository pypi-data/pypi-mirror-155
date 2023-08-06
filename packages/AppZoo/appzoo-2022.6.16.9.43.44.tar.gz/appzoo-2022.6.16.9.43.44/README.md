[![Downloads](http://pepy.tech/badge/AppZoo)](http://pepy.tech/project/AppZoo)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/jie-yuan/appzoo/apps_streamlit/demo.py)

<h1 align = "center">:rocket: AppZoo :facepunch:</h1>

---



## Install
```bash
pip install -U appzoo
```
## Usage
- Rest Api
```python
import jieba
from appzoo import App

pred1 = lambda **kwargs: kwargs['x'] + kwargs['y']
pred2 = lambda x=1, y=1: x - y
pred3 = lambda text='小米是家不错的公司': jieba.lcut(text)

app = App(verbose=True)
app.add_route("/", pred1, result_key='result')
app.add_route("/f1", pred1, version="1")
app.add_route("/f2", pred2, version="2")
app.add_route("/f3", pred3, version="3")

app.run() # appcli easy-run ./apps
```

- 带缓存
```python
@lru_cache()
def post_func(kwargs: str):
    logger.info(kwargs)
    return kwargs


app.add_route_plus(post_func)
```

- Fast Api
```bash
app-run - fastapi demo.py
app-run - fastapi -- --help
```

- [Streamlit App](https://share.streamlit.io/jie-yuan/appzoo/apps_streamlit/demo.py)
```bash
app-run - streamlit demo.py
app-run - streamlit -- --help
```


---
## TODO
- add logger: 采样
- add scheduler
- add 监听服务
- add rpc服务
    - hive等穿透
- add thrift https://github.com/Thriftpy/thriftpy2
- add dataReport
- add plotly
- add explain
---

对于RESTful API的URL具体设计的规范如下：
1.不用大写字母，所有单词使用英文且小写。
2.连字符用中杠"-“而不用下杠”_"
3.正确使用 “/“表示层级关系,URL的层级不要过深，并且越靠前的层级应该相对越稳定
4.结尾不要包含正斜杠分隔符”/”
5.URL中不出现动词，用请求方式表示动作
6.资源表示用复数不要用单数
7.不要使用文件扩展名

---
[FastAPI--依赖注入之Depends](https://blog.csdn.net/shykevin/article/details/106834526)