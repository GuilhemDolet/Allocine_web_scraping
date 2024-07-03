# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from sqlalchemy.orm import sessionmaker
from bdd_sqlalchemy.config import DATABASE_URL 
from bdd_sqlalchemy.models import Base, Movie, People, Table, GenreByMovie, CountryByMovie

from sqlalchemy import create_engine

class AllocineMovieScrapperPipeline:
    def process_item(self, item, spider):
        item = self.clean_time(item)
        item = self.clean_actors(item)
        item = self.clean_language(item)
        item = self.clean_years(item)
        item = self.clean_realisator(item)
        # item = self.clean_genre(item)
        # item = self.clean_country(item)
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
            adapter['actors'] = actors
        else:
            adapter['actors'] = actors #supossement une liste vide

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
    
    # def clean_genre(self, item):
        adapter = ItemAdapter(item)
        genre = adapter.get('genre')

        if len(genre) > 1 :
            adapter['genre'] = ', '.join(genre)
        elif len(genre) == 0:
            adapter['genre'] = 'Non disponible'
        else:
            adapter['genre'] = genre[0]

        return item
    
    # def clean_country(self, item):
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


class DatabasePipeline:
  
    def __init__(self):
        # initialise une session SQLAlchemy
        engine = create_engine(DATABASE_URL, echo = True)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine) # Fabrique de session. Toujours besoin de l'instancier plus tard

    def process_item(self, item, spider):
        # Créer une instance de Movie
        session = self.Session()
        self.load_movie_table(item, session, spider)
        return item

    def load_movie_table(self, item, session, spider):
        # Check pour éviter les doublons:
        movie = session.query(Movie).filter_by(title = item.get('title')).first()
        if movie is None:
            movie = Movie(
                title = item.get('title'),
                press_score = item.get('press_score'),
                public_score = item.get('public_score'),
                duration = item.get('time'),
                language = item.get('language'),
                date = item.get('years'),
                description = item.get('description')
            )
            session.add(movie)
            session.flush() #Flush pour pouvoir récupérer le movie_id 

        # Ajout des données vers la table Genre_by_movies
        for genre in item.get('genre', []):
            genre_by_movie_id = session.query(GenreByMovie).filter_by(name_genre=genre, movie_id=movie.movie_id).first()
            if genre_by_movie_id is None:
                nouvelle_ligne = GenreByMovie(name_genre=genre, movie_id=movie.movie_id)
                session.add(nouvelle_ligne)
                session.flush() 
        
        # Ajout des données vers la table Country_by_movies
        for country in item.get('country', []):
            country_by_movie_id = session.query(CountryByMovie).filter_by(country_name=country, movie_id=movie.movie_id).first()
            if country_by_movie_id is None:
                nouvelle_ligne = CountryByMovie(country_name=country, movie_id=movie.movie_id)
                session.add(nouvelle_ligne)
                session.flush() 
        #------------ MANY TO MANY -------------------------------#
        # # Lien avec la table People.
        # for actor in item.get('actors', []):
        #     people_actor = session.query(People).filter_by(people_name = actor).first()
        #     if people_actor is None:
        #         une_ligne_de_ma_table_people = People(people_name=actor)
        #         session.add(une_ligne_de_ma_table_people)
        #         session.flush() # Cela force l'exécution immédiate de l'INSERT SQL pour la nouvelle personne, assurant ainsi que l'ID de la nouvelle personne est disponible.

        #     if people_actor and people_actor not in movie.people:
        #         movie.people.append(people_actor) # Cela établit la relation many-to-many entre le film et la personne en ajoutant une entrée dans la table d'association movies_people_association.
        # ---------------------------------------------------------#
        try:
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
    
