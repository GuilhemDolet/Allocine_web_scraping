from typing import Iterable
import scrapy
from imdbscrapper.items import ImdbscrapperItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError

class MoviespiderSpider(scrapy.Spider):
    name = "moviespider"
    allowed_domains = ["allocine.fr"]
    
    def start_requests(self):

        # yield scrapy.Request(url="https://www.allocine.fr/film/meilleurs/", callback=self.parse)

        start_urls = [f"https://www.allocine.fr/film/meilleurs/?page={i}" for i in range(1, 31)]
        for url in start_urls:
            yield  scrapy.Request(url=url, callback=self.parse, errback=self.error_callback)
    

    def parse(self, response,):
        
        # On trouve un objet HTML qui se répète plusieurs fois sur la page pour itérer dessus.
        movies_vignettes = response.xpath("//li[@class='mdl']")

        # parcourir les différentes vignettes par film SUR LA PREMIERE PAGE (10 sur chaque pages)
        for vignette in movies_vignettes:
            url_movie = vignette.xpath(".//h2/a/@href").get()
            yield response.follow(url_movie, self.parse_movie_info, errback=self.error_callback)
        

    def parse_movie_info(self, response):

        item = ImdbscrapperItem()
        item['title'] =  response.xpath("//div[@class='titlebar-title titlebar-title-xl']/text()").get()

        # Gestion des valeurs manquantes:
        press_score = response.xpath("//span[@class='stareval-note']/text()").get()
        if press_score:
            item['press_score']= press_score
        else:
            item['press_score'] = "Non disponible"

        # Gestion des valeurs manquantes:
        item['public_score'] = response.xpath("//span[@class='stareval-note']/text()")[1].get()
        # y'a des Nones qui traine = OK = Géré avec le 'or' à la fin de la ligne
        item['mention'] = response.xpath("//section[@class='section ovw ovw-synopsis']/div[@class='certificate']/span[@class='certificate-text']/text()").get() or "Non disponible"
        # des retour à la lignes à nettoyer = OK = Géré avec le pipeline
        item['time'] =  response.xpath("//div[@class='meta-body-item meta-body-info']/text()[contains(., 'h')]").get()
        #à nettoyer aussi
        item['years'] =  response.xpath("//div[@class='meta-body-item meta-body-info']/span/text()").get()
        item['description'] =  response.xpath("//div[@class='content-txt ']/p/text()").get()
        # pour le genre on obtient une liste
        item['genre'] = response.xpath("//div[@class='meta-body']/div[@class='meta-body-item meta-body-info']/span[contains(@class, 'dark-grey-link')]/text()").getall()
        # nettoyage necessaire pour actors = OK = géré avec le pipeline
        item['actors'] =  response.xpath("//div[@class='meta-body-item meta-body-actor']/span/text()").getall()
        # nettoyage pour enlever de la liste le 'De' et le 'Par' et transformer en string
        item['realisator'] =  response.xpath("//div[contains(@class, 'meta-body-item meta-body-direction')]/span/text()").getall()
        item['country'] =  response.xpath("//section[@class='section ovw ovw-technical']//div[@class='item']/span[@class='that']/span/text()").getall()
        #un retour à la ligne à nettoyer
        item['language'] =  response.xpath("//section[@class='section ovw ovw-technical']//span[contains(text(), 'Langues')]/following-sibling::span[1]/text()").get()

        yield item

    # pour récupérer les erreurs dans le fichier scrapy.log
    def error_callback(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(f'HTTP Error on {response.url}')
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error(f'DNS Lookup Error on {request.url}')
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error(f'Timeout Error on {request.url}')

