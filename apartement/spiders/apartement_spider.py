import scrapy
import logging
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from .. import sorter

class ApartemensSpider(scrapy.Spider):
    name = "apartements"
    start_urls = [
            'https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/'
        ]
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        if 'www.nepremicnine.net' in response.url:
            for apartement in self.parseNepremicnine(response):
                yield apartement

    def parseNepremicnine(self, response):
        advertisments = response.xpath("//div[@class='seznam']/div")
        apartements = []
        for oglas in advertisments:
            try:
                link = oglas.xpath("descendant::*[@class='slika']/@href").extract_first()
                size = float(oglas.xpath("descendant::*[@class='velikost']/text()").extract_first().split(' ')[0].replace(',','.'))
                price = float(oglas.xpath("descendant::*[@class='cena']/text()").extract_first().split(' ')[0].replace('.', '').replace(',','.'))
                year = int(oglas.xpath("descendant::*[@class='atribut leto']/strong/text()").extract_first())
                location = oglas.xpath("descendant::*[@class='title']/text()").extract_first()
                ppsm = price/size
                apartement = {
                        'ppsm' : ppsm,
                        'year' : year,
                        'location' : location,
                        'price' : price,
                        'size' : size,
                        'link' : response.urljoin(link)
                    }
                yield apartement
            except:
                self.logger.warning("Couldn't find get information for advert %s" % oglas )
                continue
        next_page = response.xpath("//a[@class='next']/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parseNepremicnine)

    def spider_closed(self):
        sorter.modifyApartments('apartments.json', 'orderedApartments.json')
