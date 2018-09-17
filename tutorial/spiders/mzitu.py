# -*- coding: utf-8 -*-
import scrapy
from tutorial import items


class MzituSpider(scrapy.Spider):
    name = 'mzitu'
    allowed_domains = ['mzitu.com']
    start_urls = ['http://www.mzitu.com/']

    def parse(self, response):
        gallerys = response.css('div.postlist ul#pins li span a')
        for gallery in gallerys:
            gallery_url = gallery.css('a::attr(href)').extract_first()
            yield scrapy.Request(url=gallery_url, callback=self.parse_page)
        # 下一页
        next_page = response.css('a.next.page-numbers::attr(href)').extract_first()
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_page(self, response):
        image = response.css('div.content')
        item = items.ImageItem()
        item['image_path'] = image.css('div.main-image p a img::attr(alt)').extract_first()
        item['image_title'] = image.css('h2.main-title::text').extract_first()
        item['image_urls'] = [image.css('div.main-image p a img::attr(src)').extract_first()]
        yield item
        # 下一页
        next_page = response.xpath('//div[@class="pagenavi"]/a[last()]/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.parse_page) 
