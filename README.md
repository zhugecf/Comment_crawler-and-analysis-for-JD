# -Comment_crawler of JD
本项目实现了对京东商品评论爬取的功能。采用代理的方法，可以实现简单的大规模爬取评论数据。

运行方法：

1.在pcharm中创建一个项目，将main.py放在项目根目录下。再将stopword.txt放在项目根目录下。
 
 2.打开main.py，在第53行处，将secret的键值改为自己的提取密钥。
  
  PS:本项目采用的是天启代理ip。该网站网址为：https://www.tianqiip.com/  进入该网站后，注册自己的账号,在左上角的个人中心中，点击我的套餐，即可看见自己的提取密钥。

注：每次运行项目的时候，在main.py中直接运行。并且项目根目录下只留main.py和stopword.txt两个文件。
