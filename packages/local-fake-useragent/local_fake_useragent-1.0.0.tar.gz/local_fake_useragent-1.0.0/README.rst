# 这是一个本地版ua随机头, 不会出现请求超时等错误, 功能单一, 使用简单

## 更多精彩文章, 请关注 [ 不止于python ] 公众号

# 使用方法
```python
from local_fake_useragent import UserAgent
# 获取所有浏览器的随机请求头
u = UserAgent()

# 获取chrome的随机请求头
u = UserAgent("chrome")

# 添加自定义请求头
c = {
    "0": ["a", "b"]
}
u = UserAgent("0", add_custom_header=c)

print(u.rget)

# 支持的浏览器
print(UserAgent.BROWER)
```


# 测试用例
```python
import requests
from local_fake_useragent import UserAgent

uas = UserAgent()
headers = {'User-agent': uas.rget}
url = 'https://www.baidu.com'
response = requests.get(url=url, headers=headers)
response.encoding = response.apparent_encoding
print(response.text)
```