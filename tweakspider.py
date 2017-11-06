import scrapy

with open("urls.txt") as f:
    URLS = f.read().strip().split()

COOKIES={"TnetID":"0P-2Vw4m_7p2KTzlzAJ1scnEMCKzbu33", "tc":"1509963891%2C1509963891"}

class TweakSpider(scrapy.Spider):
    name = 'tweakspider'
    start_urls = URLS

    def start_requests(self):
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
        for i, url in enumerate(self.start_urls):
            yield scrapy.http.Request(url,cookies=COOKIES, callback=self.parse)

    def parse(self, response):
        for message in response.css('.message'):
            yield {
                'username': message.css('a.user ::text').extract_first(),
                'content': message.css('.messagecontent ::text').extract()
            }

        #raise scrapy.exceptions.CloseSpider('done')

        for next_page in response.css('.pageDistribution a.next'):
            yield response.follow(next_page, self.parse)
