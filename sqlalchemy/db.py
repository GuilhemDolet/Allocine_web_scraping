 # Configuration de la base de données (engine, session)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

#Créer un engine => lien de connexion avec la BDD
engine = create_engine(DATABASE_URL, echo = True)

#Créer une session 
Session = sessionmaker(bind=engine) # Like a dispenser : C'est une fabrique de session. Session ici n'est pas une instance de session elle-même, mais une fabrique qui produit des instances de session. Quand on appelle Session(), cela crée une nouvelle instance de session.
# session = Session() 

def get_session():
    # return une instance de Session()
    return Session()