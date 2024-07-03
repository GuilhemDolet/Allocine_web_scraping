# Définition des modèles SQLAlchemy (tables)

from sqlalchemy import Column, Integer, String, Float, ForeignKey, PrimaryKeyConstraint, Table, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base() #créer une class "Base" (modèle)

# SET UP des tables d'associations pour les relations many to many:

movies_people_association = Table('les_acteurs_et_realisateur_du_film',
                                     Base.metadata,
                                     Column('movie_id', Integer, ForeignKey('movies.movie_id')),
                                     Column('people_id', Integer, ForeignKey('people.people_id')),
                                     UniqueConstraint('movie_id', 'people_id'))

series_people_association = Table('les_acteurs_et_realisateur_de_la_serie',
                                     Base.metadata,
                                     Column('serie_id', Integer, ForeignKey('series.serie_id')),
                                     Column('people_id', Integer, ForeignKey('people.people_id')),
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

    # lien avec la table People
    people = relationship('People', secondary=movies_people_association, back_populates="movies")

    def __repr__(self):
        return f"{self.title}, {self.date}"
    
class Serie(Base):

    __tablename__ = 'series'
    serie_id = Column(Integer, autoincrement=True, primary_key=True)
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

    people = relationship('People', secondary=series_people_association, back_populates='series')

    def __repr__(self):
        return f"{self.title}, {self.date}"
    
class People(Base):
    __tablename__ = "people"
    people_id = Column(Integer, autoincrement=True, primary_key=True)
    people_name = Column(String, index=True)

    movies = relationship('Movie', secondary=movies_people_association, back_populates='people')
    series = relationship('Serie', secondary=series_people_association, back_populates='people')

class GenreByMovie(Base):

    __tablename__ = "genre_by_movie"
    name_genre = Column(String, index=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    movie = relationship('Movie', backref="genre_by_movie")
    
    __table_args__ = (
        PrimaryKeyConstraint('name_genre','movie_id'),
    )

    def __repr__(self):
        return f"Genre : {self.name_genre}"
    
# class GenreBySerie(Base):

#     __tablename__ = "genre_by_serie"
#     name_genre = Column(String, index=True)
#     serie_id = Column(Integer, ForeignKey('series.serie_id'))
#     serie = relationship('Serie', backref="genre_by_serie")
    
#     __table_args__ = (
#         PrimaryKeyConstraint('name_genre','serie_id'),
#     )

#     def __repr__(self):
#         return f"Genre : {self.name_genre}"
    
class CountryByMovie(Base):
    __tablename__ = "country_by_movie"
    country_name = Column(String, index=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    movie = relationship("Movie", backref="country_by_movie")

    __table_args__ = (
        PrimaryKeyConstraint('country_name', 'movie_id'),
    )

# class CountryBySerie(Base):
#     __tablename__ = "country_by_serie"
#     country_name = Column(String, index=True)
#     serie_id = Column(Integer, ForeignKey('series.serie_id'))
#     serie = relationship("Serie", backref="country_by_serie")
    
#     __table_args__ = (
#         PrimaryKeyConstraint('country_name', 'serie_id'),
#     )

