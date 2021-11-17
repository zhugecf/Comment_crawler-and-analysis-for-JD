# -Comment_crawler of JD
本项目实现了对京东商品评论爬取的功能。采用代理的方法，可以实现简单的大规模爬取评论数据。

运行方法：

1.在pcharm中创建一个项目，将main.py放在项目根目录下。再将stopword.txt放在项目根目录下。
 
2.打开main.py，在第53行处，将secret的键值改为自己的提取密钥。
  
  PS:本项目采用的是天启代理ip。该网站网址为：https://www.tianqiip.com/  进入该网站后，注册自己的账号,在左上角的个人中心中，点击我的套餐，即可看见自己的提取密钥。
  
3.main.py中，第51行的port代表获取的代理ip的类型，1为http，2为https，3为socks5。第52行的time表示获取的代理ip有效时长，只能选择3、5、10、15其中的一个。3就是3分钟内有效。

4.运行程序前需要先将本机ip添加到天启代理网站的白名单中。可以先点网站上的提取ip，然后下翻找到生成API链接，然后打开链接。这个时候，本机ip没有加入到白名单中，所以打开链接后，显示的是：{"code":1010,"msg":"当前IP(............)不在白名单内，请先设置IP白名单或联系客户经理"}。这里，IP()中的那一串ip就是要加入到白名单的ip。把那个ip复制一些，点击网站的个人中心，有一个IP白名单。将刚刚那个复制了的ip添加到白名单中就可以了。

注：每次运行项目的时候，在main.py中直接运行。并且项目根目录下只留main.py和stopword.txt两个文件。







请提前确认一下的运行库是否已经安装：

import requests

import os

import csv

import json

import time

from lxml import etree

from snownlp import SnowNLP

import random

import jieba

from collections import Counter

import matplotlib.pyplot as plt

from wordcloud import WordCloud

from dateutil.parser import parse

from random import choice
