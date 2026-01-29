"""
Interface graphique avec tkinter
Application de gestion des ventes
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import service
import database
import os


class Application(tk.Tk):
    """Application principale avec interface tkinter"""
    
    def __init__(self):
        super().__init__()
        
        # Vérifier et initialiser la base si nécessaire
        if not os.path.exists(database.DB_PATH):
            database.init_database()
            database.populate_sample_data()
        
        # Configuration de la fenêtre principale
        self.title("Application de Gestion des Ventes")
        self.geometry("1000x700")
        self.configure(bg='#f0f0f0')
        
        # Créer les widgets
        self.create_widgets()
    
    def create_widgets(self):
        """Crée tous les widgets de l'interface"""
        
        # Titre
        title_frame = tk.Frame(self, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', pady=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text="📊 APPLICATION DE GESTION DES VENTES",
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Frame principal avec 2 colonnes
        main_frame = tk.Frame(self, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Colonne gauche - Boutons
        left_frame = tk.Frame(main_frame, bg='#f0f0f0', width=250)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Titre des actions
        tk.Label(
            left_frame,
            text="ACTIONS",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0'
        ).pack(pady=(0, 10))
        
        # Boutons d'action
        btn_style = {
            'font': ('Arial', 11),
            'width': 25,
            'height': 2,
            'bg': '#3498db',
            'fg': 'white',
            'activebackground': '#2980b9',
            'cursor': 'hand2',
            'relief': 'flat'
        }
        
        tk.Button(
            left_frame,
            text="📋 Voir les ventes",
            command=self.afficher_ventes,
            **btn_style
        ).pack(pady=5)
        
        tk.Button(
            left_frame,
            text="💰 Indicateurs globaux",
            command=self.afficher_indicateurs,
            **btn_style
        ).pack(pady=5)
        
        tk.Button(
            left_frame,
            text="🏆 Classement produits",
            command=self.afficher_classement_produits,
            **btn_style
        ).pack(pady=5)
        
        tk.Button(
            left_frame,
            text="👥 Classement clients",
            command=self.afficher_classement_clients,
            **btn_style
        ).pack(pady=5)
        
        tk.Button(
            left_frame,
            text="📊 CA par catégorie",
            command=self.afficher_ca_categorie,
            **btn_style
        ).pack(pady=5)
        
        tk.Button(
            left_frame,
            text="📈 Taux de vente (Python)",
            command=self.afficher_taux_vente,
            bg='#9b59b6',
            activebackground='#8e44ad',
            **{k: v for k, v in btn_style.items() if k not in ['bg', 'activebackground']}
        ).pack(pady=5)
        
        tk.Button(
            left_frame,
            text="⭐ Indice fidélité (Python)",
            command=self.afficher_indice_fidelite,
            bg='#9b59b6',
            activebackground='#8e44ad',
            **{k: v for k, v in btn_style.items() if k not in ['bg', 'activebackground']}
        ).pack(pady=5)
        
        # Séparateur
        tk.Frame(left_frame, height=2, bg='#bdc3c7').pack(fill='x', pady=15)
        
        tk.Button(
            left_frame,
            text="➕ Ajouter une vente",
            command=self.ouvrir_dialog_vente,
            bg='#27ae60',
            activebackground='#229954',
            **{k: v for k, v in btn_style.items() if k not in ['bg', 'activebackground']}
        ).pack(pady=5)
        
        tk.Button(
            left_frame,
            text="🔄 Réinitialiser BDD",
            command=self.reinitialiser_base,
            bg='#e74c3c',
            activebackground='#c0392b',
            **{k: v for k, v in btn_style.items() if k not in ['bg', 'activebackground']}
        ).pack(pady=5)
        
        tk.Button(
            left_frame,
            text="❌ Quitter",
            command=self.quit,
            bg='#95a5a6',
            activebackground='#7f8c8d',
            **{k: v for k, v in btn_style.items() if k not in ['bg', 'activebackground']}
        ).pack(pady=5)
        
        # Colonne droite - Zone d'affichage
        right_frame = tk.Frame(main_frame, bg='white', relief='solid', borderwidth=1)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Zone de texte scrollable
        self.text_area = scrolledtext.ScrolledText(
            right_frame,
            font=('Courier New', 10),
            bg='white',
            wrap='none'
        )
        self.text_area.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Message d'accueil
        self.afficher_message_accueil()
    
    def afficher_message_accueil(self):
        """Affiche le message d'accueil"""
        self.text_area.delete('1.0', tk.END)
        message = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          BIENVENUE DANS L'APPLICATION DE GESTION             ║
║                      DES VENTES                              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

📌 Sélectionnez une action dans le menu de gauche

📊 Fonctionnalités disponibles :
   • Consulter les ventes
   • Voir les analyses et statistiques
   • Ajouter de nouvelles ventes
   • Gérer la base de données

💡 Les boutons violets = Calculs effectués en Python
   Les autres = Requêtes SQL pures

        """
        self.text_area.insert('1.0', message)
    
    def afficher_ventes(self):
        """Affiche toutes les ventes"""
        self.text_area.delete('1.0', tk.END)
        ventes = service.get_all_ventes()
        
        if not ventes:
            self.text_area.insert('1.0', "\n❌ Aucune vente enregistrée\n")
            return
        
        output = "\n" + "="*120 + "\n"
        output += "                                    LISTE DES VENTES\n"
        output += "="*120 + "\n\n"
        output += f"{'ID':<5} {'Date':<20} {'Client':<20} {'Produit':<25} {'Qté':<8} {'Montant':<12}\n"
        output += "-"*120 + "\n"
        
        for v in ventes:
            date = v['date_vente'][:19]
            output += f"{v['vente_id']:<5} {date:<20} {v['nom_client']:<20} {v['nom_produit']:<25} {v['quantite']:<8} {v['montant_total']:<12.2f} €\n"
        
        output += "="*120 + "\n"
        output += f"\n📦 Total: {len(ventes)} vente(s)\n"
        
        self.text_area.insert('1.0', output)
    
    def afficher_indicateurs(self):
        """Affiche les indicateurs globaux"""
        self.text_area.delete('1.0', tk.END)
        
        ca = service.get_chiffre_affaires_total()
        qte = service.get_quantite_totale_vendue()
        nb = service.get_nombre_ventes()
        moy = service.get_montant_moyen_vente()
        
        output = "\n" + "="*80 + "\n"
        output += "                        INDICATEURS GLOBAUX\n"
        output += "="*80 + "\n\n"
        output += f"💰 Chiffre d'affaires total:  {ca:,.2f} €\n\n"
        output += f"📦 Quantité totale vendue:    {qte} unités\n\n"
        output += f"🛒 Nombre de ventes:          {nb}\n\n"
        output += f"📊 Montant moyen par vente:   {moy:,.2f} €\n"
        output += "\n" + "="*80 + "\n"
        
        self.text_area.insert('1.0', output)
    
    def afficher_classement_produits(self):
        """Affiche le classement des produits"""
        self.text_area.delete('1.0', tk.END)
        produits = service.get_classement_produits()
        
        output = "\n" + "="*110 + "\n"
        output += "                              CLASSEMENT DES PRODUITS\n"
        output += "="*110 + "\n\n"
        output += f"{'Produit':<30} {'Catégorie':<15} {'Ventes':<10} {'Quantité':<12} {'CA (€)':<15}\n"
        output += "-"*110 + "\n"
        
        for p in produits:
            output += f"{p['produit']:<30} {p['categorie']:<15} {p['nombre_ventes']:<10} {p['quantite_vendue']:<12} {p['chiffre_affaires']:<15,.2f}\n"
        
        output += "="*110 + "\n"
        
        self.text_area.insert('1.0', output)
    
    def afficher_classement_clients(self):
        """Affiche le classement des clients"""
        self.text_area.delete('1.0', tk.END)
        clients = service.get_meilleurs_clients()
        
        output = "\n" + "="*100 + "\n"
        output += "                              CLASSEMENT DES CLIENTS\n"
        output += "="*100 + "\n\n"
        output += f"{'Client':<25} {'Ville':<15} {'Achats':<10} {'Total (€)':<15} {'Panier moy.':<15}\n"
        output += "-"*100 + "\n"
        
        for c in clients:
            output += f"{c['client']:<25} {c['ville']:<15} {c['nombre_achats']:<10} {c['montant_total']:<15,.2f} {c['panier_moyen']:<15,.2f}\n"
        
        output += "="*100 + "\n"
        
        self.text_area.insert('1.0', output)
    
    def afficher_ca_categorie(self):
        """Affiche le CA par catégorie"""
        self.text_area.delete('1.0', tk.END)
        categories = service.get_ca_par_categorie()
        
        output = "\n" + "="*95 + "\n"
        output += "                           CHIFFRE D'AFFAIRES PAR CATÉGORIE\n"
        output += "="*95 + "\n\n"
        output += f"{'Catégorie':<20} {'Ventes':<10} {'Quantité':<12} {'CA (€)':<15} {'Moy. (€)':<15}\n"
        output += "-"*95 + "\n"
        
        for cat in categories:
            output += f"{cat['categorie']:<20} {cat['nombre_ventes']:<10} {cat['quantite_totale']:<12} {cat['chiffre_affaires']:<15,.2f} {cat['vente_moyenne']:<15,.2f}\n"
        
        output += "="*95 + "\n"
        
        self.text_area.insert('1.0', output)
    
    def afficher_taux_vente(self):
        """Affiche les taux de vente (calcul Python)"""
        self.text_area.delete('1.0', tk.END)
        taux = service.calculer_taux_conversion_stock()
        
        output = "\n" + "="*100 + "\n"
        output += "                   TAUX DE VENTE DES PRODUITS (Calcul Python)\n"
        output += "="*100 + "\n\n"
        output += f"{'Produit':<30} {'Stock init.':<12} {'Vendu':<10} {'Stock act.':<12} {'Taux %':<10}\n"
        output += "-"*100 + "\n"
        
        for t in taux:
            output += f"{t['produit']:<30} {t['stock_initial']:<12} {t['quantite_vendue']:<10} {t['stock_actuel']:<12} {t['taux_vente_pourcent']:<10.2f}%\n"
        
        output += "="*100 + "\n"
        output += "\n💡 Calcul effectué en Python (pas en SQL)\n"
        
        self.text_area.insert('1.0', output)
    
    def afficher_indice_fidelite(self):
        """Affiche l'indice de fidélité (calcul Python)"""
        self.text_area.delete('1.0', tk.END)
        indices = service.calculer_indice_fidelite_clients()
        
        output = "\n" + "="*105 + "\n"
        output += "                      INDICE DE FIDÉLITÉ CLIENTS (Calcul Python)\n"
        output += "="*105 + "\n\n"
        output += f"{'Client':<25} {'Achats':<10} {'Total (€)':<15} {'Panier moy.':<15} {'Indice':<12}\n"
        output += "-"*105 + "\n"
        
        for idx in indices:
            output += f"{idx['client']:<25} {idx['nombre_achats']:<10} {idx['montant_total']:<15,.2f} {idx['panier_moyen']:<15,.2f} {idx['indice_fidelite']:<12.2f}\n"
        
        output += "="*105 + "\n"
        output += "\n📐 Formule: Indice = (Nombre d'achats × 10) + (Panier moyen / 10)\n"
        output += "💡 Calcul effectué en Python (pas en SQL)\n"
        
        self.text_area.insert('1.0', output)
    
    def ouvrir_dialog_vente(self):
        """Ouvre une fenêtre pour ajouter une vente"""
        dialog = tk.Toplevel(self)
        dialog.title("Ajouter une vente")
        dialog.geometry("400x300")
        dialog.configure(bg='#ecf0f1')
        
        # Titre
        tk.Label(
            dialog,
            text="➕ NOUVELLE VENTE",
            font=('Arial', 14, 'bold'),
            bg='#ecf0f1'
        ).pack(pady=20)
        
        # Frame pour les champs
        form_frame = tk.Frame(dialog, bg='#ecf0f1')
        form_frame.pack(pady=10)
        
        # Client ID
        tk.Label(form_frame, text="ID Client:", font=('Arial', 11), bg='#ecf0f1').grid(row=0, column=0, padx=10, pady=10, sticky='e')
        client_entry = tk.Entry(form_frame, font=('Arial', 11), width=20)
        client_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Produit ID
        tk.Label(form_frame, text="ID Produit:", font=('Arial', 11), bg='#ecf0f1').grid(row=1, column=0, padx=10, pady=10, sticky='e')
        produit_entry = tk.Entry(form_frame, font=('Arial', 11), width=20)
        produit_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Quantité
        tk.Label(form_frame, text="Quantité:", font=('Arial', 11), bg='#ecf0f1').grid(row=2, column=0, padx=10, pady=10, sticky='e')
        quantite_entry = tk.Entry(form_frame, font=('Arial', 11), width=20)
        quantite_entry.grid(row=2, column=1, padx=10, pady=10)
        
        def valider_vente():
            try:
                client_id = int(client_entry.get())
                produit_id = int(produit_entry.get())
                quantite = int(quantite_entry.get())
                
                if quantite <= 0:
                    messagebox.showerror("Erreur", "La quantité doit être supérieure à 0")
                    return
                
                resultat = service.ajouter_vente(client_id, produit_id, quantite)
                
                if resultat['succes']:
                    messagebox.showinfo(
                        "Succès",
                        f"{resultat['message']}\nMontant: {resultat['montant_total']:.2f} €"
                    )
                    dialog.destroy()
                    self.afficher_ventes()
                else:
                    messagebox.showerror("Erreur", resultat['message'])
                    
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des nombres valides")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
        
        # Boutons
        btn_frame = tk.Frame(dialog, bg='#ecf0f1')
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="✅ Valider",
            command=valider_vente,
            font=('Arial', 11),
            bg='#27ae60',
            fg='white',
            width=12,
            cursor='hand2'
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ Annuler",
            command=dialog.destroy,
            font=('Arial', 11),
            bg='#e74c3c',
            fg='white',
            width=12,
            cursor='hand2'
        ).pack(side='left', padx=5)
    
    def reinitialiser_base(self):
        """Réinitialise la base de données"""
        reponse = messagebox.askyesno(
            "Confirmation",
            "⚠️ Voulez-vous vraiment réinitialiser la base de données ?\n\nToutes les données seront effacées et remplacées par les données de test."
        )
        
        if reponse:
            try:
                database.init_database()
                database.populate_sample_data()
                messagebox.showinfo("Succès", "✅ Base de données réinitialisée avec succès!")
                self.afficher_message_accueil()
            except Exception as e:
                messagebox.showerror("Erreur", f"❌ Erreur: {e}")


def main():
    """Fonction principale"""
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
