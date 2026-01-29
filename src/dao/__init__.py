"""Module d'initialisation du package DAO"""

from .database import Database, db
from .client_dao import ClientDAO
from .produit_dao import ProduitDAO
from .vente_dao import VenteDAO

__all__ = ['Database', 'db', 'ClientDAO', 'ProduitDAO', 'VenteDAO']
