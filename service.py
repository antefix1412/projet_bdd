"""
Service métier pour les opérations et analyses
Contient la logique métier et les requêtes SQL
"""

import database


# ============================================================================
# NIVEAU 1 - Requêtes simples (SELECT avec WHERE)
# ============================================================================

def get_client_by_id(client_id):
    """Récupère un client par son ID"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    # Requête paramétrée avec WHERE
    cursor.execute(
        "SELECT * FROM Clients WHERE client_id = ?",
        (client_id,)
    )
    
    result = cursor.fetchone()
    conn.close()
    return dict(result) if result else None


def get_produit_by_id(produit_id):
    """Récupère un produit par son ID"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    # Requête paramétrée avec WHERE
    cursor.execute(
        "SELECT * FROM Produits WHERE produit_id = ?",
        (produit_id,)
    )
    
    result = cursor.fetchone()
    conn.close()
    return dict(result) if result else None


def get_produits_by_categorie(categorie):
    """Récupère tous les produits d'une catégorie"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    # Requête paramétrée avec WHERE
    cursor.execute(
        "SELECT * FROM Produits WHERE categorie = ? ORDER BY nom",
        (categorie,)
    )
    
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]


# ============================================================================
# NIVEAU 2 - Requêtes intermédiaires (JOINTURES + AGRÉGATS)
# ============================================================================

def get_all_ventes():
    """Récupère toutes les ventes avec détails client et produit (JOINTURE)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    # Jointure entre 3 tables
    cursor.execute("""
        SELECT 
            v.vente_id,
            v.date_vente,
            v.quantite,
            v.montant_total,
            c.nom || ' ' || c.prenom as nom_client,
            c.ville,
            p.nom as nom_produit,
            p.categorie
        FROM Ventes v
        INNER JOIN Clients c ON v.client_id = c.client_id
        INNER JOIN Produits p ON v.produit_id = p.produit_id
        ORDER BY v.date_vente DESC
    """)
    
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]


def get_chiffre_affaires_total():
    """Calcule le chiffre d'affaires total (AGRÉGAT SUM)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(montant_total) as total FROM Ventes")
    
    result = cursor.fetchone()
    conn.close()
    return result['total'] if result['total'] else 0


def get_quantite_totale_vendue():
    """Calcule la quantité totale vendue (AGRÉGAT SUM)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(quantite) as total FROM Ventes")
    
    result = cursor.fetchone()
    conn.close()
    return result['total'] if result['total'] else 0


def get_nombre_ventes():
    """Compte le nombre total de ventes (AGRÉGAT COUNT)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM Ventes")
    
    result = cursor.fetchone()
    conn.close()
    return result['total']


def get_montant_moyen_vente():
    """Calcule le montant moyen d'une vente (AGRÉGAT AVG)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT AVG(montant_total) as moyenne FROM Ventes")
    
    result = cursor.fetchone()
    conn.close()
    return result['moyenne'] if result['moyenne'] else 0


# ============================================================================
# NIVEAU 3 - Requêtes avancées (GROUP BY + indicateurs métier)
# ============================================================================

def get_classement_produits():
    """Classement des produits par chiffre d'affaires (GROUP BY + ORDER BY)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
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
    """)
    
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]


def get_ca_par_categorie():
    """Chiffre d'affaires par catégorie (GROUP BY)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
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
    """)
    
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]


def get_meilleurs_clients():
    """Classement des meilleurs clients (GROUP BY + ORDER BY)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            c.nom || ' ' || c.prenom as client,
            c.ville,
            COUNT(v.vente_id) as nombre_achats,
            SUM(v.montant_total) as montant_total,
            AVG(v.montant_total) as panier_moyen
        FROM Clients c
        INNER JOIN Ventes v ON c.client_id = v.client_id
        GROUP BY c.client_id, c.nom, c.prenom, c.ville
        ORDER BY montant_total DESC
    """)
    
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]


def get_ca_par_ville():
    """Chiffre d'affaires par ville (GROUP BY sur jointure)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            c.ville,
            COUNT(DISTINCT c.client_id) as nombre_clients,
            COUNT(v.vente_id) as nombre_ventes,
            SUM(v.montant_total) as chiffre_affaires
        FROM Clients c
        INNER JOIN Ventes v ON c.client_id = v.client_id
        WHERE c.ville IS NOT NULL
        GROUP BY c.ville
        ORDER BY chiffre_affaires DESC
    """)
    
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]


# ============================================================================
# INDICATEURS CALCULÉS CÔTÉ PYTHON (pas seulement SQL)
# ============================================================================

def calculer_taux_conversion_stock():
    """
    Indicateur métier calculé en Python:
    Taux de conversion du stock en ventes pour chaque produit
    """
    conn = database.get_connection()
    cursor = conn.cursor()
    
    # Récupérer les données nécessaires
    cursor.execute("""
        SELECT 
            p.nom as produit,
            p.stock as stock_actuel,
            COALESCE(SUM(v.quantite), 0) as quantite_vendue
        FROM Produits p
        LEFT JOIN Ventes v ON p.produit_id = v.produit_id
        GROUP BY p.produit_id, p.nom, p.stock
    """)
    
    results = cursor.fetchall()
    conn.close()
    
    # Calcul côté Python
    indicateurs = []
    for row in results:
        stock_initial = row['stock_actuel'] + row['quantite_vendue']
        if stock_initial > 0:
            taux_vente = (row['quantite_vendue'] / stock_initial) * 100
        else:
            taux_vente = 0
        
        indicateurs.append({
            'produit': row['produit'],
            'stock_actuel': row['stock_actuel'],
            'quantite_vendue': row['quantite_vendue'],
            'stock_initial': stock_initial,
            'taux_vente_pourcent': round(taux_vente, 2)
        })
    
    # Trier par taux de vente
    return sorted(indicateurs, key=lambda x: x['taux_vente_pourcent'], reverse=True)


def calculer_indice_fidelite_clients():
    """
    Indicateur métier calculé en Python:
    Indice de fidélité basé sur le nombre d'achats et le montant moyen
    """
    conn = database.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            c.nom || ' ' || c.prenom as client,
            COUNT(v.vente_id) as nombre_achats,
            SUM(v.montant_total) as montant_total,
            AVG(v.montant_total) as panier_moyen
        FROM Clients c
        LEFT JOIN Ventes v ON c.client_id = v.client_id
        GROUP BY c.client_id, c.nom, c.prenom
    """)
    
    results = cursor.fetchall()
    conn.close()
    
    # Calcul de l'indice en Python
    # Indice = (nombre d'achats × 10) + (panier_moyen / 10)
    indices = []
    for row in results:
        if row['nombre_achats'] > 0:
            indice = (row['nombre_achats'] * 10) + (row['panier_moyen'] / 10)
            indices.append({
                'client': row['client'],
                'nombre_achats': row['nombre_achats'],
                'montant_total': round(row['montant_total'], 2),
                'panier_moyen': round(row['panier_moyen'], 2),
                'indice_fidelite': round(indice, 2)
            })
    
    return sorted(indices, key=lambda x: x['indice_fidelite'], reverse=True)


# ============================================================================
# FONCTION D'INSERTION (NIVEAU 1 - requêtes paramétrées)
# ============================================================================

def ajouter_vente(client_id, produit_id, quantite):
    """
    Ajoute une nouvelle vente (requête paramétrée INSERT)
    Gestion de transaction avec commit/rollback
    """
    conn = database.get_connection()
    cursor = conn.cursor()
    
    try:
        # Récupérer le produit pour le prix
        cursor.execute(
            "SELECT prix_unitaire, stock FROM Produits WHERE produit_id = ?",
            (produit_id,)
        )
        produit = cursor.fetchone()
        
        if not produit:
            raise ValueError(f"Produit {produit_id} introuvable")
        
        if produit['stock'] < quantite:
            raise ValueError(f"Stock insuffisant. Disponible: {produit['stock']}")
        
        prix_unitaire = produit['prix_unitaire']
        montant_total = quantite * prix_unitaire
        
        # Insérer la vente (requête paramétrée)
        cursor.execute(
            """INSERT INTO Ventes (client_id, produit_id, quantite, prix_unitaire, montant_total)
               VALUES (?, ?, ?, ?, ?)""",
            (client_id, produit_id, quantite, prix_unitaire, montant_total)
        )
        
        # Mettre à jour le stock
        cursor.execute(
            "UPDATE Produits SET stock = stock - ? WHERE produit_id = ?",
            (quantite, produit_id)
        )
        
        conn.commit()
        return {
            'succes': True,
            'message': 'Vente enregistrée avec succès',
            'montant_total': montant_total
        }
        
    except Exception as e:
        conn.rollback()
        return {
            'succes': False,
            'message': f'Erreur: {str(e)}'
        }
    finally:
        conn.close()
