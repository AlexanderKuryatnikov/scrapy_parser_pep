import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        pep_rows = (response.xpath('//section[@id="numerical-index"]').
                    css('tbody > tr'))

        for row in pep_rows:
            number, name = row.css('a::text').getall()
            pep_link = row.css('a::attr(href)').get()
            yield response.follow(pep_link, callback=self.parse_pep,
                                  cb_kwargs={'number': number, 'name': name})

    def parse_pep(self, response, number, name):
        status = response.css('dt:contains("Status") + dd::text').get()
        data = {
            'number': number,
            'name': name,
            'status': status,
        }
        yield PepParseItem(data)
