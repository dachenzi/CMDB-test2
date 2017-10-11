import requests
from bs4 import BeautifulSoup

# requests 模拟浏览器发get请求
response = requests.get('https://www.cnblogs.com/')

# 把请求的结果以text显示，并交给Beautifulsoup来进行解析，需要指定解析方式为html
soup = BeautifulSoup(response.text, 'html.parser')

# 在解析的结果中寻找标签是title的text文本格式
title = soup.find('title').text

# 在解析的结果中寻找属性为name='description'的meta标签，获取他的content属性的值
desc = soup.find('meta', attrs={'name': 'description'}).get('content')

print(title)
print(desc)

if __name__ == '__main__':
    cpu_count, cpu_name = getcpuinfo()
    cpu_percent = getcpupercent()
    loadavg = getloadavg()
    MemTotal, MemFree, Mempercent = getmeminfo()
    disksize, diskused, diskaval, diskuse = getdiskinfo()
    hostname, hostip = hostinfo()
