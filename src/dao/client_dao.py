"""
DAO (Data Access Object) pour la gestion des clients
Couche d'accès aux données pour les opérations CRUD sur la table Clients
"""

from typing import List, Optional, Dict, Any
from .database import db


class ClientDAO:
    """Classe d'accès aux données pour les clients"""
    
    @staticmethod
    def create(nom: str, prenom: str, email: str, telephone: str = None, ville: str = None) -> int:
        """
        NIVEAU 1 - Insertion de données
        Crée un nouveau client dans la base de données
        
        Args:
            nom: Nom du client
            prenom: Prénom du client
            email: Email du client (unique)
            telephone: Numéro de téléphone (optionnel)
            ville: Ville du client (optionnel)
        
        Returns:
            ID du client créé
        """
        query = """
            INSERT INTO Clients (nom, prenom, email, telephone, ville)
            VALUES (?, ?, ?, ?, ?)
        """
        return db.execute_insert(query, (nom, prenom, email, telephone, ville))
    
    @staticmethod
    def get_by_id(client_id: int) -> Optional[Dict[str, Any]]:
        """
        NIVEAU 1 - Sélection avec filtre WHERE
        Récupère un client par son ID
        
        Args:
            client_id: ID du client
        
        Returns:
            Dictionnaire contenant les informations du client ou None
        """
        query = """
            SELECT client_id, nom, prenom, email, telephone, ville, date_creation
            FROM Clients
            WHERE client_id = ?
        """
        results = db.execute_query(query, (client_id,))
        return dict(results[0]) if results else None
    
    @staticmethod
    def get_by_email(email: str) -> Optional[Dict[str, Any]]:
        """
        NIVEAU 1 - Sélection avec filtre WHERE
        Récupère un client par son email
        
        Args:
            email: Email du client
        
        Returns:
            Dictionnaire contenant les informations du client ou None
        """
        query = """
            SELECT client_id, nom, prenom, email, telephone, ville, date_creation
            FROM Clients
            WHERE email = ?
        """
        results = db.execute_query(query, (email,))
        return dict(results[0]) if results else None
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        NIVEAU 1 - Sélection simple
        Récupère tous les clients
        
        Returns:
            Liste de dictionnaires contenant les clients
        """
        query = """
            SELECT client_id, nom, prenom, email, telephone, ville, date_creation
            FROM Clients
            ORDER BY nom, prenom
        """
        results = db.execute_query(query)
        return [dict(row) for row in results]
    
    @staticmethod
    def get_by_ville(ville: str) -> List[Dict[str, Any]]:
        """
        NIVEAU 1 - Sélection avec filtre WHERE
        Récupère tous les clients d'une ville
        
        Args:
            ville: Nom de la ville
        
        Returns:
            Liste de dictionnaires contenant les clients
        """
        query = """
            SELECT client_id, nom, prenom, email, telephone, ville, date_creation
            FROM Clients
            WHERE ville = ?
            ORDER BY nom, prenom
        """
        results = db.execute_query(query, (ville,))
        return [dict(row) for row in results]
    
    @staticmethod
    def update(client_id: int, nom: str = None, prenom: str = None, 
               email: str = None, telephone: str = None, ville: str = None) -> int:
        """
        NIVEAU 1 - Mise à jour de données
        Met à jour les informations d'un client
        
        Args:
            client_id: ID du client à modifier
            nom: Nouveau nom (optionnel)
            prenom: Nouveau prénom (optionnel)
            email: Nouvel email (optionnel)
            telephone: Nouveau téléphone (optionnel)
            ville: Nouvelle ville (optionnel)
        
        Returns:
            Nombre de lignes modifiées
        """
        # Construire la requête dynamiquement selon les champs fournis
        fields = []
        values = []
        
        if nom is not None:
            fields.append("nom = ?")
            values.append(nom)
        if prenom is not None:
            fields.append("prenom = ?")
            values.append(prenom)
        if email is not None:
            fields.append("email = ?")
            values.append(email)
        if telephone is not None:
            fields.append("telephone = ?")
            values.append(telephone)
        if ville is not None:
            fields.append("ville = ?")
            values.append(ville)
        
        if not fields:
            return 0
        
        values.append(client_id)
        query = f"UPDATE Clients SET {', '.join(fields)} WHERE client_id = ?"
        
        return db.execute_update(query, tuple(values))
    
    @staticmethod
    def delete(client_id: int) -> int:
        """
        NIVEAU 1 - Suppression de données
        Supprime un client (si aucune vente associée)
        
        Args:
            client_id: ID du client à supprimer
        
        Returns:
            Nombre de lignes supprimées
        """
        query = "DELETE FROM Clients WHERE client_id = ?"
        return db.execute_update(query, (client_id,))
    
    @staticmethod
    def search(search_term: str) -> List[Dict[str, Any]]:
        """
        NIVEAU 1 - Recherche avec LIKE
        Recherche des clients par nom, prénom ou email
        
        Args:
            search_term: Terme de recherche
        
        Returns:
            Liste de dictionnaires contenant les clients trouvés
        """
        query = """
            SELECT client_id, nom, prenom, email, telephone, ville, date_creation
            FROM Clients
            WHERE nom LIKE ? OR prenom LIKE ? OR email LIKE ?
            ORDER BY nom, prenom
        """
        pattern = f"%{search_term}%"
        results = db.execute_query(query, (pattern, pattern, pattern))
        return [dict(row) for row in results]
    
    @staticmethod
    def count() -> int:
        """
        NIVEAU 2 - Agrégat COUNT
        Compte le nombre total de clients
        
        Returns:
            Nombre de clients
        """
        query = "SELECT COUNT(*) as total FROM Clients"
        result = db.execute_query(query)
        return result[0]['total'] if result else 0
    
    @staticmethod
    def get_clients_with_purchases() -> List[Dict[str, Any]]:
        """
        NIVEAU 2 - Jointure et agrégat
        Récupère les clients avec le nombre d'achats et le montant total
        
        Returns:
            Liste de dictionnaires avec statistiques par client
        """
        query = """
            SELECT 
                c.client_id,
                c.nom,
                c.prenom,
                c.email,
                c.ville,
                COUNT(v.vente_id) as nombre_achats,
                COALESCE(SUM(v.montant_total), 0) as montant_total
            FROM Clients c
            LEFT JOIN Ventes v ON c.client_id = v.client_id
            GROUP BY c.client_id, c.nom, c.prenom, c.email, c.ville
            ORDER BY montant_total DESC
        """
        results = db.execute_query(query)
        return [dict(row) for row in results]
