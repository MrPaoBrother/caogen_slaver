# 草根网分布式爬虫之Slaver端
**简介:**
这部分主要负责将```Master```服端传入redis中的url获取然后进行爬取，将处理后的结果重新返回给redis

## 安装

**1** scrapy安装

```
$ sudo pip install scrapy

```
**ps.```scrapy```安装对于不同的环境配置都会有不同，这里我很难给出一个详细的教程，大家根据自己的情况Google一下或者我这里推荐一些我认为不错的:**

* [scrapy安装教程-win](http://blog.csdn.net/bemorequiet/article/details/62885881)
* [scrapy安装教程-mac](https://www.jianshu.com/p/a03aab073a35)
* [scrapy安装教程-ubuntu](http://blog.csdn.net/qq_30242609/article/details/52810765)

安装好之后打开```python```界面输入：

```python
import scrapy 
scrapy.__version__
```
,如果安装成功应该会出现如下界面**(可以看到我这里使用的是1.5.0版本)**:
![scrapy版本1.5.0](http://img.blog.csdn.net/20180207165654553?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZzg0MzMzNzM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

**2** redis安装:

```
$ sudo apt-get install redis-server
```

**ps. redis安装可以参考[这里](http://www.runoob.com/redis/redis-install.html)**

**3** scrapy-redis安装:
```
$ sudo pip install scrapy-reids
```
**4** mysql安装:
请参考[这里](https://dev.mysql.com/downloads/mysql/5.6.html#downloads)，本例中使用的是```MySQL5.6.38```版本

**5** sqlalchemy安装:

```
$ sudo pip install sqlalchemy

```
**6** 其他:

* 可能还有一些软件的安装，每个人使用情况不同，我的IDE是[PyCharm](https://www.jetbrains.com/pycharm/),Mysql可视化工具使用的是[Navicat](http://www.navicat.com.cn/products/),Redis可视化工具使用的是[Redis-Desktop-Manager](https://redisdesktop.com/)

配置
----
* 在model/caogen_scrapy.ini文件中修改MySQL配置,例:

```
[default]
host=127.0.0.1
port=3306
user=root
password=
db=caogen
echo=True
```

* 在model/caogen_scrapy.ini文件中修改redis的配置

```
[default]
host = 127.0.0.1
port = 6379
```

* 在caogen/settings.py文件中,按照自己的redis配置修改,一般使用默认:

```
# Specify the host and port to use when connecting to Redis (optional).
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# Custom redis client parameters (i.e.: socket timeout, etc.)
REDIS_PARAMS = {}
# REDIS_URL = 'redis://user:pass@hostname:9001'
REDIS_PARAMS['password'] = ''
```

* **建表**,具体的可以参照model模块中的models.py文件,所有的建表语句都在model/table.txt文件中


运行说明
-------

**1** 先开启```master```端,具体方法查看**[草根网分布式爬虫之Master端](https://github.com/MrPaoBrother/caogen_master)**的文档。

**2** 在根目录下找到```run_slaver.py```文件,运行命令:

```
$ python run_slaver.py
```

*  如果redis中没有数据，程序会五秒刷新一次，**如图:**

![image](./images/caogen_slaver_redis_null.png)

* 如果有数据会将url取出后将item返回给redis，**如图:**

![image](./images/caogen_slaver_item.png)

**3** 如果此时```master```端开启了```process_item.py```文件,就会将redis中的item存入MySQL数据库中，**如图:**

![image](./images/caogen_master_mysql_result.png)

**4** 运行结束...


注意事项
-------
**1** 如果项目运行中缺少什么模块，请自行根据报错信息安装，这里不可能给出全部的可能

**2** 项目中没有设置一些中间件，只是单纯的展示一遍分布式爬虫的基本概念，有兴趣的朋友可以贡献一些改进代码。

**3** 如果项目中在运行时有什么```bug```,请留言。

**4** 该项目要配合**[草根网分布式爬虫之Master端](https://github.com/MrPaoBrother/caogen_master)**一起运行才能展示效果，请注意。

相关资料
-------
* [scrapy中文文档](http://scrapy-chs.readthedocs.io/zh_CN/0.24/)
* [scrapy-redis相关文档](https://scrapy-redis.readthedocs.io/en/stable/)
