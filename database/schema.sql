-- ============================================================================
-- SCHÉMA DE BASE DE DONNÉES - APPLICATION D'ANALYSE MÉTIER
-- ============================================================================
-- Date de création : 29 janvier 2026
-- Description : Base de données pour la gestion des ventes de produits
-- ============================================================================

-- ============================================================================
-- SUPPRESSION DES TABLES EXISTANTES (si elles existent)
-- ============================================================================
DROP TABLE IF EXISTS Ventes;
DROP TABLE IF EXISTS Produits;
DROP TABLE IF EXISTS Clients;

-- ============================================================================
-- TABLE : Clients
-- Description : Stocke les informations des clients
-- ============================================================================
CREATE TABLE Clients (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telephone VARCHAR(20),
    ville VARCHAR(100),
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Index pour améliorer les recherches par email
CREATE INDEX idx_clients_email ON Clients(email);

-- ============================================================================
-- TABLE : Produits
-- Description : Catalogue des produits disponibles
-- ============================================================================
CREATE TABLE Produits (
    produit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(200) NOT NULL,
    description TEXT,
    prix_unitaire DECIMAL(10, 2) NOT NULL CHECK(prix_unitaire > 0),
    categorie VARCHAR(50),
    stock INTEGER DEFAULT 0 CHECK(stock >= 0),
    date_ajout DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Index pour améliorer les recherches par catégorie
CREATE INDEX idx_produits_categorie ON Produits(categorie);

-- ============================================================================
-- TABLE : Ventes
-- Description : Enregistrement des transactions de vente
-- ============================================================================
CREATE TABLE Ventes (
    vente_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    produit_id INTEGER NOT NULL,
    quantite INTEGER NOT NULL CHECK(quantite > 0),
    prix_unitaire DECIMAL(10, 2) NOT NULL CHECK(prix_unitaire > 0),
    montant_total DECIMAL(10, 2) NOT NULL,
    date_vente DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Clés étrangères pour assurer l'intégrité référentielle
    FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE RESTRICT,
    FOREIGN KEY (produit_id) REFERENCES Produits(produit_id) ON DELETE RESTRICT
);

-- Index pour améliorer les performances des requêtes
CREATE INDEX idx_ventes_client ON Ventes(client_id);
CREATE INDEX idx_ventes_produit ON Ventes(produit_id);
CREATE INDEX idx_ventes_date ON Ventes(date_vente);

-- ============================================================================
-- VUES UTILES POUR L'ANALYSE
-- ============================================================================

-- Vue : Détails complets des ventes
CREATE VIEW vue_ventes_completes AS
SELECT 
    v.vente_id,
    v.date_vente,
    c.client_id,
    c.nom || ' ' || c.prenom AS nom_client,
    c.email AS email_client,
    p.produit_id,
    p.nom AS nom_produit,
    p.categorie,
    v.quantite,
    v.prix_unitaire,
    v.montant_total
FROM Ventes v
INNER JOIN Clients c ON v.client_id = c.client_id
INNER JOIN Produits p ON v.produit_id = p.produit_id;

-- Vue : Chiffre d'affaires par produit
CREATE VIEW vue_ca_par_produit AS
SELECT 
    p.produit_id,
    p.nom AS nom_produit,
    p.categorie,
    COUNT(v.vente_id) AS nombre_ventes,
    SUM(v.quantite) AS quantite_totale,
    SUM(v.montant_total) AS chiffre_affaires
FROM Produits p
LEFT JOIN Ventes v ON p.produit_id = v.produit_id
GROUP BY p.produit_id, p.nom, p.categorie;

-- Vue : Chiffre d'affaires par client
CREATE VIEW vue_ca_par_client AS
SELECT 
    c.client_id,
    c.nom || ' ' || c.prenom AS nom_client,
    c.email,
    c.ville,
    COUNT(v.vente_id) AS nombre_achats,
    SUM(v.montant_total) AS montant_total_achats
FROM Clients c
LEFT JOIN Ventes v ON c.client_id = v.client_id
GROUP BY c.client_id, c.nom, c.prenom, c.email, c.ville;

-- ============================================================================
-- FIN DU SCHÉMA
-- ============================================================================
