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
import socket
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}
def pre_data():
    url1 = 'https://search.jd.com/Search'
    print("输入商品名称：")
    str1=str(input())
    data = {
        'keyword': str1,
        'enc': 'utf-8',
        'wq':str1,
    }
    session = requests.Session()
    response = session.get(url=url1, params=data, headers=headers).text
    tree = etree.HTML(response)
    list=[]
    try:
        for i in range(1, 6):
            a = tree.xpath(
                '/html/body/div[5]/div[2]/div[2]/div[1]/div[1]/div[2]/ul[1]/li[{}]/div[1]/div[1]/a[1]/@href'.format(i))[
                0]
            # 获取商品号
            str1 = ''
            str1 = a[14:]
            first = str1.find('.')
            list.append(str1[0:first])
    except:
        time.sleep(1)
    return list
def get_dailiURL():
    list=[]
    url='http://api.tianqiip.com/getip'
    data={
        'type':'txt',
        'num':1,
        'port':2,
        'time':5,
        'secret':''#这里的secret的键值是自己的提取码
    }
    for i in range(5):
        response = requests.get(url=url, params=data)
        list.append(response.text)
    return list
def getinformation(id,index,daili_url_list):
    url='https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId='+id+'&score=0&sortType=5&page={0}&pageSize=10&isShadowSku=0&rid=0&fold=1'
    str=choice(daili_url_list)

    str='https://'+str
    proxies={
        'https':str
    }
    try:
        for i in range(999999):
            ''''''
            response = requests.get(url=url.format(i), headers=headers,proxies=proxies)
            time.sleep(random.random()*2)
            json_response = response.text.replace('fetchJSON_comment98(', '').replace(');', '')
            # json转换为字典格式，读取评论数据
            json_response = json.loads(json_response)['comments']
            print("正在提取第{}个商品的第{}页评论".format(index+1,i + 1))
            columns = ['id', 'nickname', 'referenceTime', 'creationTime', 'referenceId', 'productColor', 'productSize',
                       'score', 'content']
            # 如下循环分别提取数据
            for j in range(10):
                userid = json_response[j][columns[0]]
                username = json_response[j][columns[1]]
                buytime = json_response[j][columns[2]]
                commenttime = json_response[j][columns[3]]
                productid = json_response[j][columns[4]]
                productcolor = json_response[j][columns[5]]
                productsize = json_response[j][columns[6]]
                score = json_response[j][columns[7]]
                comment = json_response[j][columns[8]]
                # 有些用户没有追评，则返回空值
                try:
                    aftercomment = json_response[j]['afterUserComment']['content']
                except:
                    aftercomment = ''
                # 将以上提取出的数据放到一个列表里
                comment_one = [userid, username, buytime, commenttime, productid, productcolor, productsize, score,
                               comment,
                               aftercomment]
                # 生成器返回提取出的列表数据
                yield (comment_one)
    except Exception as exp:
        print(exp)
def SaveCsv(path,id,i,daili_url_list):
    end_columns = ['userId', 'userName', 'buyTime', 'commentTime', 'productId', 'productColor', 'productSize', 'score',
                   'comment', 'afterComment']
    comments=open(path,'w',newline='',encoding='utf-8')
    w=csv.writer(comments)
    w.writerow(end_columns)
    comments=getinformation(id,i,daili_url_list)
    for comment in comments:
        w.writerow(comment)
def  classify(id):
    new_list=[]
    times_list=[]
    file = open("count/{}shop.txt".format(id), 'w', encoding='utf-8')
    csvFile = open('asus_comments'+str(id)+'.csv', 'r', encoding='utf-8')
    reader = csv.reader(csvFile)
    a = list(reader)
    i=1
    try:
        while a[i][5] != '':
            new_list.append(a[i][5])
            i += 1
    except:
        print(end='')
    result=Counter(new_list)
    for key in result:
        times_list.append(result[key])
        file.write("{}:一共有{}条评论\n".format(key,result[key]))
    times_list.sort()
    times_list.reverse()
    max_times=times_list[0]
    for key in result:
        if(result[key]==max_times):
            file.write("\n" )
            file.write("评论条数最多的商品是：%s"%(key))
    print("第{}个商品评论类别归类完毕".format(id))
    file.close()
def analysis(id):
    #print('asus_comments{}.csv'.format(id))
    #remove_file('asus_comments{}.csv'.format(id))
    csvFile = open('asus_comments{}.csv'.format(id), 'r', encoding='utf-8')
    reader = csv.reader(csvFile)
    a = list(reader)
    file1 = open("analysis{}/1star.txt".format(id), 'w', encoding='utf-8')
    file2 = open("analysis{}/2star.txt".format(id), 'w', encoding='utf-8')
    file3 = open("analysis{}/3star.txt".format(id), 'w', encoding='utf-8')
    file4 = open("analysis{}/4star.txt".format(id), 'w', encoding='utf-8')
    file5 = open("analysis{}/5star.txt".format(id), 'w', encoding='utf-8')
    for i in range(1, 100000):
        if(a[i][7]==''):
            break
        if a[i][7] == '1':
            file1.write(a[i][8] + '\n')
        if a[i][7] == '2':
            file2.write(a[i][8] + '\n')
        if a[i][7] == '3':
            file3.write(a[i][8] + '\n')
        if a[i][7] == '4':
            file4.write(a[i][8] + '\n')
        if a[i][7] == '5':
            file5.write(a[i][8] + '\n')
    file1.close()
    file2.close()
    file3.close()
    file4.close()
    file5.close()
    print("第%d个商品完成数据预处理"%(id))
def wordcloud_fun(path,num,id):
    stopwords = set()
    content = [line.strip() for line in open('stopword.txt', 'r', encoding='utf-8').readlines()]
    stopwords.update(content)
    f = open(path, 'r', encoding='UTF-8').read()  # 结巴分词，生成字符串，wordcloud无法直接生成正确的中文词云
    cut_text = " ".join(jieba.cut(f))
    wordcloud = WordCloud(  # 设置字体，不然会出现口字乱码，文字的路径是电脑的字体一般路径，可以换成别的
        font_path="C:/Windows/Fonts/simfang.ttf",  # 设置了背景，宽高
        background_color="white", width=1000, height=880, stopwords=stopwords).generate(cut_text)

    wordcloud.to_file('wordcloud/shop{}/cloud{}.jpg'.format(id+1,num))
    print("第{}个商品的{}星评论词云生成完毕".format(id+1,num))
    '''plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()'''
def time_calculate(id,i):#id是第几个商品，i是第几条评论

    csvFile = open('asus_comments' + str(id) + '.csv', 'r', encoding='utf-8')
    reader = csv.reader(csvFile)
    a = list(reader)
    str1 = a[i][2]
    str2 = a[i][3]
    str1 = parse(str1)
    str2 = parse(str2)
    csvFile.close()
    return ((str2 - str1).days)*86400+(str2 - str1).seconds
def average(id):
    sum=0
    num=0

    csvFile = open('asus_comments' + str(id) + '.csv', 'r', encoding='utf-8')
    reader = csv.reader(csvFile)
    a = list(reader)
    file = open("time_calculate/{}shop.txt".format(id), 'w', encoding='utf-8')
    type_list=[]
    i = 1
    if a[1][5]!=0:
        print("第{}个商品评论周期平均值计算完毕".format(id))
    try:
        while a[i][5] != '':
            type_list.append(a[i][5])
            i += 1
    except:
        print(end='')
    result = Counter(type_list)
    type_list.clear()
    for key in result:
        type_list.append(key)
    for key in type_list:
        for i in range(1000):
            try:
                if a[i][5] == key:
                    sum += time_calculate(id, i)
                    num += 1
            except:
                print(end='')
        aver=sum/num/86400
        sum=0
        num=0
        file.write("%s的平均评论时间差是：%lf天\n"%(key,aver))

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
def feel(id):
    sum_sentiment = 0
    good_counter = 0
    just_so_so_counter = 0
    bad_counter = 0
    csvFile = open('asus_comments' + str(id) + '.csv', 'r', encoding='utf-8')
    reader = csv.reader(csvFile)
    a = list(reader)
    file = open("feel/{}shop.txt".format(id), 'w', encoding='utf-8')
    try:
        for i in range(1, 1000):
            text = a[i][8]
            sentiment = SnowNLP(text).sentiments
            file.write(a[i][8] + '\t[这一条评论的感情偏向是：' + str(sentiment) + ']\n')
            if sentiment > 0.8:
                good_counter += 1
            elif sentiment > 0.4:
                just_so_so_counter += 1
            else:
                bad_counter += 1
            sum_sentiment += sentiment
    except:
        print(end="")
    total=good_counter+bad_counter+just_so_so_counter
    file.write("-----------------共计" + str(total)+ "条评论---------------------------\n")
    file.write("-----------------0.8以上有" + str(good_counter) + "条评论----------------------\n")
    file.write("-----------------0.4-0.8有" + str(just_so_so_counter) + "条评论----------------------\n")
    file.write("-----------------0.4以下有" + str(bad_counter) + "条评论----------------------\n")
    file.write("平均感情偏向为：{}".format(sum_sentiment / total))
    file.close()
    print("第{}个商品的感情偏向分析完毕".format(id))
def setup_file():
    b = os.getcwd()
    os.mkdir(b + "//time_calculate")
    os.mkdir(b + "//wordcloud")
    os.mkdir(b + "//feel")
    os.mkdir(b + "//count")
    c = b + "//wordcloud"
    for i in range(1, 6):
        os.mkdir(b + "//analysis%d" % (i))
        os.mkdir(c + "//shop%d" % (i))
def main():
    setup_file()
    list=pre_data()
    print("符合要求的商品有%d种（最多取5种）"%len(list))
    daili_url_list=get_dailiURL()
    print("获取代理ip完成")
    try:
        for i in range(5):

            SaveCsv(r'asus_comments{}.csv'.format(i + 1), list[i],i,daili_url_list)
    except:
        print(end="")
    for i in range(5):

        try:
            analysis(i + 1)
        except:
            continue
    print("数据预处理完毕")

    for i in range(5):
        for j in range(1,6):
            try:
                wordcloud_fun('analysis{}/{}star.txt'.format(i + 1, j), j, i)
            except:
                continue

    for i in range(1, 6):
        try:
            classify(i)
        except:
            print(end='')
    for i in range(1, 6):
        try:
            average(i)
        except:
            print(end="")

    for i in range(1, 6):
        try:
            feel(i)
        except:
            print(end="")

if __name__=="__main__":
    main()