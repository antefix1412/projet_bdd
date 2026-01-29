"""
Module de gestion de la base de données SQLite
Gestion de réservations d'espaces
"""

import sqlite3
import os

DB_PATH = "reservations.db"


def get_connection():
    """Retourne une connexion à la base de données"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialise la base de données avec les tables"""
    
    # Supprimer l'ancienne base si elle existe
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table Clients
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telephone TEXT,
            entreprise TEXT,
            date_inscription DATE DEFAULT CURRENT_DATE
        )
    """)
    
    # Table Espaces
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Espaces (
            espace_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL CHECK(type IN ('Salle de réunion', 'Bureau temporaire', 'Espace événementiel')),
            capacite INTEGER NOT NULL CHECK(capacite > 0),
            tarif_horaire REAL NOT NULL CHECK(tarif_horaire > 0)
        )
    """)
    
    # Table Reservations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reservations (
            reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            espace_id INTEGER NOT NULL,
            date_reservation DATE NOT NULL,
            heure_debut TIME NOT NULL,
            duree_heures INTEGER NOT NULL CHECK(duree_heures > 0),
            statut TEXT NOT NULL CHECK(statut IN ('Confirmée', 'En attente', 'Annulée', 'Terminée')) DEFAULT 'Confirmée',
            montant_total REAL NOT NULL CHECK(montant_total >= 0),
            date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES Clients(client_id),
            FOREIGN KEY (espace_id) REFERENCES Espaces(espace_id)
        )
    """)
    
    conn.commit()
    conn.close()
    
    print("✅ Base de données initialisée avec succès!")


def populate_sample_data():
    """Remplit la base avec des données de test"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Insertion de clients
    clients = [
        ("Dupont", "Jean", "jean.dupont@email.fr", "0601020304", "TechCorp"),
        ("Martin", "Sophie", "sophie.martin@email.fr", "0602030405", "InnoLab"),
        ("Bernard", "Luc", "luc.bernard@email.fr", "0603040506", "StartupXYZ"),
        ("Petit", "Marie", "marie.petit@email.fr", "0604050607", "Consulting Pro"),
        ("Durand", "Pierre", "pierre.durand@email.fr", "0605060708", "Digital Agency"),
        ("Moreau", "Claire", "claire.moreau@email.fr", "0606070809", "TechCorp"),
        ("Simon", "Thomas", "thomas.simon@email.fr", "0607080910", "InnoLab")
    ]
    
    cursor.executemany(
        "INSERT INTO Clients (nom, prenom, email, telephone, entreprise) VALUES (?, ?, ?, ?, ?)",
        clients
    )
    
    # Insertion d'espaces
    espaces = [
        ("Salle Horizon", "Salle de réunion", 8, 45.00),
        ("Salle Panorama", "Salle de réunion", 12, 65.00),
        ("Salle Innovation", "Salle de réunion", 6, 35.00),
        ("Bureau Zen", "Bureau temporaire", 1, 25.00),
        ("Bureau Focus", "Bureau temporaire", 1, 25.00),
        ("Bureau Premium", "Bureau temporaire", 2, 40.00),
        ("Hall Événementiel A", "Espace événementiel", 50, 150.00),
        ("Hall Événementiel B", "Espace événementiel", 100, 250.00)
    ]
    
    cursor.executemany(
        "INSERT INTO Espaces (nom, type, capacite, tarif_horaire) VALUES (?, ?, ?, ?)",
        espaces
    )
    
    # Insertion de réservations (variées sur janvier 2026)
    reservations = [
        # Semaine 1
        (1, 1, '2026-01-06', '09:00', 3, 'Terminée', 135.00),
        (2, 7, '2026-01-06', '14:00', 4, 'Terminée', 600.00),
        (3, 4, '2026-01-07', '08:00', 8, 'Terminée', 200.00),
        (1, 2, '2026-01-08', '10:00', 2, 'Terminée', 130.00),
        (4, 3, '2026-01-09', '14:00', 2, 'Terminée', 70.00),
        
        # Semaine 2
        (2, 1, '2026-01-12', '09:00', 4, 'Terminée', 180.00),
        (5, 5, '2026-01-13', '08:00', 6, 'Terminée', 150.00),
        (3, 8, '2026-01-14', '18:00', 5, 'Terminée', 1250.00),
        (6, 2, '2026-01-15', '11:00', 3, 'Terminée', 195.00),
        (1, 4, '2026-01-16', '09:00', 4, 'Terminée', 100.00),
        
        # Semaine 3
        (4, 1, '2026-01-19', '10:00', 2, 'Terminée', 90.00),
        (2, 3, '2026-01-20', '14:00', 3, 'Terminée', 105.00),
        (7, 6, '2026-01-21', '08:00', 8, 'Terminée', 320.00),
        (5, 7, '2026-01-22', '10:00', 6, 'Terminée', 900.00),
        (3, 1, '2026-01-23', '15:00', 2, 'Terminée', 90.00),
        
        # Semaine 4
        (1, 2, '2026-01-26', '09:00', 4, 'Confirmée', 260.00),
        (6, 4, '2026-01-27', '08:00', 8, 'Confirmée', 200.00),
        (4, 3, '2026-01-28', '14:00', 2, 'Confirmée', 70.00),
        (2, 8, '2026-01-29', '16:00', 4, 'Confirmée', 1000.00),
        (5, 5, '2026-01-30', '09:00', 5, 'Confirmée', 125.00)
    ]
    
    cursor.executemany(
        "INSERT INTO Reservations (client_id, espace_id, date_reservation, heure_debut, duree_heures, statut, montant_total) VALUES (?, ?, ?, ?, ?, ?, ?)",
        reservations
    )
    
    conn.commit()
    conn.close()
    
    print("✅ Données de test insérées avec succès!")


if __name__ == "__main__":
    init_database()
    populate_sample_data()
