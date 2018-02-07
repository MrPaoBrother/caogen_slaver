# -*- coding: utf-8 -*-
import scrapy
from caogen.model.config import REDIS_CONN
from caogen.items import ArticleDetailItem
import time


class CaogenSlaverSpider(scrapy.Spider):
    name = 'caogen_slaver'
    allowed_domains = ['caogen.com']
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"}

    def __init__(self, name=None, **kwargs):
        # 实例化redis
        self.redis_conn = REDIS_CONN
        super(CaogenSlaverSpider, self).__init__(name, **kwargs)

    def start_requests(self):
        while True:
            url = self.get_msg_from_redis()
            if url:
                yield scrapy.Request(url, headers=self.headers, callback=self.parse, dont_filter=True)
            else:
                print("Redis 数据库为空，5秒后继续监测...")
                time.sleep(5)

    def parse(self, response):
        item = ArticleDetailItem()
        # 获取作者
        author = response.xpath('//td/span[@id="Head1_Person"]/text()').extract()
        # 获取标题
        title = response.xpath('//div[@class="copy_title"]/span[@id="Blog_Infor"]/text()').extract()
        # 获取发布时间
        pubtime = response.xpath('//div[@class="copy_title"]/span[@id="Intime"]/text()').extract()
        # 获取全文html
        content = str(response.body).decode("gbk")

        # 填充item
        item["author"] = self.get_msg_by_list(author)
        item["title"] = self.get_msg_by_list(title)
        item["pubtime"] = self.get_msg_by_list(pubtime)
        item["content"] = content
        yield item

    def get_msg_from_redis(self):
        """
        从redis读取数据
        :param r : redis对象
        :return:
        """
        # 从redis中获取一个请求
        master_request = self.redis_conn.spop("master:requests")
        if master_request is not None:
            master_request = master_request.encode("utf8")
            master_request = master_request.replace("\'", "\"")
            return master_request
        return None

    def get_msg_by_list(self, data_list):
        if len(data_list) < 1:
            return None
        return data_list[0]
