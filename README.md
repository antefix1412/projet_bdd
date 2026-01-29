# Projet de Synthèse - Application d'Analyse Métier

## Description
Application locale d'analyse de ventes utilisant SQLite et Python.

## Structure du Projet
```
projet_final/
│
├── database/
│   ├── schema.sql              # Schéma de la base de données
│   └── ventes.db               # Base de données SQLite (générée)
│
├── src/
│   ├── dao/
│   │   ├── __init__.py
│   │   ├── database.py         # Connexion à la base
│   │   ├── client_dao.py       # Accès données clients
│   │   ├── produit_dao.py      # Accès données produits
│   │   └── vente_dao.py        # Accès données ventes
│   │
│   ├── business/
│   │   ├── __init__.py
│   │   ├── client_service.py   # Logique métier clients
│   │   ├── produit_service.py  # Logique métier produits
│   │   └── vente_service.py    # Logique métier ventes
│   │
│   └── ui/
│       ├── __init__.py
│       └── cli.py              # Interface en ligne de commande
│
├── scripts/
│   ├── init_database.py        # Initialisation de la BDD
│   ├── populate_data.py        # Insertion de données de test
│   └── analytics.py            # Scripts d'analyse
│
├── requirements.txt            # Dépendances Python
└── main.py                     # Point d'entrée de l'application
```

## Fonctionnalités

### 1. Gestion des Clients
- Ajout de nouveaux clients
- Consultation des clients existants
- Mise à jour des informations

### 2. Gestion des Produits
- Ajout de produits au catalogue
- Consultation du catalogue
- Mise à jour des prix

### 3. Gestion des Ventes
- Enregistrement automatique de ventes
- Consultation de l'historique
- Filtrage par date, client ou produit

### 4. Analyses Métier
- Chiffre d'affaires total et par période
- Produits les plus vendus
- Meilleurs clients
- Évolution des ventes

## Installation

```bash
# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données
python scripts/init_database.py

# Peupler avec des données de test
python scripts/populate_data.py
```

## Utilisation

```bash
# Lancer l'application interactive
python main.py

# Exécuter les analyses
python scripts/analytics.py
```

## Modèle de Données

### Entités principales
1. **Clients** : Informations sur les clients
2. **Produits** : Catalogue de produits
3. **Ventes** : Transactions de vente

### Relations
- Une vente concerne un client et un produit
- Clés étrangères pour assurer l'intégrité référentielle

## Niveaux de Requêtes SQL

### Niveau 1 - Simple
- INSERT, SELECT avec WHERE

### Niveau 2 - Intermédiaire  
- JOIN entre tables
- Agrégats (SUM, COUNT, AVG)

### Niveau 3 - Avancé
- GROUP BY avec HAVING
- Sous-requêtes
- Requêtes complexes multi-conditions

## Auteur
Projet réalisé dans le cadre du cours de Base de Données
