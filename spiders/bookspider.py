import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article')
        for book in books:
            yield{
                'name': book.css('h3 a').attrib['title'],
                'price': book.css('.price_color::text').get(),
                'url': book.css('h3 a').attrib['href']
            }
        
        nextPage = response.css('li.next a').attrib['href']

        if nextPage is not None:
            if 'catalogue/' in nextPage:
                nextPageUrl = "https://books.toscrape.com/"+ nextPage
                yield response.follow(nextPageUrl, callback= self.parse)
            else:
                nextPageUrl = "https://books.toscrape.com/catalogue/" + nextPage
                yield response.follow(nextPageUrl, callback= self.parse)
