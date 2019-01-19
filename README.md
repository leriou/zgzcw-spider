抓取中国足彩网的足球比赛赔率

提供常用的数据抓取工具

# 介绍

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

`python3 main.py 2018-01-07` 抓取某一天的彩票数据

## Data

抓取到的数据例子:

```json
{
    "_id": "5c31e1f13b7750c3442e9c8f",
    "competition": "天皇杯",
    "list_url": "http://cp.zgzcw.com/lottery/jchtplayvsForJsp.action?lotteryId=47&type=jcmini&issue=2017-01-01",
    "match_start_time": "2017-01-01 12:50",
    "match_date": "比赛时间：2017-01-01 13:00:00",
    "hostname": "鹿岛鹿角",
    "visitname": "川崎前锋",
    "match_score_source": "1:1",
    "host_score": "1",
    "visit_score": "1",
    "match_result": 1,
    "created_time": "2019-01-06 19:08:55",
    "bjop": {
        "id": "2191207",
        "url": "http://fenxi.zgzcw.com/2191207/bjop"
    },
    "odds": {
        "0": {
            "rq": "0",
            "odds": false
        },
        "-1": {
            "rq": "-1",
            "odds": true,
            "win": "5.25",
            "eq": "3.75",
            "lost": "1.49"
        }
    },
    "rates": {
        "竞彩官方(胜平负)": {
            "begin": {
                "win": "2.38",
                "eq": "3.00",
                "lost": "2.67"
            },
            "latest": {
                "win": "2.22",
                "eq": "2.90",
                "lost": "3.00"
            },
            "probability": {
                "win": "39.91",
                "eq": "30.55",
                "lost": "29.53"
            },
            "kelly_formula": {
                "win": "0.86",
                "eq": "0.84",
                "lost": "0.98"
            },
            "odds": "0.89"
        },
        "伟德(直布罗陀)": {
            "begin": {
                "win": "2.50",
                "eq": "3.40",
                "lost": "2.80"
            },
            "latest": {
                "win": "2.45",
                "eq": "3.40",
                "lost": "2.88"
            },
            "probability": {
                "win": "38.89",
                "eq": "28.02",
                "lost": "33.08"
            },
            "kelly_formula": {
                "win": "0.95",
                "eq": "0.98",
                "lost": "0.94"
            },
            "odds": "0.95"
        },
        "立博": {
            "begin": {
                "win": "2.50",
                "eq": "3.30",
                "lost": "2.75"
            },
            "latest": {
                "win": "2.40",
                "eq": "3.30",
                "lost": "2.90"
            },
            "probability": {
                "win": "39.14",
                "eq": "28.47",
                "lost": "32.39"
            },
            "kelly_formula": {
                "win": "0.93",
                "eq": "0.95",
                "lost": "0.94"
            },
            "odds": "0.94"
        },
        "Interwetten": {
            "begin": {
                "win": "2.35",
                "eq": "3.20",
                "lost": "2.70"
            },
            "latest": {
                "win": "2.35",
                "eq": "3.10",
                "lost": "2.75"
            },
            "probability": {
                "win": "38.28",
                "eq": "29.02",
                "lost": "32.71"
            },
            "kelly_formula": {
                "win": "0.91",
                "eq": "0.89",
                "lost": "0.90"
            },
            "odds": "0.90"
        }
    },
    "estimate": {
        "Interwetten": {
            "0": 0,
            "1": 0,
            "3": 0
        },
        "竞彩官方(胜平负)": {
            "0": 0,
            "1": 0,
            "3": 0
        }
    }
}

```