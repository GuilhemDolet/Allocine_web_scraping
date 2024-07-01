# Définition des modèles SQLAlchemy (tables)

from sqlalchemy import Column, Integer, String, Float, ForeignKey, PrimaryKeyConstraint, Table, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from db import engine

Base = declarative_base() #créer une class "Base" (modèle)

# SET UP des tables d'associations pour les relations many to many:
movies_genre_association = Table('le_genre_des_films',
                                Base.metadata,
                                Column('movie_id', Integer, ForeignKey('movies.movie_id')),
                                Column('name_genre'), String, ForeignKey('genre.name_genre'),
                                UniqueConstraint('movie_id', 'genre_id'))
movies_countries_association = Table('la_nationalité_des_films',
                                     Base.metadata,
                                     Column('movie_id', Integer, ForeignKey('movies.movie_id')),
                                     Column('country_name', String, ForeignKey('countries.country_name')),
                                     UniqueConstraint('movie_id', 'country_name'))
movies_people_association = Table('les_acteurs_et_realisateur_du_film',
                                     Base.metadata,
                                     Column('movie_id', Integer, ForeignKey('movies.movie_id')),
                                     Column('people_id', String, ForeignKey('people.people.id')),
                                     UniqueConstraint('movie_id', 'people_id'))
# movies_realisator_association = Table('les_realisateurs_du_film',
#                                      Base.metadata,
#                                      Column('movie_id', Integer, ForeignKey('movies.movie_id')),
#                                      Column('people_id', String, ForeignKey('people.people_id')),
#                                      UniqueConstraint('movie_id', 'people_id'))

series_genre_association = Table('le_genre_des_series',
                                 Base.metadata,
                                 Column('series_id'), Integer, ForeignKey('series.serie_id'),
                                 Column('name_genre'), String, ForeignKey('genre.name_genre'),
                                 UniqueConstraint('series_id', 'name_genre'))
series_countries_association = Table('la_nationalité_des_series',
                                     Base.metadata,
                                     Column('serie_id', Integer, ForeignKey('series.serie_id')),
                                     Column('country_name', String, ForeignKey('countries.country_name')),
                                     UniqueConstraint('serie_id', 'country_name'))
series_people_association = Table('les_acteurs_et_realisateur_de_la_serie',
                                     Base.metadata,
                                     Column('serie_id', Integer, ForeignKey('series.serie_id')),
                                     Column('people_id', String, ForeignKey('people.people.id')),
                                     UniqueConstraint('serie_id', 'people_id'))



class Movie(Base):
    __tablename__ = 'movies'
    movie_id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String)
    date = Column(String)
    public_score = Column(Float)
    press_score = Column(Float)
    language = Column(String)
    duration = Column(String)
    description = Column(String)

    # lien avec entre les tables
    genre = relationship('Genre', secondary=movies_genre_association, back_populates='movies')
    countries = relationship('Countries', secondary=movies_countries_association, back_populates='movies')
    people = relationship('People', secondary=movies_people_association, back_populates="movies")

    def __repr__(self):
        return f"{self.title}, {self.date}"
    
class Serie(Base):

    __tablename__ = 'series'
    serie_id = Column(Integer, utoincrement=True, primary_key=True)
    title = Column(String)
    date = Column(String)
    status = Column(String)
    episodes_nbr = Column(Integer)
    seasons_nbr = Column(Integer)
    public_score = Column(Float)
    press_score = Column(Float)
    language = Column(String)
    duration = Column(String)
    description = Column(String)

    genre = relationship('Genre', secondary=series_genre_association, back_populates='series')
    countries = relationship('Countries', secondary=series_countries_association, back_populates='series')
    people = relationship('People', secondary=series_people_association, back_populates='series')

    def __repr__(self):
        return f"{self.title}, {self.date}"
    
class People(Base):
    __tablename__ = "people"
    people_id = Column(Integer, autoincrement=True, primary_key=True)
    people_name = Column(String, index=True)

    movie = relationship('Movie', secondary=movies_people_association, back_populates='people')
    serie = relationship('Serie', secondary=series_people_association, back_populates='people')

class Genre(Base):

    __tablename__ = "genre"
    name_genre = Column(String, primary_key=True, index=True)
    
    movies = relationship('Movie', secondary=movies_genre_association, back_populates='genre')
    series = relationship('Serie', secondary=movies_genre_association, back_populates='genre')

    def __repr__(self):
        return f"Genre : {self.name_genre}"
    
class Countries(Base):
    __tablename__ = "countries"
    country_name = Column(String, primary_key=True, index=True)

    movies = relationship('Movie', secondary=movies_countries_association, back_populates="countries")
    series = relationship('Serie', secondary=series_countries_association, back_populates="countries")


if __name__ == "__main__":
    # Configuration de la base de données
    Base.metadata.create_all(engine)  