# -*- coding: utf-8 -*-
import re
import scrapy
import urllib
from Tx.items import TxItem

class TxspiderSpider(scrapy.Spider):
    name = 'TxSpider'
    allowed_domains = ['www.bijianshang.com/index.php']
    # start_urls = ['http://www.bijianshang.com/index.php/']

    @staticmethod
    def __remove_html_tags(str):
        return re.sub(r'<[^>]+>', '', str)
    def start_requests(self):
        # keywords = getattr(self, 'keywords', None),
        # '网站的编码是gb2312的'http://www.bijianshang.com/news/html/?2130.html
        keywords = u'谢谢'.encode('utf-8')
        print("test!!!!!!!!!!!")
        requesturl = "http://www.bijianshang.com/search/index.php?myord=uptime&myshownums=20&key={0}&imageField.x=0&imageField.y=0".format(urllib.quote(keywords))
        return [scrapy.Request(requesturl,meta={'dont_obey_robotstxt ': True},dont_filter=True,callback=self.__parse_paragraph_pages)]
    def __parse_paragraph_pages(self, response):
        # '解析跳转到每篇文件链接'
        # for blog_url in response.xpath('//tr[@class="bg"]/td[@class="f14"]/a[@class="f234"]/@href').extract():
        for paragraph_url in response.css('li div[class=title] a[target=_self] ::attr(href)').extract():
            paragraph_url=paragraph_url.lstrip('../')
            request_url="http://www.bijianshang.com/{0}".format(paragraph_url)
            print("saduihsadksahndksad")
            print(request_url)
            yield scrapy.Request(request_url,meta={'dont_obey_robotstxt ': True},dont_filter=True,callback=self.parse)
        i=0
        print("saskjdhsakjdhsajkdhajksdhsjkadnsa")
        for temp in response.css('li[class=pbutton] a::text').extract():
            if temp == u'下一页':
                print(temp)
                break
            i=i+1
            print(i)
            print(temp)
        if response.css('li[class=pbutton] a::text').extract():
            print("fuxc")
            pass
            print(response.css('li[class=pbutton] a::text').extract())
            print(i)
            next_page = response.css('li[class=pbutton] a::attr(href)').extract()[i]
            print("The next page_url is:")
            print(next_page)
            if next_page is not None:
                print("this")
                requesturl ="http://www.bijianshang.com/{0}".format(next_page)
                yield scrapy.Request(requesturl,meta={'dont_obey_robotstxt ': True},dont_filter=True,callback=self.__parse_paragraph_pages)
        else:
            print("sasasssadasadfdsa")


    def parse(self, response):
        # '解析网站台词正文和节目名 name&content'
        print("shabi")
        name = response.css('div[class=newstitle] ::text,div[id=newscontent] div[class=newstitle]::text').extract()
        print(name)
        print(response.css('p[class=MsoNormal] ::text,p[class=p] ::text').extract())
        items=[]
        for temp in response.css('p[class=MsoNormal]::text,p[class=p] ::text,p[class=MsoNormal] font b span font::text,p[class=MsoNormal] font span font::text,p[class=MsoNormal] span font::text').extract():
            items.append(temp)
        content = items
        yield TxItem({'name': name,'content': content})