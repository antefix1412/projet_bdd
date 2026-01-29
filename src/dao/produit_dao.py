"""
DAO (Data Access Object) pour la gestion des produits
Couche d'accès aux données pour les opérations CRUD sur la table Produits
"""

from typing import List, Optional, Dict, Any
from decimal import Decimal
from .database import db


class ProduitDAO:
    """Classe d'accès aux données pour les produits"""
    
    @staticmethod
    def create(nom: str, prix_unitaire: float, description: str = None, 
               categorie: str = None, stock: int = 0) -> int:
        """
        NIVEAU 1 - Insertion de données
        Crée un nouveau produit dans la base de données
        
        Args:
            nom: Nom du produit
            prix_unitaire: Prix unitaire du produit
            description: Description du produit (optionnel)
            categorie: Catégorie du produit (optionnel)
            stock: Quantité en stock (par défaut 0)
        
        Returns:
            ID du produit créé
        """
        query = """
            INSERT INTO Produits (nom, prix_unitaire, description, categorie, stock)
            VALUES (?, ?, ?, ?, ?)
        """
        return db.execute_insert(query, (nom, prix_unitaire, description, categorie, stock))
    
    @staticmethod
    def get_by_id(produit_id: int) -> Optional[Dict[str, Any]]:
        """
        NIVEAU 1 - Sélection avec filtre WHERE
        Récupère un produit par son ID
        
        Args:
            produit_id: ID du produit
        
        Returns:
            Dictionnaire contenant les informations du produit ou None
        """
        query = """
            SELECT produit_id, nom, description, prix_unitaire, categorie, stock, date_ajout
            FROM Produits
            WHERE produit_id = ?
        """
        results = db.execute_query(query, (produit_id,))
        return dict(results[0]) if results else None
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        NIVEAU 1 - Sélection simple
        Récupère tous les produits
        
        Returns:
            Liste de dictionnaires contenant les produits
        """
        query = """
            SELECT produit_id, nom, description, prix_unitaire, categorie, stock, date_ajout
            FROM Produits
            ORDER BY categorie, nom
        """
        results = db.execute_query(query)
        return [dict(row) for row in results]
    
    @staticmethod
    def get_by_categorie(categorie: str) -> List[Dict[str, Any]]:
        """
        NIVEAU 1 - Sélection avec filtre WHERE
        Récupère tous les produits d'une catégorie
        
        Args:
            categorie: Nom de la catégorie
        
        Returns:
            Liste de dictionnaires contenant les produits
        """
        query = """
            SELECT produit_id, nom, description, prix_unitaire, categorie, stock, date_ajout
            FROM Produits
            WHERE categorie = ?
            ORDER BY nom
        """
        results = db.execute_query(query, (categorie,))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_categories() -> List[str]:
        """
        NIVEAU 2 - SELECT DISTINCT
        Récupère toutes les catégories de produits distinctes
        
        Returns:
            Liste des catégories
        """
        query = """
            SELECT DISTINCT categorie
            FROM Produits
            WHERE categorie IS NOT NULL
            ORDER BY categorie
        """
        results = db.execute_query(query)
        return [row['categorie'] for row in results]
    
    @staticmethod
    def get_in_stock() -> List[Dict[str, Any]]:
        """
        NIVEAU 1 - Sélection avec filtre WHERE
        Récupère les produits en stock (quantité > 0)
        
        Returns:
            Liste de dictionnaires contenant les produits en stock
        """
        query = """
            SELECT produit_id, nom, description, prix_unitaire, categorie, stock, date_ajout
            FROM Produits
            WHERE stock > 0
            ORDER BY stock DESC
        """
        results = db.execute_query(query)
        return [dict(row) for row in results]
    
    @staticmethod
    def get_out_of_stock() -> List[Dict[str, Any]]:
        """
        NIVEAU 1 - Sélection avec filtre WHERE
        Récupère les produits en rupture de stock
        
        Returns:
            Liste de dictionnaires contenant les produits en rupture
        """
        query = """
            SELECT produit_id, nom, description, prix_unitaire, categorie, stock, date_ajout
            FROM Produits
            WHERE stock = 0
            ORDER BY nom
        """
        results = db.execute_query(query)
        return [dict(row) for row in results]
    
    @staticmethod
    def update(produit_id: int, nom: str = None, prix_unitaire: float = None,
               description: str = None, categorie: str = None, stock: int = None) -> int:
        """
        NIVEAU 1 - Mise à jour de données
        Met à jour les informations d'un produit
        
        Args:
            produit_id: ID du produit à modifier
            nom: Nouveau nom (optionnel)
            prix_unitaire: Nouveau prix (optionnel)
            description: Nouvelle description (optionnel)
            categorie: Nouvelle catégorie (optionnel)
            stock: Nouveau stock (optionnel)
        
        Returns:
            Nombre de lignes modifiées
        """
        fields = []
        values = []
        
        if nom is not None:
            fields.append("nom = ?")
            values.append(nom)
        if prix_unitaire is not None:
            fields.append("prix_unitaire = ?")
            values.append(prix_unitaire)
        if description is not None:
            fields.append("description = ?")
            values.append(description)
        if categorie is not None:
            fields.append("categorie = ?")
            values.append(categorie)
        if stock is not None:
            fields.append("stock = ?")
            values.append(stock)
        
        if not fields:
            return 0
        
        values.append(produit_id)
        query = f"UPDATE Produits SET {', '.join(fields)} WHERE produit_id = ?"
        
        return db.execute_update(query, tuple(values))
    
    @staticmethod
    def update_stock(produit_id: int, quantite: int) -> int:
        """
        NIVEAU 1 - Mise à jour de données
        Met à jour le stock d'un produit
        
        Args:
            produit_id: ID du produit
            quantite: Nouvelle quantité en stock
        
        Returns:
            Nombre de lignes modifiées
        """
        query = "UPDATE Produits SET stock = ? WHERE produit_id = ?"
        return db.execute_update(query, (quantite, produit_id))
    
    @staticmethod
    def decrease_stock(produit_id: int, quantite: int) -> int:
        """
        NIVEAU 1 - Mise à jour avec calcul
        Diminue le stock d'un produit
        
        Args:
            produit_id: ID du produit
            quantite: Quantité à retirer du stock
        
        Returns:
            Nombre de lignes modifiées
        """
        query = "UPDATE Produits SET stock = stock - ? WHERE produit_id = ? AND stock >= ?"
        return db.execute_update(query, (quantite, produit_id, quantite))
    
    @staticmethod
    def increase_stock(produit_id: int, quantite: int) -> int:
        """
        NIVEAU 1 - Mise à jour avec calcul
        Augmente le stock d'un produit
        
        Args:
            produit_id: ID du produit
            quantite: Quantité à ajouter au stock
        
        Returns:
            Nombre de lignes modifiées
        """
        query = "UPDATE Produits SET stock = stock + ? WHERE produit_id = ?"
        return db.execute_update(query, (quantite, produit_id))
    
    @staticmethod
    def delete(produit_id: int) -> int:
        """
        NIVEAU 1 - Suppression de données
        Supprime un produit (si aucune vente associée)
        
        Args:
            produit_id: ID du produit à supprimer
        
        Returns:
            Nombre de lignes supprimées
        """
        query = "DELETE FROM Produits WHERE produit_id = ?"
        return db.execute_update(query, (produit_id,))
    
    @staticmethod
    def search(search_term: str) -> List[Dict[str, Any]]:
        """
        NIVEAU 1 - Recherche avec LIKE
        Recherche des produits par nom ou description
        
        Args:
            search_term: Terme de recherche
        
        Returns:
            Liste de dictionnaires contenant les produits trouvés
        """
        query = """
            SELECT produit_id, nom, description, prix_unitaire, categorie, stock, date_ajout
            FROM Produits
            WHERE nom LIKE ? OR description LIKE ?
            ORDER BY nom
        """
        pattern = f"%{search_term}%"
        results = db.execute_query(query, (pattern, pattern))
        return [dict(row) for row in results]
    
    @staticmethod
    def count() -> int:
        """
        NIVEAU 2 - Agrégat COUNT
        Compte le nombre total de produits
        
        Returns:
            Nombre de produits
        """
        query = "SELECT COUNT(*) as total FROM Produits"
        result = db.execute_query(query)
        return result[0]['total'] if result else 0
    
    @staticmethod
    def get_average_price() -> float:
        """
        NIVEAU 2 - Agrégat AVG
        Calcule le prix moyen des produits
        
        Returns:
            Prix moyen
        """
        query = "SELECT AVG(prix_unitaire) as moyenne FROM Produits"
        result = db.execute_query(query)
        return float(result[0]['moyenne']) if result and result[0]['moyenne'] else 0.0
    
    @staticmethod
    def get_products_with_sales() -> List[Dict[str, Any]]:
        """
        NIVEAU 2 - Jointure et agrégats
        Récupère les produits avec statistiques de ventes
        
        Returns:
            Liste de dictionnaires avec statistiques par produit
        """
        query = """
            SELECT 
                p.produit_id,
                p.nom,
                p.categorie,
                p.prix_unitaire,
                p.stock,
                COUNT(v.vente_id) as nombre_ventes,
                COALESCE(SUM(v.quantite), 0) as quantite_vendue,
                COALESCE(SUM(v.montant_total), 0) as chiffre_affaires
            FROM Produits p
            LEFT JOIN Ventes v ON p.produit_id = v.produit_id
            GROUP BY p.produit_id, p.nom, p.categorie, p.prix_unitaire, p.stock
            ORDER BY chiffre_affaires DESC
        """
        results = db.execute_query(query)
        return [dict(row) for row in results]
