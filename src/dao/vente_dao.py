"""
DAO (Data Access Object) pour la gestion des ventes
Couche d'accès aux données pour les opérations CRUD sur la table Ventes
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date
from .database import db


class VenteDAO:
    """Classe d'accès aux données pour les ventes"""
    
    @staticmethod
    def create(client_id: int, produit_id: int, quantite: int, prix_unitaire: float) -> int:
        """
        NIVEAU 1 - Insertion de données avec calcul
        Crée une nouvelle vente dans la base de données
        
        Args:
            client_id: ID du client
            produit_id: ID du produit
            quantite: Quantité vendue
            prix_unitaire: Prix unitaire au moment de la vente
        
        Returns:
            ID de la vente créée
        """
        montant_total = quantite * prix_unitaire
        query = """
            INSERT INTO Ventes (client_id, produit_id, quantite, prix_unitaire, montant_total)
            VALUES (?, ?, ?, ?, ?)
        """
        return db.execute_insert(query, (client_id, produit_id, quantite, prix_unitaire, montant_total))
    
    @staticmethod
    def create_with_date(client_id: int, produit_id: int, quantite: int, 
                        prix_unitaire: float, date_vente: str) -> int:
        """
        NIVEAU 1 - Insertion de données avec date spécifique
        Crée une nouvelle vente avec une date personnalisée
        
        Args:
            client_id: ID du client
            produit_id: ID du produit
            quantite: Quantité vendue
            prix_unitaire: Prix unitaire au moment de la vente
            date_vente: Date de la vente (format: YYYY-MM-DD HH:MM:SS)
        
        Returns:
            ID de la vente créée
        """
        montant_total = quantite * prix_unitaire
        query = """
            INSERT INTO Ventes (client_id, produit_id, quantite, prix_unitaire, montant_total, date_vente)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        return db.execute_insert(query, (client_id, produit_id, quantite, prix_unitaire, montant_total, date_vente))
    
    @staticmethod
    def get_by_id(vente_id: int) -> Optional[Dict[str, Any]]:
        """
        NIVEAU 2 - Jointure entre tables
        Récupère une vente complète par son ID avec informations client et produit
        
        Args:
            vente_id: ID de la vente
        
        Returns:
            Dictionnaire contenant les informations complètes de la vente ou None
        """
        query = """
            SELECT 
                v.vente_id,
                v.date_vente,
                v.quantite,
                v.prix_unitaire,
                v.montant_total,
                c.client_id,
                c.nom || ' ' || c.prenom as nom_client,
                c.email as email_client,
                p.produit_id,
                p.nom as nom_produit,
                p.categorie
            FROM Ventes v
            INNER JOIN Clients c ON v.client_id = c.client_id
            INNER JOIN Produits p ON v.produit_id = p.produit_id
            WHERE v.vente_id = ?
        """
        results = db.execute_query(query, (vente_id,))
        return dict(results[0]) if results else None
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        NIVEAU 2 - Jointure entre tables
        Récupère toutes les ventes avec détails
        
        Returns:
            Liste de dictionnaires contenant les ventes
        """
        query = """
            SELECT 
                v.vente_id,
                v.date_vente,
                v.quantite,
                v.prix_unitaire,
                v.montant_total,
                c.nom || ' ' || c.prenom as nom_client,
                p.nom as nom_produit,
                p.categorie
            FROM Ventes v
            INNER JOIN Clients c ON v.client_id = c.client_id
            INNER JOIN Produits p ON v.produit_id = p.produit_id
            ORDER BY v.date_vente DESC
        """
        results = db.execute_query(query)
        return [dict(row) for row in results]
    
    @staticmethod
    def get_by_client(client_id: int) -> List[Dict[str, Any]]:
        """
        NIVEAU 2 - Jointure avec filtre WHERE
        Récupère toutes les ventes d'un client
        
        Args:
            client_id: ID du client
        
        Returns:
            Liste de dictionnaires contenant les ventes du client
        """
        query = """
            SELECT 
                v.vente_id,
                v.date_vente,
                v.quantite,
                v.prix_unitaire,
                v.montant_total,
                p.nom as nom_produit,
                p.categorie
            FROM Ventes v
            INNER JOIN Produits p ON v.produit_id = p.produit_id
            WHERE v.client_id = ?
            ORDER BY v.date_vente DESC
        """
        results = db.execute_query(query, (client_id,))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_by_produit(produit_id: int) -> List[Dict[str, Any]]:
        """
        NIVEAU 2 - Jointure avec filtre WHERE
        Récupère toutes les ventes d'un produit
        
        Args:
            produit_id: ID du produit
        
        Returns:
            Liste de dictionnaires contenant les ventes du produit
        """
        query = """
            SELECT 
                v.vente_id,
                v.date_vente,
                v.quantite,
                v.prix_unitaire,
                v.montant_total,
                c.nom || ' ' || c.prenom as nom_client
            FROM Ventes v
            INNER JOIN Clients c ON v.client_id = c.client_id
            WHERE v.produit_id = ?
            ORDER BY v.date_vente DESC
        """
        results = db.execute_query(query, (produit_id,))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_by_date_range(date_debut: str, date_fin: str) -> List[Dict[str, Any]]:
        """
        NIVEAU 2 - Jointure avec filtres multiples
        Récupère les ventes dans une période donnée
        
        Args:
            date_debut: Date de début (format: YYYY-MM-DD)
            date_fin: Date de fin (format: YYYY-MM-DD)
        
        Returns:
            Liste de dictionnaires contenant les ventes de la période
        """
        query = """
            SELECT 
                v.vente_id,
                v.date_vente,
                v.quantite,
                v.prix_unitaire,
                v.montant_total,
                c.nom || ' ' || c.prenom as nom_client,
                p.nom as nom_produit,
                p.categorie
            FROM Ventes v
            INNER JOIN Clients c ON v.client_id = c.client_id
            INNER JOIN Produits p ON v.produit_id = p.produit_id
            WHERE DATE(v.date_vente) BETWEEN ? AND ?
            ORDER BY v.date_vente DESC
        """
        results = db.execute_query(query, (date_debut, date_fin))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_recent(limit: int = 10) -> List[Dict[str, Any]]:
        """
        NIVEAU 2 - Jointure avec LIMIT
        Récupère les ventes les plus récentes
        
        Args:
            limit: Nombre de ventes à récupérer
        
        Returns:
            Liste de dictionnaires contenant les ventes récentes
        """
        query = """
            SELECT 
                v.vente_id,
                v.date_vente,
                v.quantite,
                v.prix_unitaire,
                v.montant_total,
                c.nom || ' ' || c.prenom as nom_client,
                p.nom as nom_produit
            FROM Ventes v
            INNER JOIN Clients c ON v.client_id = c.client_id
            INNER JOIN Produits p ON v.produit_id = p.produit_id
            ORDER BY v.date_vente DESC
            LIMIT ?
        """
        results = db.execute_query(query, (limit,))
        return [dict(row) for row in results]
    
    @staticmethod
    def delete(vente_id: int) -> int:
        """
        NIVEAU 1 - Suppression de données
        Supprime une vente
        
        Args:
            vente_id: ID de la vente à supprimer
        
        Returns:
            Nombre de lignes supprimées
        """
        query = "DELETE FROM Ventes WHERE vente_id = ?"
        return db.execute_update(query, (vente_id,))
    
    @staticmethod
    def count() -> int:
        """
        NIVEAU 2 - Agrégat COUNT
        Compte le nombre total de ventes
        
        Returns:
            Nombre de ventes
        """
        query = "SELECT COUNT(*) as total FROM Ventes"
        result = db.execute_query(query)
        return result[0]['total'] if result else 0
    
    @staticmethod
    def get_total_revenue() -> float:
        """
        NIVEAU 2 - Agrégat SUM
        Calcule le chiffre d'affaires total
        
        Returns:
            Montant total des ventes
        """
        query = "SELECT COALESCE(SUM(montant_total), 0) as total FROM Ventes"
        result = db.execute_query(query)
        return float(result[0]['total'])
    
    @staticmethod
    def get_average_sale() -> float:
        """
        NIVEAU 2 - Agrégat AVG
        Calcule le montant moyen d'une vente
        
        Returns:
            Montant moyen
        """
        query = "SELECT COALESCE(AVG(montant_total), 0) as moyenne FROM Ventes"
        result = db.execute_query(query)
        return float(result[0]['moyenne'])
    
    @staticmethod
    def get_revenue_by_product() -> List[Dict[str, Any]]:
        """
        NIVEAU 3 - GROUP BY avec agrégats multiples
        Calcule le chiffre d'affaires par produit
        
        Returns:
            Liste de dictionnaires avec statistiques par produit
        """
        query = """
            SELECT 
                p.produit_id,
                p.nom as nom_produit,
                p.categorie,
                COUNT(v.vente_id) as nombre_ventes,
                SUM(v.quantite) as quantite_totale,
                SUM(v.montant_total) as chiffre_affaires,
                AVG(v.montant_total) as vente_moyenne
            FROM Produits p
            LEFT JOIN Ventes v ON p.produit_id = v.produit_id
            GROUP BY p.produit_id, p.nom, p.categorie
            HAVING COUNT(v.vente_id) > 0
            ORDER BY chiffre_affaires DESC
        """
        results = db.execute_query(query)
        return [dict(row) for row in results]
    
    @staticmethod
    def get_revenue_by_client() -> List[Dict[str, Any]]:
        """
        NIVEAU 3 - GROUP BY avec agrégats multiples
        Calcule le chiffre d'affaires par client
        
        Returns:
            Liste de dictionnaires avec statistiques par client
        """
        query = """
            SELECT 
                c.client_id,
                c.nom || ' ' || c.prenom as nom_client,
                c.email,
                c.ville,
                COUNT(v.vente_id) as nombre_achats,
                SUM(v.montant_total) as montant_total,
                AVG(v.montant_total) as achat_moyen
            FROM Clients c
            LEFT JOIN Ventes v ON c.client_id = v.client_id
            GROUP BY c.client_id, c.nom, c.prenom, c.email, c.ville
            HAVING COUNT(v.vente_id) > 0
            ORDER BY montant_total DESC
        """
        results = db.execute_query(query)
        return [dict(row) for row in results]
    
    @staticmethod
    def get_revenue_by_category() -> List[Dict[str, Any]]:
        """
        NIVEAU 3 - GROUP BY avec jointure
        Calcule le chiffre d'affaires par catégorie de produit
        
        Returns:
            Liste de dictionnaires avec statistiques par catégorie
        """
        query = """
            SELECT 
                p.categorie,
                COUNT(v.vente_id) as nombre_ventes,
                SUM(v.quantite) as quantite_totale,
                SUM(v.montant_total) as chiffre_affaires,
                AVG(v.montant_total) as vente_moyenne
            FROM Ventes v
            INNER JOIN Produits p ON v.produit_id = p.produit_id
            WHERE p.categorie IS NOT NULL
            GROUP BY p.categorie
            ORDER BY chiffre_affaires DESC
        """
        results = db.execute_query(query)
        return [dict(row) for row in results]
    
    @staticmethod
    def get_revenue_by_month() -> List[Dict[str, Any]]:
        """
        NIVEAU 3 - GROUP BY avec fonction de date
        Calcule le chiffre d'affaires par mois
        
        Returns:
            Liste de dictionnaires avec statistiques mensuelles
        """
        query = """
            SELECT 
                strftime('%Y-%m', date_vente) as mois,
                COUNT(vente_id) as nombre_ventes,
                SUM(quantite) as quantite_totale,
                SUM(montant_total) as chiffre_affaires,
                AVG(montant_total) as vente_moyenne
            FROM Ventes
            GROUP BY strftime('%Y-%m', date_vente)
            ORDER BY mois DESC
        """
        results = db.execute_query(query)
        return [dict(row) for row in results]
    
    @staticmethod
    def get_top_selling_products(limit: int = 10) -> List[Dict[str, Any]]:
        """
        NIVEAU 3 - GROUP BY avec ORDER BY et LIMIT
        Récupère les produits les plus vendus
        
        Args:
            limit: Nombre de produits à récupérer
        
        Returns:
            Liste de dictionnaires avec les produits les plus vendus
        """
        query = """
            SELECT 
                p.produit_id,
                p.nom as nom_produit,
                p.categorie,
                SUM(v.quantite) as quantite_vendue,
                COUNT(v.vente_id) as nombre_transactions,
                SUM(v.montant_total) as chiffre_affaires
            FROM Produits p
            INNER JOIN Ventes v ON p.produit_id = v.produit_id
            GROUP BY p.produit_id, p.nom, p.categorie
            ORDER BY quantite_vendue DESC
            LIMIT ?
        """
        results = db.execute_query(query, (limit,))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_best_customers(limit: int = 10) -> List[Dict[str, Any]]:
        """
        NIVEAU 3 - GROUP BY avec ORDER BY et LIMIT
        Récupère les meilleurs clients
        
        Args:
            limit: Nombre de clients à récupérer
        
        Returns:
            Liste de dictionnaires avec les meilleurs clients
        """
        query = """
            SELECT 
                c.client_id,
                c.nom || ' ' || c.prenom as nom_client,
                c.email,
                c.ville,
                COUNT(v.vente_id) as nombre_achats,
                SUM(v.montant_total) as montant_total
            FROM Clients c
            INNER JOIN Ventes v ON c.client_id = v.client_id
            GROUP BY c.client_id, c.nom, c.prenom, c.email, c.ville
            ORDER BY montant_total DESC
            LIMIT ?
        """
        results = db.execute_query(query, (limit,))
        return [dict(row) for row in results]
