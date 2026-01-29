"""
Service métier pour la gestion des produits
Couche de logique métier entre l'interface et la DAO
"""

from typing import List, Optional, Dict, Any
from src.dao import ProduitDAO


class ProduitService:
    """Service de gestion des produits avec validation métier"""
    
    def __init__(self):
        self.produit_dao = ProduitDAO()
    
    def creer_produit(self, nom: str, prix_unitaire: float, description: str = None,
                      categorie: str = None, stock: int = 0) -> Dict[str, Any]:
        """
        Crée un nouveau produit avec validation
        
        Args:
            nom: Nom du produit
            prix_unitaire: Prix unitaire
            description: Description (optionnel)
            categorie: Catégorie (optionnel)
            stock: Stock initial
        
        Returns:
            Dictionnaire avec succès et message/ID
        
        Raises:
            ValueError: Si les données sont invalides
        """
        # Validation
        if not nom or not nom.strip():
            raise ValueError("Le nom du produit est obligatoire")
        
        if prix_unitaire is None or prix_unitaire <= 0:
            raise ValueError("Le prix unitaire doit être supérieur à 0")
        
        if stock < 0:
            raise ValueError("Le stock ne peut pas être négatif")
        
        # Créer le produit
        produit_id = self.produit_dao.create(
            nom.strip(),
            prix_unitaire,
            description.strip() if description else None,
            categorie.strip().title() if categorie else None,
            stock
        )
        
        return {
            'succes': True,
            'message': 'Produit créé avec succès',
            'produit_id': produit_id
        }
    
    def obtenir_produit(self, produit_id: int) -> Optional[Dict[str, Any]]:
        """
        Récupère un produit par son ID
        
        Args:
            produit_id: ID du produit
        
        Returns:
            Informations du produit ou None
        """
        return self.produit_dao.get_by_id(produit_id)
    
    def obtenir_tous_les_produits(self) -> List[Dict[str, Any]]:
        """
        Récupère tous les produits
        
        Returns:
            Liste des produits
        """
        return self.produit_dao.get_all()
    
    def obtenir_produits_par_categorie(self, categorie: str) -> List[Dict[str, Any]]:
        """
        Récupère les produits d'une catégorie
        
        Args:
            categorie: Nom de la catégorie
        
        Returns:
            Liste des produits de la catégorie
        """
        if not categorie or not categorie.strip():
            return []
        return self.produit_dao.get_by_categorie(categorie.strip().title())
    
    def obtenir_categories(self) -> List[str]:
        """
        Récupère toutes les catégories
        
        Returns:
            Liste des catégories
        """
        return self.produit_dao.get_categories()
    
    def obtenir_produits_en_stock(self) -> List[Dict[str, Any]]:
        """
        Récupère les produits en stock
        
        Returns:
            Liste des produits en stock
        """
        return self.produit_dao.get_in_stock()
    
    def obtenir_produits_en_rupture(self) -> List[Dict[str, Any]]:
        """
        Récupère les produits en rupture de stock
        
        Returns:
            Liste des produits en rupture
        """
        return self.produit_dao.get_out_of_stock()
    
    def rechercher_produits(self, terme: str) -> List[Dict[str, Any]]:
        """
        Recherche des produits
        
        Args:
            terme: Terme de recherche
        
        Returns:
            Liste des produits trouvés
        """
        if not terme or not terme.strip():
            return []
        return self.produit_dao.search(terme.strip())
    
    def modifier_produit(self, produit_id: int, **kwargs) -> Dict[str, Any]:
        """
        Modifie les informations d'un produit
        
        Args:
            produit_id: ID du produit
            **kwargs: Champs à modifier
        
        Returns:
            Dictionnaire avec succès et message
        
        Raises:
            ValueError: Si les données sont invalides
        """
        # Vérifier que le produit existe
        produit = self.produit_dao.get_by_id(produit_id)
        if not produit:
            raise ValueError(f"Produit avec l'ID {produit_id} introuvable")
        
        # Valider les données
        if 'prix_unitaire' in kwargs:
            if kwargs['prix_unitaire'] is None or kwargs['prix_unitaire'] <= 0:
                raise ValueError("Le prix unitaire doit être supérieur à 0")
        
        if 'stock' in kwargs:
            if kwargs['stock'] < 0:
                raise ValueError("Le stock ne peut pas être négatif")
        
        # Normaliser les données
        if 'nom' in kwargs and kwargs['nom']:
            kwargs['nom'] = kwargs['nom'].strip()
        
        if 'description' in kwargs and kwargs['description']:
            kwargs['description'] = kwargs['description'].strip()
        
        if 'categorie' in kwargs and kwargs['categorie']:
            kwargs['categorie'] = kwargs['categorie'].strip().title()
        
        # Modifier le produit
        rows_affected = self.produit_dao.update(produit_id, **kwargs)
        
        if rows_affected > 0:
            return {
                'succes': True,
                'message': 'Produit modifié avec succès'
            }
        else:
            return {
                'succes': False,
                'message': 'Aucune modification effectuée'
            }
    
    def modifier_stock(self, produit_id: int, nouvelle_quantite: int) -> Dict[str, Any]:
        """
        Modifie le stock d'un produit
        
        Args:
            produit_id: ID du produit
            nouvelle_quantite: Nouvelle quantité en stock
        
        Returns:
            Dictionnaire avec succès et message
        
        Raises:
            ValueError: Si les données sont invalides
        """
        if nouvelle_quantite < 0:
            raise ValueError("Le stock ne peut pas être négatif")
        
        # Vérifier que le produit existe
        produit = self.produit_dao.get_by_id(produit_id)
        if not produit:
            raise ValueError(f"Produit avec l'ID {produit_id} introuvable")
        
        rows_affected = self.produit_dao.update_stock(produit_id, nouvelle_quantite)
        
        if rows_affected > 0:
            return {
                'succes': True,
                'message': f'Stock mis à jour: {nouvelle_quantite} unités'
            }
        else:
            return {
                'succes': False,
                'message': 'Échec de la mise à jour du stock'
            }
    
    def ajouter_stock(self, produit_id: int, quantite: int) -> Dict[str, Any]:
        """
        Ajoute du stock à un produit
        
        Args:
            produit_id: ID du produit
            quantite: Quantité à ajouter
        
        Returns:
            Dictionnaire avec succès et message
        
        Raises:
            ValueError: Si les données sont invalides
        """
        if quantite <= 0:
            raise ValueError("La quantité à ajouter doit être supérieure à 0")
        
        # Vérifier que le produit existe
        produit = self.produit_dao.get_by_id(produit_id)
        if not produit:
            raise ValueError(f"Produit avec l'ID {produit_id} introuvable")
        
        rows_affected = self.produit_dao.increase_stock(produit_id, quantite)
        nouveau_stock = produit['stock'] + quantite
        
        if rows_affected > 0:
            return {
                'succes': True,
                'message': f'Stock augmenté de {quantite} unités. Nouveau stock: {nouveau_stock}'
            }
        else:
            return {
                'succes': False,
                'message': 'Échec de l\'ajout au stock'
            }
    
    def retirer_stock(self, produit_id: int, quantite: int) -> Dict[str, Any]:
        """
        Retire du stock d'un produit
        
        Args:
            produit_id: ID du produit
            quantite: Quantité à retirer
        
        Returns:
            Dictionnaire avec succès et message
        
        Raises:
            ValueError: Si les données sont invalides ou stock insuffisant
        """
        if quantite <= 0:
            raise ValueError("La quantité à retirer doit être supérieure à 0")
        
        # Vérifier que le produit existe
        produit = self.produit_dao.get_by_id(produit_id)
        if not produit:
            raise ValueError(f"Produit avec l'ID {produit_id} introuvable")
        
        # Vérifier que le stock est suffisant
        if produit['stock'] < quantite:
            raise ValueError(f"Stock insuffisant. Disponible: {produit['stock']}, Demandé: {quantite}")
        
        rows_affected = self.produit_dao.decrease_stock(produit_id, quantite)
        nouveau_stock = produit['stock'] - quantite
        
        if rows_affected > 0:
            return {
                'succes': True,
                'message': f'Stock diminué de {quantite} unités. Nouveau stock: {nouveau_stock}'
            }
        else:
            return {
                'succes': False,
                'message': 'Échec de la diminution du stock'
            }
    
    def supprimer_produit(self, produit_id: int) -> Dict[str, Any]:
        """
        Supprime un produit
        
        Args:
            produit_id: ID du produit
        
        Returns:
            Dictionnaire avec succès et message
        
        Raises:
            ValueError: Si le produit a des ventes associées
        """
        # Vérifier que le produit existe
        produit = self.produit_dao.get_by_id(produit_id)
        if not produit:
            raise ValueError(f"Produit avec l'ID {produit_id} introuvable")
        
        try:
            rows_affected = self.produit_dao.delete(produit_id)
            
            if rows_affected > 0:
                return {
                    'succes': True,
                    'message': 'Produit supprimé avec succès'
                }
            else:
                return {
                    'succes': False,
                    'message': 'Échec de la suppression'
                }
        except Exception as e:
            raise ValueError("Impossible de supprimer ce produit car il a des ventes associées")
    
    def obtenir_statistiques_produits(self) -> List[Dict[str, Any]]:
        """
        Récupère les statistiques des produits avec leurs ventes
        
        Returns:
            Liste des produits avec statistiques
        """
        return self.produit_dao.get_products_with_sales()
    
    def compter_produits(self) -> int:
        """
        Compte le nombre total de produits
        
        Returns:
            Nombre de produits
        """
        return self.produit_dao.count()
    
    def obtenir_prix_moyen(self) -> float:
        """
        Calcule le prix moyen des produits
        
        Returns:
            Prix moyen
        """
        return self.produit_dao.get_average_price()
