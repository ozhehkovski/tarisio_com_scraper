import re
from scrapy.spiders import SitemapSpider
from mapfinder.items import TarisioItem

class TarisioSpider(SitemapSpider):
    name = "tarisio"
    allowed_domains = ["tarisio.com"]
    sitemap_urls = ['https://tarisio.com/sitemap-properties.xml']
    sitemap_rules = [('property', 'parse')]

    def parse(self, response):
        item = TarisioItem()
        # image file path search
        pattern = r'var\s+photos_links\s*=\s*\[(.*?)\];'
        match = re.search(pattern, response.text, re.DOTALL)
        photos_count = 0
        if match:
            photos_content = match.group(1)
            photos_list = [path.strip("' ") for path in photos_content.split(',')]
            photos_count = len(photos_list)
        item['url'] = response.url
        item['count'] = photos_count
        yield item