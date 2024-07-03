# Définition des modèles SQLAlchemy (tables)

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, PrimaryKeyConstraint, Table, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base() #créer une class "Base" (modèle)


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

    # lien avec la table d'association ActorsByMovie et RealisatorByMovie
    actors_by_movie = relationship('ActorsByMovie', back_populates='movies')
    realisator_by_movie = relationship('RealisatorByMovie', back_populates='movies')

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

    # lien avec la table d'association ActorsBySerie et RealisatorBySerie
    actors_by_serie = relationship('ActorsBySerie', back_populates='series')
    realisator_by_serie = relationship('RealisatorBySerie', back_populates='series')


    def __repr__(self):
        return f"{self.title}, {self.date}"
    
class People(Base):
    __tablename__ = "people"
    people_id = Column(Integer, autoincrement=True, primary_key=True)
    people_name = Column(String, index=True)

    # Lien avec la table d'association ActorsByMovie, RealisatorByMovie, ActorsBySerie, RealisatorBySerie
    actors_by_movie = relationship("ActorsByMovie", back_populates='people')
    realisator_by_movie = relationship('RealisatorByMovie', back_populates='people')
    actors_by_serie = relationship('ActorsBySerie', back_populates='people')
    realisator_by_serie = relationship('RealisatorBySerie', back_populates='people')

# table d'association entre People et movies (une pour les acteurs, une pour les realisateurs)
class ActorsByMovie(Base):
    __tablename__ = "actors_by_movie"
    people_id = Column(Integer, ForeignKey('people.people_id')) #ajouter Primary_key=True ?
    movie_id = Column(Integer, ForeignKey('movies.movie_id')) #ajouter Primary_key=True ?

    movies = relationship("Movie", back_populates='actors_by_movie')
    people = relationship("People", back_populates='actors_by_movie')

    __table_args__ = (
        PrimaryKeyConstraint('people_id','movie_id'),
    )

class RealisatorByMovie(Base):
    __tablename__ = "realisator_by_movie"
    people_id = Column(Integer, ForeignKey('people.people_id')) #ajouter Primary_key=True ?
    movie_id = Column(Integer, ForeignKey('movies.movie_id')) #ajouter Primary_key=True ?

    movies = relationship("Movie", back_populates='realisator_by_movie')
    people = relationship("People", back_populates='realisator_by_movie')

    __table_args__ = (
        PrimaryKeyConstraint('people_id','movie_id'),
    )

#Table d'association entre People et Serie (Une pour les acteurs, et une pour les réalisateur)
class ActorsBySerie(Base):
    __tablename__ = "actors_by_serie"
    people_id = Column(Integer, ForeignKey('people.people_id')) #ajouter Primary_key=True ?
    serie_id = Column(Integer, ForeignKey('series.serie_id')) #ajouter Primary_key=True ?

    series = relationship("Serie", back_populates='actors_by_serie')
    people = relationship("People", back_populates='actors_by_serie')

    __table_args__ = (
        PrimaryKeyConstraint('people_id','serie_id'),
    )

class RealisatorBySerie(Base):
    __tablename__ = "realisator_by_serie"
    people_id = Column(Integer, ForeignKey('people.people_id')) #ajouter Primary_key=True ?
    serie_id = Column(Integer, ForeignKey('series.serie_id')) #ajouter Primary_key=True ?

    series = relationship("Serie", back_populates='realisator_by_serie')
    people = relationship("People", back_populates='realisator_by_serie')

    __table_args__ = (
        PrimaryKeyConstraint('people_id','serie_id'),
    )
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
    
class GenreBySerie(Base):

    __tablename__ = "genre_by_serie"
    name_genre = Column(String, index=True)
    serie_id = Column(Integer, ForeignKey('series.serie_id'))
    serie = relationship('Serie', backref="genre_by_serie")
    
    __table_args__ = (
        PrimaryKeyConstraint('name_genre','serie_id'),
    )

    def __repr__(self):
        return f"Genre : {self.name_genre}"
    
class CountryByMovie(Base):
    __tablename__ = "country_by_movie"
    country_name = Column(String, index=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    movie = relationship("Movie", backref="country_by_movie")

    __table_args__ = (
        PrimaryKeyConstraint('country_name', 'movie_id'),
    )

class CountryBySerie(Base):
    __tablename__ = "country_by_serie"
    country_name = Column(String, index=True)
    serie_id = Column(Integer, ForeignKey('series.serie_id'))
    serie = relationship("Serie", backref="country_by_serie")
    
    __table_args__ = (
        PrimaryKeyConstraint('country_name', 'serie_id'),
    )

# engine = create_engine('sqlite:///allocine_scrapping.db', echo = True)
# Base.metadata.create_all(engine)