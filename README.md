抓取中国足彩网的足球比赛赔率

提供常用的数据抓取工具

# 介绍

`bilibili.py`: 抓取哔哩哔哩用户的个人信息页面数据

`fzdm.py`: 抓取风之动漫网站的动漫数据

`zgzcw.py`: 抓取中国足彩网的数据

# 安装(Mac OS)

## 依赖

1. 浏览器驱动

使用了`selenium`来做页面上的js解析, 所以需要一个浏览器驱动,Chrome或者firefox都行

`chromedriver`: 谷歌浏览器驱动(推荐, 速度比firefox快一点)
或
`geckodriver`: 火狐浏览器驱动

下载地址: http://npm.taobao.org/mirrors/chromedriver

下载完成以后,放到系统环境变量里面就行了,可以放到 `/usr/bin`下面

2. mongodb数据库

`brew install mongodb`: 安装mongodb,使用mongodb作为基础数据库

抓取的中间数据和解析过后的数据都使用mongodb进行存储

3. pip依赖

`git clone xxx`  下载项目

`cd zgzcw_spider`:   进入项目目录

`pip3 install -r requirements.txt`:  安装依赖

## Usage

`python3 main.py bilibili 123` 抓取bilibili用户123的数据

`python3 main.py fzdm 进击的巨人` 抓取进击的巨人动画的数据

`python3 main.py zgzcw 2018-01-07` 抓取某一天的彩票数据