import scrapy
from scrapy.http.response.html import HtmlResponse

from art_porn.items import ArtPornItem


class BaseSpider(scrapy.Spider):
    name = 'all'

    def start_requests(self):
        body = {
            'action': 'login',
            'redirect_to': '/',
            'format': 'json',
            'mode': 'async',
            'username': self.settings.get('USER'),
            'pass': self.settings.get('PASS')
        }
        yield scrapy.FormRequest(url='https://theartporn.com/login/', formdata=body)

    def parse(self, response: HtmlResponse, **kwargs):
        if response.json().get('status') == 'success':
            for category in self.settings.getlist('CATEGORY'):
                yield scrapy.Request(url='https://theartporn.com/categories/{0}/'.format(category),
                                     callback=self.categories_parse, cb_kwargs={'category': category})

    def categories_parse(self, response: HtmlResponse, category):
        next_url_list = response.css('a.button.prev::attr(href)').getall()
        if len(next_url_list) > 1:
            yield scrapy.Request(url=response.urljoin(next_url_list[1]), callback=self.categories_parse,
                                 cb_kwargs={'category': category})
        else:
            yield scrapy.Request(url=response.urljoin(next_url_list[0]), callback=self.categories_parse,
                                 cb_kwargs={'category': category})

        for item in response.css('div.thumb-video.cf').css('a.thumb-video-link::attr(href)').getall():
            yield scrapy.Request(url=item, callback=self.video_parse, cb_kwargs={'category': category})

    def video_parse(self, response: HtmlResponse, category):
        title = response.css('h2.title.big::text').get()
        for item in response.css('ul.video-downloads-buttons').css('li'):
            if '1080p' in item.css('a::text').get().strip():
                link = item.css('a::attr(href)').get()
                resp_cookie = response.headers.get('Set-Cookie').decode().split(';')[0]
                yield ArtPornItem(name=title, link=link, category=category,
                                  cookie=response.request.headers.get('Cookie').decode() + resp_cookie)
