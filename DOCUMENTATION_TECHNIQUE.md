# Document Technique - Choix et Justifications

## 1. Modélisation de la Base de Données

### Choix du modèle relationnel
Nous avons opté pour un modèle simple à 3 tables :
- **Clients** : Informations sur les acheteurs
- **Produits** : Catalogue des articles
- **Ventes** : Transactions (table de jonction enrichie)

### Justification
- ✓ Évite la redondance (normalisation)
- ✓ Relations claires avec clés étrangères
- ✓ Facilite les jointures et analyses
- ✓ Extensible pour évolutions futures

### Contraintes implémentées
```sql
-- Clés primaires : auto-incrémentées
client_id INTEGER PRIMARY KEY AUTOINCREMENT

-- Contraintes CHECK : validation des données
prix_unitaire REAL NOT NULL CHECK(prix_unitaire > 0)
stock INTEGER DEFAULT 0 CHECK(stock >= 0)

-- Contraintes UNIQUE : unicité de l'email
email TEXT UNIQUE NOT NULL

-- Clés étrangères : intégrité référentielle
FOREIGN KEY (client_id) REFERENCES Clients(client_id)
```

## 2. Choix SQL

### Niveaux de requêtes couverts

**Niveau 1 - Simple (4 points)**
- INSERT avec requêtes paramétrées
- SELECT avec WHERE
- Validation : tous les inserts utilisent `?` pour la sécurité

**Niveau 2 - Intermédiaire (4 points)**
- INNER JOIN et LEFT JOIN entre 2-3 tables
- Agrégats : SUM(), COUNT(), AVG()
- Exemple : `get_all_ventes()` joint 3 tables

**Niveau 3 - Avancé (4 points)**
- GROUP BY avec plusieurs colonnes
- HAVING pour filtrer les agrégats
- ORDER BY pour classements
- Exemple : `get_classement_produits()`

### Requête complexe représentative
```sql
SELECT 
    p.nom as produit,
    p.categorie,
    COUNT(v.vente_id) as nombre_ventes,
    SUM(v.quantite) as quantite_vendue,
    SUM(v.montant_total) as chiffre_affaires
FROM Produits p
LEFT JOIN Ventes v ON p.produit_id = v.produit_id
GROUP BY p.produit_id, p.nom, p.categorie
HAVING COUNT(v.vente_id) > 0
ORDER BY chiffre_affaires DESC
```

**Points techniques :**
- LEFT JOIN pour inclure produits sans ventes
- GROUP BY sur 3 colonnes
- HAVING pour exclure produits non vendus
- 4 agrégats différents (COUNT, SUM × 2)
- ORDER BY sur résultat calculé

## 3. Backend Python

### Architecture choisie

```
database.py  →  service.py  →  ui.py
  (BDD)      (Logique métier)  (Interface)
```

**Séparation des responsabilités :**
- `database.py` : Connexion, création schéma, données de test
- `service.py` : Toutes les requêtes SQL et calculs métier
- `ui.py` : Interface utilisateur uniquement

### Justification
- ✓ Code organisé et lisible
- ✓ Facile à maintenir
- ✓ Testable indépendamment
- ✓ Respecte le principe de responsabilité unique

### Gestion de la connexion
```python
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Accès par nom de colonne
    conn.execute("PRAGMA foreign_keys = ON")  # Activer FK
    return conn
```

**Choix :**
- `row_factory = sqlite3.Row` : permet `row['nom']` au lieu de `row[0]`
- PRAGMA foreign_keys : active la validation des clés étrangères

### Sécurité - Requêtes paramétrées
```python
# ✅ BON - Requête paramétrée (sécurisé)
cursor.execute(
    "SELECT * FROM Clients WHERE client_id = ?",
    (client_id,)
)

# ❌ MAUVAIS - Concaténation (injection SQL possible)
cursor.execute(f"SELECT * FROM Clients WHERE client_id = {client_id}")
```

**Toutes nos requêtes utilisent des paramètres (`?`) pour éviter l'injection SQL.**

### Gestion des transactions
```python
try:
    # Opérations multiples
    cursor.execute("INSERT INTO Ventes ...")
    cursor.execute("UPDATE Produits SET stock = ...")
    
    conn.commit()  # Valider si tout OK
    return {'succes': True}
    
except Exception as e:
    conn.rollback()  # Annuler si erreur
    return {'succes': False, 'message': str(e)}
```

**Principe :** Tout ou rien - si une erreur survient, on annule tout.

## 4. Analyses Métier

### Indicateurs SQL (7 analyses)
1. **CA total** - `SUM(montant_total)`
2. **Quantité totale** - `SUM(quantite)`
3. **Nombre de ventes** - `COUNT(*)`
4. **Montant moyen** - `AVG(montant_total)`
5. **Classement produits** - `GROUP BY` + `ORDER BY`
6. **CA par catégorie** - `GROUP BY categorie`
7. **Meilleurs clients** - `GROUP BY client_id`

### Indicateurs calculés en Python (2 analyses)

**1. Taux de vente des produits**
```python
stock_initial = stock_actuel + quantite_vendue
taux_vente = (quantite_vendue / stock_initial) * 100
```
Permet de voir quels produits se vendent le mieux proportionnellement.

**2. Indice de fidélité clients**
```python
indice = (nombre_achats × 10) + (panier_moyen / 10)
```
Combine fréquence d'achat et valeur moyenne pour identifier les meilleurs clients.

**Justification du calcul en Python :**
- Formules personnalisées métier
- Plusieurs étapes de calcul
- Plus lisible en Python qu'en SQL complexe

## 5. Points Forts du Projet

### Niveau SQL
✓ 3 niveaux de requêtes maîtrisés
✓ Jointures complexes (jusqu'à 3 tables)
✓ Agrégats multiples avec GROUP BY
✓ HAVING pour filtrage avancé

### Niveau Python
✓ Requêtes 100% paramétrées (sécurité)
✓ Transactions avec commit/rollback
✓ Architecture claire (3 fichiers séparés)
✓ Gestion des erreurs complète

### Niveau Fonctionnel
✓ 9 analyses différentes
✓ Interface utilisateur complète
✓ Données de test pertinentes
✓ Documentation complète

## 6. Complexité Maîtrisée

Le projet reste **accessible à un junior (7-8h de travail)** tout en démontrant :
- Maîtrise des concepts SQL (3 niveaux)
- Bonne pratique Python (séparation, sécurité)
- Analyses métier pertinentes
- Code propre et documenté

**Temps estimé par partie :**
- Modélisation et schéma : 1h
- Requêtes SQL simples : 1h
- Requêtes SQL avancées : 2h
- Backend Python : 2h
- Interface UI : 1h
- Tests et documentation : 1h
**Total : ~8h**

## Conclusion

Ce projet démontre :
1. ✅ Modèle cohérent avec clés et relations
2. ✅ Requêtes SQL des 3 niveaux
3. ✅ Backend Python sécurisé
4. ✅ Logique métier claire
5. ✅ Analyses exploitables

Architecture **simple mais complète**, idéale pour un projet de synthèse de cours de Base de Données.
