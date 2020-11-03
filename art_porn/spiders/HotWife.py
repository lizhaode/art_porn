import scrapy
from scrapy.http.response.html import HtmlResponse

from art_porn.items import HotItem


class BaseSpider(scrapy.Spider):
    name = 'hot'

    def start_requests(self):
        yield scrapy.Request(url='http://www.hotwiferio.com/members/index.php')

    def parse(self, response: HtmlResponse, **kwargs):
        for li in response.css('nav').css('li'):
            if li.css('::text').get() == 'Scenes':
                for child in li.css('ul>li'):
                    try:
                        year = int(child.css('::text').get())
                        link = child.css('::attr(href)').get()
                        yield scrapy.Request(url=response.urljoin(link), cb_kwargs={'category': year},
                                             callback=self.parse_page)
                    except ValueError as e:
                        pass

    def parse_page(self, response: HtmlResponse, category):
        for i in response.css('a.model_title'):
            yield scrapy.Request(i.css('::attr(href)').get(), callback=self.video_parse,
                                 cb_kwargs={'category': category})

    def video_parse(self, response: HtmlResponse, category):
        link = response.urljoin(response.css("a.full_download_link[onclick*='mp43000']::attr(href)").get())
        title = ''
        for i in response.css('div.title_bar::text').getall():
            i = i.strip()
            if i:
                title = i
                break
        yield HotItem(name=title, link=link, category=category)
