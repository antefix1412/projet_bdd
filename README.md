# Projet de Synthèse - Application d'Analyse de Ventes

## Description
Application locale de gestion et d'analyse de ventes utilisant SQLite et Python.
Projet réalisé dans le cadre du cours de Base de Données.

## Structure du Projet
```
projet_final/
├── database.py      # Connexion BDD et création du schéma
├── service.py       # Requêtes SQL et logique métier
├── ui.py            # Interface utilisateur (menu)
└── ventes.db        # Base de données SQLite (générée)
```

## Installation et Utilisation

### Initialiser la base de données
```bash
python database.py
```

### Lancer l'application
```bash
python ui.py
```

## Modèle de Données

### Entités

**Clients**
- client_id (PK)
- nom, prenom, email (UNIQUE), ville

**Produits**
- produit_id (PK)
- nom, prix_unitaire, categorie, stock

**Ventes**
- vente_id (PK)
- client_id (FK), produit_id (FK)
- quantite, prix_unitaire, montant_total, date_vente

### Relations
- Une vente concerne **un client** et **un produit**
- Clés étrangères pour assurer l'intégrité référentielle

## Requêtes SQL Implémentées

### Niveau 1 - Requêtes simples
✓ Insertions avec requêtes paramétrées (sécurisées)
✓ SELECT avec WHERE
✓ Gestion des transactions (commit/rollback)

### Niveau 2 - Requêtes intermédiaires
✓ JOINTURES entre 2 et 3 tables
✓ Agrégats: SUM, COUNT, AVG
✓ LEFT JOIN pour inclure les données nulles

### Niveau 3 - Requêtes avancées
✓ GROUP BY avec plusieurs colonnes
✓ HAVING pour filtrer les groupes
✓ ORDER BY pour classements
✓ Requêtes complexes multi-conditions

## Analyses Métier Disponibles

### Analyses SQL
1. **Chiffre d'affaires total** - SUM(montant_total)
2. **Quantité totale vendue** - SUM(quantite)
3. **Classement des produits** - GROUP BY + ORDER BY
4. **CA par catégorie** - GROUP BY categorie
5. **CA par ville** - GROUP BY ville avec jointure
6. **Meilleurs clients** - GROUP BY client avec agrégats

### Indicateurs calculés en Python
7. **Taux de vente des produits** - % de stock vendu (calcul Python)
8. **Indice de fidélité clients** - Score basé sur achats et panier moyen (calcul Python)

## Fonctionnalités

- ✅ Consultation des ventes avec détails complets
- ✅ Analyses statistiques multiples
- ✅ Ajout de nouvelles ventes avec validation
- ✅ Gestion automatique du stock
- ✅ Requêtes paramétrées (sécurité SQL)
- ✅ Transactions avec rollback en cas d'erreur

## Choix Techniques

### Base de données
- **SQLite** : Simple, portable, sans serveur
- **Schéma normalisé** : 3 tables avec relations claires
- **Contraintes** : CHECK, UNIQUE, NOT NULL, FK
- **Index implicites** : sur les clés primaires

### Architecture Python
- **3 fichiers séparés** : database / service / ui
- **Séparation des responsabilités** :
  - `database.py` : Connexion et schéma
  - `service.py` : Requêtes SQL et logique métier
  - `ui.py` : Interface utilisateur

### Sécurité
- **Requêtes paramétrées** : Protection contre l'injection SQL
- **Transactions** : Cohérence des données (commit/rollback)
- **Validation** : Contrôles métier avant insertion

### Python
- **Simplicité** : Code clair et lisible
- **Commentaires** : Chaque requête est documentée
- **Gestion d'erreurs** : try/except avec rollback

## Exemples de Requêtes

### Jointure avec agrégats
```sql
SELECT 
    p.nom as produit,
    COUNT(v.vente_id) as nombre_ventes,
    SUM(v.quantite) as quantite_vendue,
    SUM(v.montant_total) as chiffre_affaires
FROM Produits p
LEFT JOIN Ventes v ON p.produit_id = v.produit_id
GROUP BY p.produit_id, p.nom
ORDER BY chiffre_affaires DESC
```

### Requête paramétrée (sécurisée)
```python
cursor.execute(
    "SELECT * FROM Clients WHERE client_id = ?",
    (client_id,)
)
```

## Auteur
Projet réalisé dans le cadre du cours de Base de Données - B2
