from scrapy import Spider, Request
from patient.items import PatientItem
import re
import math

custom_settings = {
    'USER_AGENT': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:80.0) Gecko/20100101 Firefox/80.0"
}

class PatientSpider(Spider):
    name = 'patient_spider'
    allowed_urls = ['https://patient.info/']
    start_urls = ['https://patient.info/forums']

    def parse(self, response):
        group_urls = ['https://patient.info/forums/discuss/browse/coronavirus-covid-19--4541',
        'https://patient.info/forums/discuss/browse/depression-683',
        'https://patient.info/forums/discuss/browse/anxiety-disorders-70']

        for url in group_urls:
            yield Request(url=url, callback=self.parse_group_page)

    def parse_group_page(self, response):

        covid_urls = [f'https://patient.info/forums/discuss/browse/coronavirus-covid-19--4541?page={i+1}#group-discussions' for i in range(5)]  

        depression_urls = [f'https://patient.info/forums/discuss/browse/depression-683?page={i+1}#group-discussions' for i in range(21)] 

        anxiety_urls = [f'https://patient.info/forums/discuss/browse/anxiety-disorders-70?page={i+1}#group-discussions' for i in range(120)]  

        # print('='*55)
        # print(len(covid_urls))
        # print(len(depression_urls))
        # print(len(anxiety_urls))
        # print('='*55)



        for url in covid_urls:
            yield Request(url=url,callback=self.parse_results_page)

        for url in depression_urls:
            yield Request(url=url,callback=self.parse_results_page)

        for url in anxiety_urls:
            yield Request(url=url,callback=self.parse_results_page)


    def parse_results_page(self, response):
        post_url = response.xpath('//h3[@class="post__title"]/a/@href').extract()[1:]
        post_url = ['https://patient.info' + url for url in post_url]


        for url in post_url:
            yield Request(url=url,callback=self.parse_post_page)

    def parse_post_page(self, response):
        replies = response.xpath('//li[@class="comment"]') 

        reply_text = []

        for reply in replies:
            reply_ = reply.xpath('.//div[@class="post__content break-word"]/p/text()').extract()
            reply_text.append(reply_)
            
        group = response.xpath('//li[@class="breadcrumb-item"]/a/span/text()').extract()[-1].strip()
        post_title = response.xpath('//h1[@class="u-h1 post__title"]/text()').extract_first()
        post_user = response.xpath('//h5/a[@class="author__name"]/text()').extract_first()
        post_likes = re.findall('\d+', response.xpath('//p[@class="post__stats"]/text()').extract()[3].strip()[0:7])
        num_replies = re.findall('\d+', response.xpath('//p[@class="post__stats"]/text()').extract()[3].strip()[7:20])
        post_date = response.xpath('//time[@class="fuzzy"]/@datetime').extract_first()[0:10]
        num_following = re.findall('\d+', response.xpath('//p[@class="post__stats"]/span/text()').extract()[2])
        post_text = response.xpath('//div[@class="post__content"]/p/text()').extract()[:-1]
        reply_user = response.xpath('//a[@rel="nofollow author"]/text()').extract()[1:]


        item = PatientItem()
        item['group'] = group
        item['post_title'] = post_title
        item['post_user'] = post_user
        item['post_likes'] = post_likes
        item['num_replies'] = num_replies
        item['post_date'] = post_date
        item['num_following'] = num_following
        item['post_text'] = post_text
        item['reply_user'] = reply_user
        item['reply_text'] = reply_text

        yield item