# -*- coding: utf-8 -*-
import datetime

import scrapy

from ..items import Top500Item

def parse_int(str):
    try:
        return int(str.replace(',', ''))
    except AttributeError:
        return

class RmaxSpider(scrapy.Spider):
    name = 'rmax'
    allowed_domains = ['top500.org']

    def start_requests(self):
        base_url = 'http://top500.org/lists'
        urls = []

        months = ['06', '11']
        start_year = 1993
        now = datetime.datetime.now()

        for year in range(start_year, now.year + 1):
            for month in months:
                urls.append('%s/%d/%s/' % (base_url, year, month))

        for uri in urls:
            yield scrapy.Request(url=uri, callback=self.parse)


    def parse(self, response):
        year, month = response.url.split('/')[-3:-1]

        table_data = response.xpath('//table//tr')
        for row in table_data[1:]:
            item = Top500Item()

            item['year'] = int(year)
            item['month'] = int(month)

            item['rank'] = parse_int(row.xpath('td[1]/text()').extract_first())

            sys = ''.join(row.xpath('td[2]/text()').extract_first())
            item['system'] = ' '.join(sys.split())

            item['cores'] = parse_int(row.xpath('td[3]/text()').extract_first())
            item['rmax'] = row.xpath('td[4]/text()').extract_first()
            item['rpeak'] = row.xpath('td[5]/text()').extract_first()
            item['power'] = parse_int(row.xpath('td[6]/text()').extract_first())

            yield item
