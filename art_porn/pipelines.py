# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import requests

from art_porn.items import ArtPornItem
from art_porn.lib.download_header import random_other_headers
from art_porn.spiders.Start import BaseSpider


class ArtPornPipeline:
    def process_item(self, item, spider: BaseSpider):
        base_url = 'http://127.0.0.1:8900/jsonrpc'
        token = 'token:' + spider.settings.get('ARIA_TOKEN')
        if isinstance(item, ArtPornItem):
            headers = random_other_headers()
            headers.append('Cookie:' + item['cookie'])
            download_data = {
                'jsonrpc': '2.0',
                'method': 'aria2.addUri',
                'id': '0',
                'params': [token, [item['link']],
                           {
                               'out': item['name'] + '.mp4',
                               'header': headers,
                               'dir': '/opt/videos/{0}'.format(item['category'])
                           }]
            }
            requests.post(url=base_url, json=download_data)
        return item
