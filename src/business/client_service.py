"""
Service métier pour la gestion des clients
Couche de logique métier entre l'interface et la DAO
"""

from typing import List, Optional, Dict, Any
from src.dao import ClientDAO


class ClientService:
    """Service de gestion des clients avec validation métier"""
    
    def __init__(self):
        self.client_dao = ClientDAO()
    
    def creer_client(self, nom: str, prenom: str, email: str, 
                     telephone: str = None, ville: str = None) -> Dict[str, Any]:
        """
        Crée un nouveau client avec validation
        
        Args:
            nom: Nom du client
            prenom: Prénom du client
            email: Email du client
            telephone: Téléphone (optionnel)
            ville: Ville (optionnel)
        
        Returns:
            Dictionnaire avec succès et message/ID
        
        Raises:
            ValueError: Si les données sont invalides
        """
        # Validation
        if not nom or not nom.strip():
            raise ValueError("Le nom est obligatoire")
        
        if not prenom or not prenom.strip():
            raise ValueError("Le prénom est obligatoire")
        
        if not email or not email.strip():
            raise ValueError("L'email est obligatoire")
        
        if not self._valider_email(email):
            raise ValueError("Format d'email invalide")
        
        # Vérifier si l'email existe déjà
        client_existant = self.client_dao.get_by_email(email)
        if client_existant:
            raise ValueError(f"Un client avec l'email {email} existe déjà")
        
        # Créer le client
        client_id = self.client_dao.create(
            nom.strip().title(),
            prenom.strip().title(),
            email.strip().lower(),
            telephone.strip() if telephone else None,
            ville.strip().title() if ville else None
        )
        
        return {
            'succes': True,
            'message': 'Client créé avec succès',
            'client_id': client_id
        }
    
    def obtenir_client(self, client_id: int) -> Optional[Dict[str, Any]]:
        """
        Récupère un client par son ID
        
        Args:
            client_id: ID du client
        
        Returns:
            Informations du client ou None
        """
        return self.client_dao.get_by_id(client_id)
    
    def obtenir_tous_les_clients(self) -> List[Dict[str, Any]]:
        """
        Récupère tous les clients
        
        Returns:
            Liste des clients
        """
        return self.client_dao.get_all()
    
    def rechercher_clients(self, terme: str) -> List[Dict[str, Any]]:
        """
        Recherche des clients
        
        Args:
            terme: Terme de recherche
        
        Returns:
            Liste des clients trouvés
        """
        if not terme or not terme.strip():
            return []
        return self.client_dao.search(terme.strip())
    
    def obtenir_clients_par_ville(self, ville: str) -> List[Dict[str, Any]]:
        """
        Récupère les clients d'une ville
        
        Args:
            ville: Nom de la ville
        
        Returns:
            Liste des clients de la ville
        """
        if not ville or not ville.strip():
            return []
        return self.client_dao.get_by_ville(ville.strip().title())
    
    def modifier_client(self, client_id: int, **kwargs) -> Dict[str, Any]:
        """
        Modifie les informations d'un client
        
        Args:
            client_id: ID du client
            **kwargs: Champs à modifier (nom, prenom, email, telephone, ville)
        
        Returns:
            Dictionnaire avec succès et message
        
        Raises:
            ValueError: Si les données sont invalides
        """
        # Vérifier que le client existe
        client = self.client_dao.get_by_id(client_id)
        if not client:
            raise ValueError(f"Client avec l'ID {client_id} introuvable")
        
        # Valider l'email si fourni
        if 'email' in kwargs and kwargs['email']:
            if not self._valider_email(kwargs['email']):
                raise ValueError("Format d'email invalide")
            
            # Vérifier que l'email n'est pas déjà utilisé par un autre client
            client_existant = self.client_dao.get_by_email(kwargs['email'])
            if client_existant and client_existant['client_id'] != client_id:
                raise ValueError(f"L'email {kwargs['email']} est déjà utilisé")
            
            kwargs['email'] = kwargs['email'].strip().lower()
        
        # Normaliser les données
        if 'nom' in kwargs and kwargs['nom']:
            kwargs['nom'] = kwargs['nom'].strip().title()
        
        if 'prenom' in kwargs and kwargs['prenom']:
            kwargs['prenom'] = kwargs['prenom'].strip().title()
        
        if 'ville' in kwargs and kwargs['ville']:
            kwargs['ville'] = kwargs['ville'].strip().title()
        
        if 'telephone' in kwargs and kwargs['telephone']:
            kwargs['telephone'] = kwargs['telephone'].strip()
        
        # Modifier le client
        rows_affected = self.client_dao.update(client_id, **kwargs)
        
        if rows_affected > 0:
            return {
                'succes': True,
                'message': 'Client modifié avec succès'
            }
        else:
            return {
                'succes': False,
                'message': 'Aucune modification effectuée'
            }
    
    def supprimer_client(self, client_id: int) -> Dict[str, Any]:
        """
        Supprime un client
        
        Args:
            client_id: ID du client
        
        Returns:
            Dictionnaire avec succès et message
        
        Raises:
            ValueError: Si le client a des ventes associées
        """
        # Vérifier que le client existe
        client = self.client_dao.get_by_id(client_id)
        if not client:
            raise ValueError(f"Client avec l'ID {client_id} introuvable")
        
        try:
            rows_affected = self.client_dao.delete(client_id)
            
            if rows_affected > 0:
                return {
                    'succes': True,
                    'message': 'Client supprimé avec succès'
                }
            else:
                return {
                    'succes': False,
                    'message': 'Échec de la suppression'
                }
        except Exception as e:
            raise ValueError("Impossible de supprimer ce client car il a des ventes associées")
    
    def obtenir_statistiques_clients(self) -> List[Dict[str, Any]]:
        """
        Récupère les statistiques des clients avec leurs achats
        
        Returns:
            Liste des clients avec statistiques
        """
        return self.client_dao.get_clients_with_purchases()
    
    def compter_clients(self) -> int:
        """
        Compte le nombre total de clients
        
        Returns:
            Nombre de clients
        """
        return self.client_dao.count()
    
    @staticmethod
    def _valider_email(email: str) -> bool:
        """
        Valide le format d'un email (validation simple)
        
        Args:
            email: Email à valider
        
        Returns:
            True si valide, False sinon
        """
        if not email or '@' not in email:
            return False
        
        parties = email.split('@')
        if len(parties) != 2:
            return False
        
        local, domaine = parties
        if not local or not domaine:
            return False
        
        if '.' not in domaine:
            return False
        
        return True
