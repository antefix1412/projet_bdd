"""
Module de connexion à la base de données SQLite
Gère la création du schéma et les opérations SQL de base
"""

import sqlite3
import os

# Chemin vers la base de données
DB_PATH = os.path.join(os.path.dirname(__file__), 'ventes.db')


def get_connection():
    """Retourne une connexion à la base de données"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
    conn.execute("PRAGMA foreign_keys = ON")  # Activer les clés étrangères
    return conn


def init_database():
    """Crée les tables de la base de données"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Suppression des tables si elles existent
        cursor.execute("DROP TABLE IF EXISTS Ventes")
        cursor.execute("DROP TABLE IF EXISTS Produits")
        cursor.execute("DROP TABLE IF EXISTS Clients")
        
        # Table Clients
        cursor.execute("""
            CREATE TABLE Clients (
                client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                ville TEXT
            )
        """)
        
        # Table Produits
        cursor.execute("""
            CREATE TABLE Produits (
                produit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prix_unitaire REAL NOT NULL CHECK(prix_unitaire > 0),
                categorie TEXT,
                stock INTEGER DEFAULT 0 CHECK(stock >= 0)
            )
        """)
        
        # Table Ventes
        cursor.execute("""
            CREATE TABLE Ventes (
                vente_id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                produit_id INTEGER NOT NULL,
                quantite INTEGER NOT NULL CHECK(quantite > 0),
                prix_unitaire REAL NOT NULL CHECK(prix_unitaire > 0),
                montant_total REAL NOT NULL,
                date_vente DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES Clients(client_id),
                FOREIGN KEY (produit_id) REFERENCES Produits(produit_id)
            )
        """)
        
        conn.commit()
        print("Base de données initialisée avec succès")
        
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de l'initialisation: {e}")
        raise
    finally:
        conn.close()


def populate_sample_data():
    """Insère des données de test dans la base"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # NIVEAU 1 - Insertions de clients
        clients = [
            ('Dupont', 'Marie', 'marie.dupont@email.com', 'Paris'),
            ('Martin', 'Pierre', 'pierre.martin@email.com', 'Lyon'),
            ('Bernard', 'Sophie', 'sophie.bernard@email.com', 'Paris'),
            ('Dubois', 'Luc', 'luc.dubois@email.com', 'Marseille'),
            ('Laurent', 'Julie', 'julie.laurent@email.com', 'Lyon')
        ]
        
        cursor.executemany(
            "INSERT INTO Clients (nom, prenom, email, ville) VALUES (?, ?, ?, ?)",
            clients
        )
        
        # NIVEAU 1 - Insertions de produits
        produits = [
            ('Ordinateur portable', 899.99, 'Informatique', 15),
            ('Souris sans fil', 29.99, 'Informatique', 50),
            ('Clavier mécanique', 89.99, 'Informatique', 30),
            ('Écran 24 pouces', 199.99, 'Informatique', 20),
            ('Casque audio', 79.99, 'Audio', 25),
            ('Webcam HD', 59.99, 'Informatique', 18),
            ('Disque dur externe', 119.99, 'Informatique', 12),
            ('Enceinte Bluetooth', 49.99, 'Audio', 40)
        ]
        
        cursor.executemany(
            "INSERT INTO Produits (nom, prix_unitaire, categorie, stock) VALUES (?, ?, ?, ?)",
            produits
        )
        
        # NIVEAU 1 - Insertions de ventes avec calcul du montant
        ventes = [
            (1, 1, 2, 899.99),   # Marie achète 2 ordinateurs
            (2, 2, 5, 29.99),    # Pierre achète 5 souris
            (1, 5, 1, 79.99),    # Marie achète 1 casque
            (3, 3, 2, 89.99),    # Sophie achète 2 claviers
            (4, 4, 1, 199.99),   # Luc achète 1 écran
            (2, 6, 3, 59.99),    # Pierre achète 3 webcams
            (5, 2, 10, 29.99),   # Julie achète 10 souris
            (3, 7, 1, 119.99),   # Sophie achète 1 disque dur
            (1, 8, 2, 49.99),    # Marie achète 2 enceintes
            (4, 1, 1, 899.99),   # Luc achète 1 ordinateur
            (5, 3, 1, 89.99),    # Julie achète 1 clavier
            (2, 5, 2, 79.99)     # Pierre achète 2 casques
        ]
        
        for client_id, produit_id, quantite, prix_unitaire in ventes:
            montant_total = quantite * prix_unitaire
            cursor.execute(
                """INSERT INTO Ventes (client_id, produit_id, quantite, prix_unitaire, montant_total) 
                   VALUES (?, ?, ?, ?, ?)""",
                (client_id, produit_id, quantite, prix_unitaire, montant_total)
            )
        
        conn.commit()
        print("Données de test insérées avec succès")
        
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de l'insertion des données: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    print("=== Initialisation de la base de données ===")
    init_database()
    populate_sample_data()
    print("=== Terminé ===")
