"""
Interface graphique avec PySide6
Application de gestion de réservations d'espaces
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QDialog, QLineEdit, QMessageBox,
    QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import service
import database


class Application(QMainWindow):
    """Application principale avec interface PySide6"""
    
    def __init__(self):
        super().__init__()
        
        # Initialiser la base avec des données de test au démarrage
        database.init_database()
        database.populate_sample_data()
        
        # Configuration de la fenêtre principale
        self.setWindowTitle("Gestion de Réservations d'Espaces")
        self.setGeometry(100, 100, 1200, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Créer les widgets
        self.create_widgets(central_widget)
    
    def create_widgets(self, central_widget):
        """Crée tous les widgets de l'interface"""
        
        # Layout principal vertical
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Titre
        title_widget = QWidget()
        title_widget.setStyleSheet("background-color: #2c3e50;")
        title_widget.setFixedHeight(80)
        title_layout = QVBoxLayout(title_widget)
        
        title_label = QLabel("🏢 GESTION DE RÉSERVATIONS D'ESPACES")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_layout.addWidget(title_label)
        
        main_layout.addWidget(title_widget)
        
        # Frame principal avec 2 colonnes
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # Colonne gauche - Boutons
        left_widget = QWidget()
        left_widget.setFixedWidth(300)
        left_layout = QVBoxLayout(left_widget)
        
        # Titre des actions
        actions_label = QLabel("ACTIONS")
        actions_label.setAlignment(Qt.AlignCenter)
        actions_label.setFont(QFont("Arial", 12, QFont.Bold))
        left_layout.addWidget(actions_label)
        
        # Style de base pour les boutons
        base_style = """
            QPushButton {
                font-size: 11pt;
                padding: 10px;
                border: none;
                border-radius: 5px;
                color: white;
                text-align: left;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
        """
        
        # Boutons d'action
        btn_reservations = QPushButton("📋 Voir les réservations")
        btn_reservations.setStyleSheet(base_style + "QPushButton { background-color: #3498db; }")
        btn_reservations.clicked.connect(self.afficher_reservations)
        left_layout.addWidget(btn_reservations)
        
        btn_indicateurs = QPushButton("💰 Indicateurs globaux")
        btn_indicateurs.setStyleSheet(base_style + "QPushButton { background-color: #3498db; }")
        btn_indicateurs.clicked.connect(self.afficher_indicateurs)
        left_layout.addWidget(btn_indicateurs)
        
        btn_espaces = QPushButton("🏆 Espaces les plus demandés")
        btn_espaces.setStyleSheet(base_style + "QPushButton { background-color: #3498db; }")
        btn_espaces.clicked.connect(self.afficher_espaces_demandes)
        left_layout.addWidget(btn_espaces)
        
        btn_clients = QPushButton("👥 Meilleurs clients")
        btn_clients.setStyleSheet(base_style + "QPushButton { background-color: #3498db; }")
        btn_clients.clicked.connect(self.afficher_meilleurs_clients)
        left_layout.addWidget(btn_clients)
        
        btn_periode = QPushButton("📊 Volume par période")
        btn_periode.setStyleSheet(base_style + "QPushButton { background-color: #3498db; }")
        btn_periode.clicked.connect(self.afficher_volume_periode)
        left_layout.addWidget(btn_periode)
        
        btn_type = QPushButton("📈 CA par type d'espace")
        btn_type.setStyleSheet(base_style + "QPushButton { background-color: #3498db; }")
        btn_type.clicked.connect(self.afficher_ca_par_type)
        left_layout.addWidget(btn_type)
        
        btn_taux = QPushButton("📊 Taux d'occupation (Python)")
        btn_taux.setStyleSheet(base_style + "QPushButton { background-color: #9b59b6; }")
        btn_taux.clicked.connect(self.afficher_taux_occupation)
        left_layout.addWidget(btn_taux)
        
        btn_popularite = QPushButton("⭐ Indice popularité (Python)")
        btn_popularite.setStyleSheet(base_style + "QPushButton { background-color: #9b59b6; }")
        btn_popularite.clicked.connect(self.afficher_indice_popularite)
        left_layout.addWidget(btn_popularite)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #bdc3c7;")
        separator.setFixedHeight(2)
        left_layout.addWidget(separator)
        
        btn_ajouter = QPushButton("➕ Nouvelle réservation")
        btn_ajouter.setStyleSheet(base_style + "QPushButton { background-color: #27ae60; }")
        btn_ajouter.clicked.connect(self.ouvrir_dialog_reservation)
        left_layout.addWidget(btn_ajouter)
        
        btn_reinit = QPushButton("🔄 Réinitialiser BDD")
        btn_reinit.setStyleSheet(base_style + "QPushButton { background-color: #e74c3c; }")
        btn_reinit.clicked.connect(self.reinitialiser_base)
        left_layout.addWidget(btn_reinit)
        
        btn_quitter = QPushButton("❌ Quitter")
        btn_quitter.setStyleSheet(base_style + "QPushButton { background-color: #95a5a6; }")
        btn_quitter.clicked.connect(self.close)
        left_layout.addWidget(btn_quitter)
        
        left_layout.addStretch()
        
        # Colonne droite - Zone d'affichage
        right_widget = QWidget()
        right_widget.setStyleSheet("background-color: white; border: 1px solid #ddd;")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(5, 5, 5, 5)
        
        # Zone de texte
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setFont(QFont("Courier New", 10))
        self.text_area.setStyleSheet("color: black; background-color: white;")
        right_layout.addWidget(self.text_area)
        
        # Ajouter les colonnes au layout principal
        content_layout.addWidget(left_widget)
        content_layout.addWidget(right_widget)
        
        main_layout.addWidget(content_widget)
        
        # Message d'accueil
        self.afficher_message_accueil()
    
    def afficher_message_accueil(self):
        """Affiche le message d'accueil"""
        self.text_area.clear()
        message = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          BIENVENUE DANS L'APPLICATION DE GESTION             ║
║                  DE RÉSERVATIONS D'ESPACES                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

🏢 Types d'espaces disponibles :
   • Salles de réunion
   • Bureaux temporaires
   • Espaces événementiels

📌 Sélectionnez une action dans le menu de gauche

📊 Fonctionnalités disponibles :
   • Consulter les réservations
   • Analyser l'occupation et les statistiques
   • Ajouter de nouvelles réservations
   • Gérer la base de données

💡 Les boutons violets = Calculs effectués en Python
   Les autres = Requêtes SQL pures

        """
        self.text_area.setPlainText(message)
    
    def afficher_reservations(self):
        """Affiche toutes les réservations"""
        self.text_area.clear()
        reservations = service.get_all_reservations()
        
        if not reservations:
            self.text_area.setText("Aucune reservation enregistree")
            return
        
        output = "\n" + "="*130 + "\n"
        output += "                                    LISTE DES RESERVATIONS\n"
        output += "="*130 + "\n\n"
        output += f"{'ID':<5} {'Date':<12} {'Heure':<8} {'Duree':<8} {'Client':<25} {'Espace':<25} {'Type':<22} {'Statut':<12} {'Montant':<10}\n"
        output += "-"*130 + "\n"
        
        for r in reservations:
            output += f"{r['reservation_id']:<5} {r['date_reservation']:<12} {r['heure_debut']:<8} {r['duree_heures']:<8}h {r['client']:<25} {r['espace']:<25} {r['type_espace']:<22} {r['statut']:<12} {r['montant_total']:<10.2f} euros\n"
        
        output += "="*130 + "\n"
        output += f"\nTotal: {len(reservations)} reservation(s)\n"
        
        self.text_area.setText(output)
    
    def afficher_indicateurs(self):
        """Affiche les indicateurs globaux"""
        self.text_area.clear()
        
        stats = service.get_statistiques_globales()
        
        output = "\n" + "="*80 + "\n"
        output += "                        INDICATEURS GLOBAUX\n"
        output += "="*80 + "\n\n"
        output += f"Chiffre d'affaires total:      {stats['ca_total'] or 0:.2f} euros\n\n"
        output += f"Nombre de reservations:        {stats['nombre_reservations'] or 0}\n\n"
        output += f"Heures totales reservees:      {stats['heures_totales'] or 0} heures\n\n"
        output += f"Duree moyenne par reservation: {stats['duree_moyenne'] or 0:.2f} heures\n\n"
        output += f"Montant moyen par reservation: {stats['montant_moyen'] or 0:.2f} euros\n"
        output += "\n" + "="*80 + "\n"
        
        self.text_area.setText(output)
    
    def afficher_espaces_demandes(self):
        """Affiche le classement des espaces les plus demandés"""
        self.text_area.clear()
        espaces = service.get_espaces_les_plus_demandes()
        
        output = "\n" + "="*120 + "\n"
        output += "                              ESPACES LES PLUS DEMANDES\n"
        output += "="*120 + "\n\n"
        output += f"{'Espace':<30} {'Type':<22} {'Cap.':<6} {'Resa.':<8} {'Heures':<10} {'CA (euros)':<15} {'Moy (euros)':<12}\n"
        output += "-"*120 + "\n"
        
        for e in espaces:
            output += f"{e['espace']:<30} {e['type']:<22} {e['capacite']:<6} {e['nombre_reservations']:<8} {e['heures_totales'] or 0:<10} {e['ca_total'] or 0:<15.2f} {e['montant_moyen'] or 0:<12.2f}\n"
        
        output += "="*120 + "\n"
        
        self.text_area.setText(output)
    
    def afficher_meilleurs_clients(self):
        """Affiche le classement des meilleurs clients"""
        self.text_area.clear()
        clients = service.get_meilleurs_clients()
        
        output = "\n" + "="*115 + "\n"
        output += "                              MEILLEURS CLIENTS\n"
        output += "="*115 + "\n\n"
        output += f"{'Client':<25} {'Entreprise':<20} {'Resa.':<8} {'Total (euros)':<15} {'Moy (euros)':<12} {'Heures':<10}\n"
        output += "-"*115 + "\n"
        
        for c in clients:
            output += f"{c['client']:<25} {c['entreprise']:<20} {c['nombre_reservations']:<8} {c['montant_total']:<15.2f} {c['montant_moyen']:<12.2f} {c['heures_totales']:<10}\n"
        
        output += "="*115 + "\n"
        
        self.text_area.setText(output)
    
    def afficher_volume_periode(self):
        """Affiche le volume de réservations par période"""
        self.text_area.clear()
        periodes = service.get_reservations_par_periode(2026, 1)
        
        output = "\n" + "="*90 + "\n"
        output += "                     VOLUME DE RESERVATIONS PAR JOUR (JANVIER 2026)\n"
        output += "="*90 + "\n\n"
        output += f"{'Date':<15} {'Reservations':<15} {'Heures reservees':<20} {'CA du jour (euros)':<20}\n"
        output += "-"*90 + "\n"
        
        for p in periodes:
            output += f"{p['date_reservation']:<15} {p['nombre_reservations']:<15} {p['heures_reservees']:<20} {p['ca_jour']:<20.2f}\n"
        
        output += "="*90 + "\n"
        
        self.text_area.setText(output)
    
    def afficher_ca_par_type(self):
        """Affiche le CA par type d'espace"""
        self.text_area.clear()
        types = service.get_ca_par_type_espace()
        
        output = "\n" + "="*105 + "\n"
        output += "                           CHIFFRE D'AFFAIRES PAR TYPE D'ESPACE\n"
        output += "="*105 + "\n\n"
        output += f"{'Type':<25} {'Reservations':<15} {'Heures':<12} {'CA (euros)':<18} {'Montant moy (euros)':<15}\n"
        output += "-"*105 + "\n"
        
        for t in types:
            output += f"{t['type']:<25} {t['nombre_reservations'] or 0:<15} {t['heures_totales'] or 0:<12} {t['ca_total'] or 0:<18.2f} {t['montant_moyen'] or 0:<15.2f}\n"
        
        output += "="*105 + "\n"
        
        self.text_area.setText(output)
    
    def afficher_taux_occupation(self):
        """Affiche les taux d'occupation (calcul Python)"""
        self.text_area.clear()
        taux = service.calculer_taux_occupation_espaces()
        
        output = "\n" + "="*110 + "\n"
        output += "                   TAUX D'OCCUPATION DES ESPACES (Calcul Python)\n"
        output += "="*110 + "\n\n"
        output += f"{'Espace':<30} {'Type':<25} {'H. reservees':<15} {'H. dispo.':<12} {'Taux %':<10}\n"
        output += "-"*110 + "\n"
        
        for t in taux:
            output += f"{t['espace']:<30} {t['type']:<25} {t['heures_reservees']:<15} {t['heures_disponibles']:<12} {t['taux_occupation_pourcent']:<10.2f}%\n"
        
        output += "="*110 + "\n"
        output += "\nCalcul effectue en Python (pas en SQL)\n"
        output += "Base: 10h/jour x 20 jours ouvrables = 200h disponibles\n"
        
        self.text_area.setText(output)
    
    def afficher_indice_popularite(self):
        """Affiche l'indice de popularité (calcul Python)"""
        self.text_area.clear()
        indices = service.calculer_indice_popularite_espaces()
        
        output = "\n" + "="*115 + "\n"
        output += "                      INDICE DE POPULARITE DES ESPACES (Calcul Python)\n"
        output += "="*115 + "\n\n"
        output += f"{'Espace':<30} {'Type':<25} {'Resa.':<10} {'CA (euros)':<15} {'Indice':<15}\n"
        output += "-"*115 + "\n"
        
        for idx in indices:
            output += f"{idx['espace']:<30} {idx['type']:<25} {idx['nombre_reservations']:<10} {idx['ca_total']:<15.2f} {idx['indice_popularite']:<15.2f}\n"
        
        output += "="*115 + "\n"
        output += "\nFormule: Indice = (Nombre de reservations x 10) + (CA / 100)\n"
        output += "Calcul effectue en Python (pas en SQL)\n"
        
        self.text_area.setText(output)
    
    def ouvrir_dialog_reservation(self):
        """Ouvre une fenêtre pour ajouter une réservation"""
        dialog = DialogReservation(self)
        if dialog.exec():
            self.afficher_reservations()
    
    def reinitialiser_base(self):
        """Réinitialise la base de données"""
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Voulez-vous vraiment réinitialiser la base de données ?\n\nToutes les données seront effacées et remplacées par les données de test.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                database.init_database()
                database.populate_sample_data()
                QMessageBox.information(self, "Succès", "Base de données réinitialisée avec succès!")
                self.afficher_message_accueil()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur: {e}")


class DialogReservation(QDialog):
    """Dialogue pour ajouter une réservation"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nouvelle réservation")
        self.setFixedSize(450, 350)
        
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("➕ NOUVELLE RÉSERVATION")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Formulaire
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        
        # Client ID
        client_layout = QHBoxLayout()
        client_layout.addWidget(QLabel("ID Client:"))
        self.client_entry = QLineEdit()
        client_layout.addWidget(self.client_entry)
        form_layout.addLayout(client_layout)
        
        # Espace ID
        espace_layout = QHBoxLayout()
        espace_layout.addWidget(QLabel("ID Espace:"))
        self.espace_entry = QLineEdit()
        espace_layout.addWidget(self.espace_entry)
        form_layout.addLayout(espace_layout)
        
        # Date
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Date (AAAA-MM-JJ):"))
        self.date_entry = QLineEdit()
        self.date_entry.setPlaceholderText("2026-01-30")
        date_layout.addWidget(self.date_entry)
        form_layout.addLayout(date_layout)
        
        # Heure
        heure_layout = QHBoxLayout()
        heure_layout.addWidget(QLabel("Heure (HH:MM):"))
        self.heure_entry = QLineEdit()
        self.heure_entry.setPlaceholderText("09:00")
        heure_layout.addWidget(self.heure_entry)
        form_layout.addLayout(heure_layout)
        
        # Durée
        duree_layout = QHBoxLayout()
        duree_layout.addWidget(QLabel("Durée (heures):"))
        self.duree_entry = QLineEdit()
        duree_layout.addWidget(self.duree_entry)
        form_layout.addLayout(duree_layout)
        
        layout.addWidget(form_widget)
        
        # Boutons
        btn_layout = QHBoxLayout()
        
        btn_valider = QPushButton("✅ Valider")
        btn_valider.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; font-size: 11pt;")
        btn_valider.clicked.connect(self.valider_reservation)
        btn_layout.addWidget(btn_valider)
        
        btn_annuler = QPushButton("❌ Annuler")
        btn_annuler.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px; font-size: 11pt;")
        btn_annuler.clicked.connect(self.reject)
        btn_layout.addWidget(btn_annuler)
        
        layout.addLayout(btn_layout)
    
    def valider_reservation(self):
        """Valide et enregistre la réservation"""
        try:
            client_id = int(self.client_entry.text())
            espace_id = int(self.espace_entry.text())
            date_reservation = self.date_entry.text()
            heure_debut = self.heure_entry.text()
            duree_heures = int(self.duree_entry.text())
            
            if duree_heures <= 0:
                QMessageBox.warning(self, "Erreur", "La durée doit être supérieure à 0")
                return
            
            resultat = service.ajouter_reservation(client_id, espace_id, date_reservation, heure_debut, duree_heures)
            
            if resultat['succes']:
                QMessageBox.information(
                    self,
                    "Succès",
                    f"{resultat['message']}\nMontant: {resultat['montant_total']:.2f} €"
                )
                self.accept()
            else:
                QMessageBox.critical(self, "Erreur", resultat['message'])
                
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer des valeurs valides")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))


def main():
    """Fonction principale"""
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
