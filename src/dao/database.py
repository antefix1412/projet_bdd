"""
Module de connexion à la base de données SQLite
Gère la connexion, les transactions et l'exécution des requêtes
"""

import sqlite3
import os
from typing import Optional, List, Tuple, Any
from contextlib import contextmanager


class Database:
    """Classe singleton pour gérer la connexion à la base de données"""
    
    _instance: Optional['Database'] = None
    _db_path: str = None
    
    def __new__(cls, db_path: str = None):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, db_path: str = None):
        """
        Initialise la connexion à la base de données
        
        Args:
            db_path: Chemin vers le fichier de base de données SQLite
        """
        if self._initialized:
            return
            
        if db_path is None:
            # Chemin par défaut
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            db_path = os.path.join(project_root, 'database', 'ventes.db')
        
        self._db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None
        self._initialized = True
    
    def connect(self) -> sqlite3.Connection:
        """
        Établit une connexion à la base de données
        
        Returns:
            Objet de connexion SQLite
        """
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)
            # Activer les clés étrangères
            self._connection.execute("PRAGMA foreign_keys = ON")
            # Configurer le mode Row pour avoir accès par nom de colonne
            self._connection.row_factory = sqlite3.Row
        return self._connection
    
    def close(self):
        """Ferme la connexion à la base de données"""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    @contextmanager
    def get_cursor(self):
        """
        Gestionnaire de contexte pour obtenir un curseur
        Gère automatiquement le commit et le rollback
        
        Yields:
            Curseur de base de données
        """
        connection = self.connect()
        cursor = connection.cursor()
        try:
            yield cursor
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """
        Exécute une requête SELECT et retourne les résultats
        
        Args:
            query: Requête SQL à exécuter
            params: Paramètres de la requête (requête paramétrée)
        
        Returns:
            Liste des lignes résultantes
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Exécute une requête INSERT, UPDATE ou DELETE
        
        Args:
            query: Requête SQL à exécuter
            params: Paramètres de la requête (requête paramétrée)
        
        Returns:
            Nombre de lignes affectées
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount
    
    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """
        Exécute une requête INSERT et retourne l'ID généré
        
        Args:
            query: Requête SQL INSERT à exécuter
            params: Paramètres de la requête (requête paramétrée)
        
        Returns:
            ID de la dernière ligne insérée
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.lastrowid
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """
        Exécute une requête avec plusieurs ensembles de paramètres
        
        Args:
            query: Requête SQL à exécuter
            params_list: Liste de tuples de paramètres
        
        Returns:
            Nombre total de lignes affectées
        """
        with self.get_cursor() as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount
    
    def execute_script(self, script: str):
        """
        Exécute un script SQL (plusieurs requêtes)
        
        Args:
            script: Script SQL à exécuter
        """
        connection = self.connect()
        try:
            connection.executescript(script)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
    
    def get_db_path(self) -> str:
        """Retourne le chemin vers la base de données"""
        return self._db_path


# Instance globale de la base de données
db = Database()
