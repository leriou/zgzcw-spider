抓取中国足彩网的足球比赛赔率

提供常用的数据抓取工具

# 介绍

`bilibili_main.py`: 抓取哔哩哔哩用户的个人信息页面数据

`fzdm_main.py`: 抓取风之动漫网站的动漫数据

`main.py`: 抓取中国足彩网的数据

# 安装

## 依赖

1. 浏览器驱动

使用了`selenium`来做页面上的js解析, 所以需要一个浏览器驱动,Chrome或者firefox都行

`chromedriver`: 谷歌浏览器驱动
或
`geckodriver`: 火狐浏览器驱动

下载完成以后,放到系统环境变量里面就行了,可以放到 `/usr/bin`下面

2. mongodb数据库

`brew install mongodb`: 安装mongodb,使用mongodb作为基础数据库

抓取的中间数据和解析过后的数据都使用mongodb进行存储

3. pipenv

`git clone`  下载项目

`cd zgzcw_spider`:   进入项目目录

`pip install pipenv`:  安装pipenv

`pipenv install`:  安装依赖

`pipenv run python3 main.py`: 运行抓取中国足彩网的数据的代码

## usage

`pipenv run python3 bilibili_main.py 123 ` 抓取bilibili用户123的数据

`pipenv run python3 fzdm_main.py 进击的巨人` 抓取进击的巨人动画的数据

`pipenv run python3 main.py 2018-01-07`