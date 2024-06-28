# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class AllocineMovieScrapperPipeline:
    def process_item(self, item, spider):
        item = self.clean_time(item)
        item = self.clean_actors(item)
        item = self.clean_language(item)
        item = self.clean_years(item)
        item = self.clean_realisator(item)
        item = self.clean_genre(item)
        item = self.clean_country(item)
        item = self.clean_press_score(item)
        item = self.clean_public_score(item)
        return item
    
    def clean_time(self, item):
        adapter = ItemAdapter(item)
        time = adapter.get('time')
        if time:
            match_or_not = re.search(r'\n?(.*)\n?', time)
            if match_or_not:
                adapter['time'] = match_or_not.group(1)
            else:
                adapter['time'] = "Non disponible"
        else: 
            adapter['time'] = "Non disponible"
            
        return item
    
    def clean_actors(self, item):
        adapter = ItemAdapter(item)
        actors = adapter.get('actors', [])
        if len(actors) > 0 :
            actors.pop(0)
            if len(actors) > 1 :
                adapter['actors'] = ', '.join(actors)
            else:
                adapter['actors'] = actors[0]
        else:
            adapter['actors'] = "Non disponible"

        return item

    def clean_language(self, item):
        adapter = ItemAdapter(item)
        language = adapter.get('language')
        if language:
            match = re.search(r'\n(\w+)', language)
            if match:
                adapter['language'] = match.group(1)
            else:
                adapter['language'] = "Non disponible"
        else:
            adapter['language'] = "Non disponible"
        return item
    
    def clean_years(self, item):
        adapter = ItemAdapter(item)
        years = adapter.get('years')
        if years:
            years_cleaned = re.search(r'\n?(.*)\n?', years).group(1).strip()
            if years_cleaned:
                adapter['years'] = years_cleaned
            else:
                years_cleaned = None
        else: 
            years_cleaned = "Non disponible"

        return item
    
    def clean_realisator(self, item):
        adapter = ItemAdapter(item)
        realisator = adapter.get('realisator')
        liste_tampon = []
        start = True
        stop = False

        for element in realisator:
            if element.lower() == 'de':
                start = True
            elif element.lower() == 'par':
                stop = True
            elif start and not stop:
                liste_tampon.append(element)
        
        realisator_cleaned = ', '.join(liste_tampon)
        adapter['realisator'] = realisator_cleaned
        return item
    
    def clean_genre(self, item):
        adapter = ItemAdapter(item)
        genre = adapter.get('genre')

        if len(genre) > 1 :
            adapter['genre'] = ', '.join(genre)
        elif len(genre) == 0:
            adapter['genre'] = 'Non disponible'
        else:
            adapter['genre'] = genre[0]

        return item
    
    def clean_country(self, item):
        adapter = ItemAdapter(item)
        genre = adapter.get('country')

        if len(genre) > 1 :
            adapter['country'] = ', '.join(genre)
        elif len(genre) == 0:
            adapter['country'] = "Non disponible"
        else:
            adapter['country'] = genre[0]

        return item
    
    
    def clean_press_score(self, item):
        adapter = ItemAdapter(item)
        press_score = adapter.get('press_score')
        if press_score == "Non disponible":
            adapter['press_score'] = "Non disponible"
        else :
            press_score = press_score.replace(',', '.')
            int_press_score = float(press_score)
            adapter['press_score'] = int_press_score
        return item
    
    def clean_public_score(self, item):
        adapter = ItemAdapter(item)
        public_score = adapter.get('public_score')

        if public_score == "Non disponible":
            adapter['public_score'] = "Non disponible"
        else:
            public_score = public_score.replace(',', '.')
            int_public_score = float(public_score)
            adapter['public_score'] = int_public_score
            
        return item

class AllocineSerieScrapperPipeline(AllocineMovieScrapperPipeline):
    
    def process_item(self, item, spider):
        item = self.clean_annee_de_diffusion(item)
        item = self.clean_time(item)
        item = self.clean_realisator(item)
        item = self.clean_press_score(item)
        item = self.clean_public_score(item)
        item = self.clean_saisons(item)
        item = self.clean_episodes(item)
        item = self.clean_title(item)
        item = self.clean_actors(item)

        return item
        
    def clean_title(self, item):

        adapter = ItemAdapter(item)
        title = adapter.get('title')
        if title:
            adapter['title'] = title
        else:
            adapter['title'] = None
        return item
    
    def clean_annee_de_diffusion(self, item):
        adapter = ItemAdapter(item)
        annee = adapter.get('année_de_diffusion')
        cleaned_annee = re.search(r'\n?(.*)\n?', annee).group(1)
        adapter['année_de_diffusion'] = cleaned_annee
        return item

    def clean_realisator(self, item):
        adapter = ItemAdapter(item)
        realisator = adapter.get('realisator')
        if len(realisator) >= 1:
            adapter['realisator'] = realisator
        else: 
            adapter['realisator'] = None
        return item
    
    def clean_saisons(self, item):
        adapter = ItemAdapter(item)
        saisons = adapter.get("nbr_saisons")
        cleaned_saison = int(saisons.split()[0])
        adapter["nbr_saisons"] = cleaned_saison
        return item
    
    def clean_episodes(self, item):
        adapter = ItemAdapter(item)
        episodes = adapter.get("nbr_episodes")
        cleaned_episode = int(episodes.split()[0])
        adapter["nbr_episodes"] = cleaned_episode
        return item
    
    def clean_actors(self, item):
        adapter = ItemAdapter(item)
        actors = adapter.get('title')
        if actors:
            adapter['title'] = actors
        else:
            adapter['title'] = None
        return item
# if "__main__" == __name__:
#     objet = ImdbscrapperPipeline()
#     objet.clean_mention(item)
