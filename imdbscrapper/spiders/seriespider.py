from typing import Iterable
import scrapy
from imdbscrapper.items import SerieAllocinescrapperItem


class SeriespiderSpider(scrapy.Spider):
    name = "seriespider"
    allowed_domains = ["allocine.fr"]
    
    def start_requests(self):

        start_urls = [f"https://www.allocine.fr/series/meilleures/?page={i}" for i in range(1,21)]
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)
        
    def parse(self, response):
        # je trouve un pattern de div qui va me permettre de cliquer sur chaque titre sur la page en cours et accéder aux détails
        liste_div_serie = response.xpath("//div[@class='card entity-card entity-card-list cf']")
        
        for div_serie in liste_div_serie:
            lien_titre = div_serie.xpath(".//h2/a/@href").get()
            yield response.follow(lien_titre, self.parse_item)

    def parse_item(self, response):
        
        item = SerieAllocinescrapperItem()
        item['title'] =  response.xpath("//span[contains(@class, 'titlebar-link')]/text()").get()
        item['année_de_diffusion'] = response.xpath('//div[@class="meta-body-item meta-body-info"]/text()').get()
        item['status'] =  response.xpath("//div[contains(@class, 'label-status')]/text()").get()
        item['time'] = response.xpath('//div[@class="meta-body-item meta-body-info"]/text()')[1].get()
        item['genre'] = response.xpath('//div[@class="meta-body-item meta-body-info"]/span[contains(@class, "dark-grey")]/text()').getall()
        item['realisator'] = response.xpath('//div[@class= "meta-body-item meta-body-direction"]//a[contains(@href, "/personne/fichepersonne_gen_")]/text()').getall()
        item['actors'] = response.xpath('//div[@class= "meta-body-item meta-body-actor"]//span[contains(@class, "dark-grey-link")]/text()').getall()
        item['country'] = response.xpath('//div[@class= "meta-body-item meta-body-nationality"][1]//span[contains(@class, "dark-grey-link")]/text()').getall()
        item['press_score'] = response.xpath("//span[@class='stareval-note']/text()").get()
        item['public_score'] = response.xpath("//span[@class='stareval-note']/text()")[1].get()
        item['description'] = response.xpath("//p[@class='bo-p']/text()").get()
        item['nbr_saisons'] = response.xpath("//div[@class='stats-item']/text()").get()
        item['nbr_episodes'] = response.xpath("//div[@class='stats-item']/text()")[1].get()
        return item
   