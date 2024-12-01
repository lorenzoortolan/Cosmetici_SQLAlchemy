from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect


# Crea una base per i modelli
Base = declarative_base()

# Definizione della classe Prodotto
class Prodotto(Base):
    __tablename__ = 'prodotti'
    
    CodiceProdotto = Column(Integer, primary_key=True)
    Nome = Column(String)
    Descrizione = Column(String)
    Prezzo = Column(Float)
    Disponibilita = Column(Integer)
    CodiceCategoria = Column(Integer, ForeignKey('categorie.CodiceCategoria'))

    # Relazione con la categoria
    categoria = relationship("Categoria")

# Definizione della classe Categoria
class Categoria(Base):
    __tablename__ = 'categorie'
    
    CodiceCategoria = Column(Integer, primary_key=True)
    NomeCategoria = Column(String)

# Connessione al database SQLite
DATABASE_URL = "sqlite:///ecommerce.db"
engine = create_engine(DATABASE_URL, echo=True)


# Creazione delle tabelle
Base.metadata.create_all(engine)

# Creazione di una sessione per interagire con il database
Session = sessionmaker(bind=engine)
session = Session()

# Inserimento di un nuovo prodotto
# Inserimento di nuovi prodotti
def inserisci_prodotti():
    # Creazione di una nuova categoria
    nuova_categoria = Categoria(NomeCategoria='Cosmetici')
    session.add(nuova_categoria)
    session.commit()

    # Aggiunta dei prodotti
    prodotti = [
        Prodotto(
            Nome='Crema Idratante',
            Descrizione='Crema per la pelle secca',
            Prezzo=19.99,
            Disponibilita=100,
            CodiceCategoria=nuova_categoria.CodiceCategoria
        ),
        Prodotto(
            Nome='Shampoo Nutriente',
            Descrizione='Shampoo per capelli secchi',
            Prezzo=15.49,
            Disponibilita=50,
            CodiceCategoria=nuova_categoria.CodiceCategoria
        ),
        Prodotto(
            Nome='Balsamo Ristrutturante',
            Descrizione='Balsamo per capelli danneggiati',
            Prezzo=12.99,
            Disponibilita=80,
            CodiceCategoria=nuova_categoria.CodiceCategoria
        )
    ]

    # Aggiunta prodotti alla sessione
    session.add_all(prodotti)
    session.commit()

    # Messaggio di conferma
    for prodotto in prodotti:
        print(f"Prodotto {prodotto.Nome} inserito con successo!")

# Lettura prodotti dal database
def leggi_prodotti():
    prodotti = session.query(Prodotto).all()
    for prodotto in prodotti:
        print(f"Nome: {prodotto.Nome}, Prezzo: {prodotto.Prezzo}, Categoria: {prodotto.categoria.NomeCategoria}")

# Funzione per aggiornare un prodotto
def aggiorna_prodotto(codice_prodotto, nuovo_prezzo):
    prodotto = session.query(Prodotto).filter_by(CodiceProdotto=codice_prodotto).first()
    if prodotto:
        prodotto.Prezzo = nuovo_prezzo
        session.commit()
        print(f"Prodotto {prodotto.Nome} aggiornato con successo!")
    else:
        print(f"Prodotto con codice {codice_prodotto} non trovato.")

# Funzione per cancellare un prodotto
def cancella_prodotto(codice_prodotto):
    prodotto = session.query(Prodotto).filter_by(CodiceProdotto=codice_prodotto).first()
    if prodotto:
        session.delete(prodotto)
        session.commit()
        print(f"Prodotto {prodotto.Nome} cancellato con successo!")
    else:
        print(f"Prodotto con codice {codice_prodotto} non trovato.")

# Esecuzione delle funzioni di esempio
if __name__ == '__main__':
    # Inserimento di un prodotto
    inserisci_prodotti()
    
    # Lettura dei prodotti
    leggi_prodotti()
    
    # Aggiorna un prodotto (modifica il prezzo di un prodotto esistente)
    aggiorna_prodotto(1, 24.99)
    
    # Cancellazione di un prodotto
    cancella_prodotto(1)
    
    # Lettura prodotti per vedere i cambiamenti
    leggi_prodotti()


inspector = inspect (engine)
tables = inspector.get_table_names()
print("Tabelle nel database:", tables)
