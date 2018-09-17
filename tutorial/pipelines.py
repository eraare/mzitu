# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from . import settings
import os


class MzituPipeline(ImagesPipeline):
	def get_media_requests(self, item, info):
		for image_url in item['image_urls']:
			# yield scrapy.Request(image_url, headers=self.headers(image_url), meta={'item': item})
			yield scrapy.Request(image_url, meta={'item': item})

	def item_completed(self, results, item, info):
		image_paths = [x['path'] for ok, x in results if ok]
		if not image_paths:
			raise DropItem("Item contains no images")
			item['image_paths'] = image_paths
			return item

	def file_path(self, request, response=None, info=None):
		item = request.meta['item']
		image_path = item.get('image_path')
		image_title = item.get('image_title') + '.jpg'
		the_path = os.path.join(image_path, image_title)
		return the_path

	def headers(self, referer):
		"""处理下载防盗链"""
		headers = {
			'Host': 'i.meizitu.net',
			'Pragma': 'no-cache',
			# 'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
	        'Cache-Control': 'no-cache',
	        'Connection': 'keep-alive',
	        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
	        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
	        'Referer': referer
		}
		return headers
