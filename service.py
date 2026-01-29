"""
Module service - Requêtes SQL et logique métier
Gestion de réservations d'espaces
"""

import database


# ============================================================================
# NIVEAU 1 - SELECT, INSERT, WHERE
# ============================================================================

def get_all_reservations():
    """Récupère toutes les réservations avec détails (JOIN)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            r.reservation_id,
            r.date_reservation,
            r.heure_debut,
            r.duree_heures,
            r.statut,
            r.montant_total,
            c.nom || ' ' || c.prenom AS client,
            e.nom AS espace,
            e.type AS type_espace
        FROM Reservations r
        INNER JOIN Clients c ON r.client_id = c.client_id
        INNER JOIN Espaces e ON r.espace_id = e.espace_id
        ORDER BY r.date_reservation DESC, r.heure_debut
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]


def get_espaces_disponibles(type_espace=None):
    """Liste des espaces avec filtre optionnel par type"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    if type_espace:
        query = """
            SELECT espace_id, nom, type, capacite, tarif_horaire
            FROM Espaces
            WHERE type = ?
            ORDER BY nom
        """
        cursor.execute(query, (type_espace,))
    else:
        query = """
            SELECT espace_id, nom, type, capacite, tarif_horaire
            FROM Espaces
            ORDER BY type, nom
        """
        cursor.execute(query)
    
    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]


def ajouter_reservation(client_id, espace_id, date_reservation, heure_debut, duree_heures):
    """Ajoute une nouvelle réservation (INSERT avec calcul de montant)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    try:
        # Récupérer le tarif horaire de l'espace
        cursor.execute("SELECT tarif_horaire, nom FROM Espaces WHERE espace_id = ?", (espace_id,))
        espace = cursor.fetchone()
        
        if not espace:
            return {'succes': False, 'message': "Espace introuvable"}
        
        # Calculer le montant total
        montant_total = espace['tarif_horaire'] * duree_heures
        
        # Insérer la réservation
        query = """
            INSERT INTO Reservations 
            (client_id, espace_id, date_reservation, heure_debut, duree_heures, statut, montant_total)
            VALUES (?, ?, ?, ?, ?, 'Confirmée', ?)
        """
        
        cursor.execute(query, (client_id, espace_id, date_reservation, heure_debut, duree_heures, montant_total))
        conn.commit()
        
        return {
            'succes': True,
            'message': f"Réservation créée pour {espace['nom']}",
            'montant_total': montant_total,
            'reservation_id': cursor.lastrowid
        }
        
    except Exception as e:
        conn.rollback()
        return {'succes': False, 'message': str(e)}
    finally:
        conn.close()


# ============================================================================
# NIVEAU 2 - JOIN, Agrégats (COUNT, SUM, AVG)
# ============================================================================

def get_chiffre_affaires_total():
    """Calcule le chiffre d'affaires total (SUM)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT COALESCE(SUM(montant_total), 0) AS ca_total
        FROM Reservations
        WHERE statut != 'Annulée'
    """
    
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    
    return result['ca_total']


def get_nombre_reservations():
    """Compte le nombre total de réservations (COUNT)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT COUNT(*) AS total
        FROM Reservations
        WHERE statut != 'Annulée'
    """
    
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    
    return result['total']


def get_duree_moyenne_reservations():
    """Calcule la durée moyenne des réservations (AVG)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT AVG(duree_heures) AS duree_moyenne
        FROM Reservations
        WHERE statut != 'Annulée'
    """
    
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    
    return result['duree_moyenne'] or 0


def get_statistiques_globales():
    """Retourne toutes les statistiques en une seule requête"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            COUNT(*) AS nombre_reservations,
            SUM(montant_total) AS ca_total,
            AVG(montant_total) AS montant_moyen,
            SUM(duree_heures) AS heures_totales,
            AVG(duree_heures) AS duree_moyenne
        FROM Reservations
        WHERE statut != 'Annulée'
    """
    
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    
    return dict(result)


# ============================================================================
# NIVEAU 3 - GROUP BY, HAVING, Sous-requêtes
# ============================================================================

def get_espaces_les_plus_demandes():
    """Classement des espaces par nombre de réservations (GROUP BY + ORDER BY)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            e.nom AS espace,
            e.type,
            e.capacite,
            COUNT(r.reservation_id) AS nombre_reservations,
            SUM(r.duree_heures) AS heures_totales,
            SUM(r.montant_total) AS ca_total,
            AVG(r.montant_total) AS montant_moyen
        FROM Espaces e
        LEFT JOIN Reservations r ON e.espace_id = r.espace_id AND r.statut != 'Annulée'
        GROUP BY e.espace_id, e.nom, e.type, e.capacite
        ORDER BY nombre_reservations DESC, ca_total DESC
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]


def get_reservations_par_periode(annee=2026, mois=1):
    """Volume de réservations par jour sur une période (GROUP BY date)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            date_reservation,
            COUNT(*) AS nombre_reservations,
            SUM(duree_heures) AS heures_reservees,
            SUM(montant_total) AS ca_jour
        FROM Reservations
        WHERE strftime('%Y', date_reservation) = ? 
          AND strftime('%m', date_reservation) = ?
          AND statut != 'Annulée'
        GROUP BY date_reservation
        ORDER BY date_reservation
    """
    
    cursor.execute(query, (str(annee), f"{mois:02d}"))
    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]


def get_ca_par_type_espace():
    """Chiffre d'affaires par type d'espace (GROUP BY type)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            e.type,
            COUNT(r.reservation_id) AS nombre_reservations,
            SUM(r.duree_heures) AS heures_totales,
            SUM(r.montant_total) AS ca_total,
            AVG(r.montant_total) AS montant_moyen
        FROM Espaces e
        LEFT JOIN Reservations r ON e.espace_id = r.espace_id AND r.statut != 'Annulée'
        GROUP BY e.type
        ORDER BY ca_total DESC
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]


def get_meilleurs_clients():
    """Classement des clients par volume de réservations (GROUP BY + HAVING)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            c.nom || ' ' || c.prenom AS client,
            c.entreprise,
            COUNT(r.reservation_id) AS nombre_reservations,
            SUM(r.montant_total) AS montant_total,
            AVG(r.montant_total) AS montant_moyen,
            SUM(r.duree_heures) AS heures_totales
        FROM Clients c
        INNER JOIN Reservations r ON c.client_id = r.client_id
        WHERE r.statut != 'Annulée'
        GROUP BY c.client_id, c.nom, c.prenom, c.entreprise
        HAVING COUNT(r.reservation_id) > 0
        ORDER BY nombre_reservations DESC, montant_total DESC
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]


# ============================================================================
# CALCULS PYTHON (non SQL)
# ============================================================================

def calculer_taux_occupation_espaces():
    """
    Calcule le taux d'occupation de chaque espace en Python
    Formule: (heures réservées / heures disponibles sur la période) * 100
    Hypothèse: 10h/jour ouvrables, 20 jours sur janvier
    """
    conn = database.get_connection()
    cursor = conn.cursor()
    
    # Récupérer les espaces et leurs heures réservées
    query = """
        SELECT 
            e.espace_id,
            e.nom,
            e.type,
            COALESCE(SUM(r.duree_heures), 0) AS heures_reservees
        FROM Espaces e
        LEFT JOIN Reservations r ON e.espace_id = r.espace_id 
            AND r.statut != 'Annulée'
            AND r.date_reservation BETWEEN '2026-01-01' AND '2026-01-31'
        GROUP BY e.espace_id, e.nom, e.type
    """
    
    cursor.execute(query)
    espaces = cursor.fetchall()
    conn.close()
    
    # Calcul Python du taux d'occupation
    heures_disponibles = 10 * 20  # 10h/jour * 20 jours ouvrables
    
    resultats = []
    for espace in espaces:
        heures_reservees = espace['heures_reservees']
        taux_occupation = (heures_reservees / heures_disponibles) * 100
        
        resultats.append({
            'espace': espace['nom'],
            'type': espace['type'],
            'heures_reservees': heures_reservees,
            'heures_disponibles': heures_disponibles,
            'taux_occupation_pourcent': round(taux_occupation, 2)
        })
    
    # Tri par taux décroissant
    resultats.sort(key=lambda x: x['taux_occupation_pourcent'], reverse=True)
    
    return resultats


def calculer_indice_popularite_espaces():
    """
    Calcule un indice de popularité en Python
    Formule: (Nombre de réservations × 10) + (CA total / 100)
    """
    conn = database.get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            e.nom AS espace,
            e.type,
            COUNT(r.reservation_id) AS nb_reservations,
            COALESCE(SUM(r.montant_total), 0) AS ca_total
        FROM Espaces e
        LEFT JOIN Reservations r ON e.espace_id = r.espace_id AND r.statut != 'Annulée'
        GROUP BY e.espace_id, e.nom, e.type
    """
    
    cursor.execute(query)
    espaces = cursor.fetchall()
    conn.close()
    
    # Calcul Python de l'indice
    resultats = []
    for espace in espaces:
        nb_reservations = espace['nb_reservations']
        ca_total = espace['ca_total']
        
        indice = (nb_reservations * 10) + (ca_total / 100)
        
        resultats.append({
            'espace': espace['espace'],
            'type': espace['type'],
            'nombre_reservations': nb_reservations,
            'ca_total': ca_total,
            'indice_popularite': round(indice, 2)
        })
    
    # Tri par indice décroissant
    resultats.sort(key=lambda x: x['indice_popularite'], reverse=True)
    
    return resultats
