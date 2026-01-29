"""
Interface graphique Tkinter - Design Futuriste
Application de gestion de réservations d'espaces
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import service
import database


# Palette de couleurs futuriste
COLORS = {
    'bg_dark': '#0a0e27',
    'bg_medium': '#1a1f3a',
    'bg_card': '#252b48',
    'primary': '#00d4ff',
    'secondary': '#7b2cbf',
    'accent': '#00ff88',
    'text': '#e0e0e0',
    'text_dim': '#8892b0',
    'danger': '#ff006e',
    'warning': '#ffbe0b',
    'success': '#06ffa5'
}


class FuturisticButton(tk.Button):
    """Bouton avec effet futuriste"""
    
    def __init__(self, parent, text, command, color, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=color,
            fg='#ffffff',
            font=('Consolas', 10, 'bold'),
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=12,
            cursor='hand2',
            activebackground=color,
            activeforeground='#ffffff',
            **kwargs
        )
        
        self.default_color = color
        self.hover_color = self.lighten_color(color)
        
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def lighten_color(self, hex_color):
        """Éclaircit une couleur hexadécimale"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, int(r * 1.2))
        g = min(255, int(g * 1.2))
        b = min(255, int(b * 1.2))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def on_enter(self, e):
        self['bg'] = self.hover_color
    
    def on_leave(self, e):
        self['bg'] = self.default_color


class Application(tk.Tk):
    """Application principale avec interface Tkinter futuriste"""
    
    def __init__(self):
        super().__init__()
        
        # Initialiser la base avec des données de test
        database.init_database()
        database.populate_sample_data()
        
        # Configuration de la fenêtre
        self.title("CYBER RESERVATIONS v2.0")
        self.geometry("1400x800")
        self.configure(bg=COLORS['bg_dark'])
        
        # Style
        self.setup_style()
        
        # Créer l'interface
        self.create_widgets()
        
    def setup_style(self):
        """Configure le style des widgets ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        
    def create_widgets(self):
        """Crée tous les widgets de l'interface"""
        
        # Barre de titre futuriste
        title_frame = tk.Frame(self, bg=COLORS['bg_medium'], height=100)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="⚡ CYBER RESERVATIONS SYSTEM ⚡",
            font=('Orbitron', 24, 'bold'),
            bg=COLORS['bg_medium'],
            fg=COLORS['primary']
        )
        title_label.pack(expand=True)
        
        subtitle = tk.Label(
            title_frame,
            text="GESTION INTELLIGENTE D'ESPACES",
            font=('Consolas', 10),
            bg=COLORS['bg_medium'],
            fg=COLORS['text_dim']
        )
        subtitle.pack()
        
        # Frame principal
        main_frame = tk.Frame(self, bg=COLORS['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panneau gauche - Menu
        left_panel = tk.Frame(main_frame, bg=COLORS['bg_card'], width=280)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Titre du menu
        menu_title = tk.Label(
            left_panel,
            text="◢ NAVIGATION ◣",
            font=('Consolas', 12, 'bold'),
            bg=COLORS['bg_card'],
            fg=COLORS['primary'],
            pady=15
        )
        menu_title.pack()
        
        # Ligne de séparation lumineuse
        sep1 = tk.Frame(left_panel, bg=COLORS['primary'], height=2)
        sep1.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Boutons du menu
        btn_config = [
            ("▶ Reservations", self.afficher_reservations, COLORS['primary']),
            ("▶ Indicateurs", self.afficher_indicateurs, COLORS['primary']),
            ("▶ Top Espaces", self.afficher_espaces_demandes, COLORS['primary']),
            ("▶ Top Clients", self.afficher_meilleurs_clients, COLORS['primary']),
            ("▶ Volume Temps", self.afficher_volume_periode, COLORS['primary']),
            ("▶ CA par Type", self.afficher_ca_par_type, COLORS['primary']),
            ("▶ Taux Occup.", self.afficher_taux_occupation, COLORS['secondary']),
            ("▶ Popularite", self.afficher_indice_popularite, COLORS['secondary']),
        ]
        
        for text, cmd, color in btn_config:
            btn = FuturisticButton(left_panel, text, cmd, color)
            btn.pack(fill=tk.X, padx=15, pady=5)
        
        # Séparateur
        sep2 = tk.Frame(left_panel, bg=COLORS['accent'], height=2)
        sep2.pack(fill=tk.X, padx=20, pady=15)
        
        # Boutons d'action
        btn_add = FuturisticButton(
            left_panel,
            "✚ NOUVELLE RESA",
            self.ouvrir_dialog_reservation,
            COLORS['success']
        )
        btn_add.pack(fill=tk.X, padx=15, pady=5)
        
        btn_reset = FuturisticButton(
            left_panel,
            "⟳ RESET BDD",
            self.reinitialiser_base,
            COLORS['danger']
        )
        btn_reset.pack(fill=tk.X, padx=15, pady=5)
        
        btn_quit = FuturisticButton(
            left_panel,
            "✕ QUITTER",
            self.quit,
            COLORS['warning']
        )
        btn_quit.pack(fill=tk.X, padx=15, pady=5)
        
        # Panneau droit - Zone d'affichage
        right_panel = tk.Frame(main_frame, bg=COLORS['bg_card'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Titre de la zone d'affichage
        display_title = tk.Label(
            right_panel,
            text="═══ TERMINAL DATA ═══",
            font=('Consolas', 11, 'bold'),
            bg=COLORS['bg_card'],
            fg=COLORS['accent'],
            pady=10
        )
        display_title.pack()
        
        # Zone de texte avec style cyberpunk
        text_frame = tk.Frame(right_panel, bg=COLORS['primary'], bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.text_area = scrolledtext.ScrolledText(
            text_frame,
            font=('Consolas', 10),
            bg='#0d1117',
            fg=COLORS['accent'],
            insertbackground=COLORS['primary'],
            selectbackground=COLORS['secondary'],
            selectforeground='#ffffff',
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=15
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Message d'accueil
        self.afficher_message_accueil()
        
        # Barre de statut
        status_bar = tk.Frame(self, bg=COLORS['bg_medium'], height=30)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        status_bar.pack_propagate(False)
        
        status_label = tk.Label(
            status_bar,
            text="● SYSTEM READY | DATABASE ONLINE | PYTHON CORE v3.12",
            font=('Consolas', 8),
            bg=COLORS['bg_medium'],
            fg=COLORS['text_dim'],
            anchor=tk.W
        )
        status_label.pack(side=tk.LEFT, padx=15)
    
    def afficher_message_accueil(self):
        """Affiche le message d'accueil futuriste"""
        self.text_area.delete(1.0, tk.END)
        message = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        ⚡ CYBER RESERVATIONS MANAGEMENT SYSTEM ⚡              ║
║                    [ INITIALIZATION COMPLETE ]                 ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

┌─[ MODULES DISPONIBLES ]
│
├─► Salles de reunion
├─► Bureaux temporaires  
├─► Espaces evenementiels
│
└─[ OPERATIONS DISPONIBLES ]
   │
   ├─ CONSULTER les reservations
   ├─ ANALYSER l'occupation
   ├─ GENERER des statistiques
   ├─ AJOUTER de nouvelles reservations
   └─ ADMINISTRER la base de donnees

┌─[ INFO ]
│
├─ Boutons VIOLETS = Calculs Python
└─ Boutons CYAN = Requetes SQL

>>> Selectionnez une operation dans le panneau de navigation...

        """
        self.text_area.insert(1.0, message)
    
    def afficher_reservations(self):
        """Affiche toutes les réservations"""
        self.text_area.delete(1.0, tk.END)
        reservations = service.get_all_reservations()
        
        if not reservations:
            self.text_area.insert(1.0, "\n>>> ERREUR: Aucune reservation trouvee\n")
            return
        
        output = "\n" + "="*130 + "\n"
        output += "                          [ LISTE DES RESERVATIONS ]\n"
        output += "="*130 + "\n\n"
        output += f"{'ID':<5} {'Date':<12} {'Heure':<8} {'Duree':<8} {'Client':<25} {'Espace':<25} {'Type':<22} {'Statut':<12} {'Montant':<10}\n"
        output += "-"*130 + "\n"
        
        for r in reservations:
            output += f"{r['reservation_id']:<5} {r['date_reservation']:<12} {r['heure_debut']:<8} {r['duree_heures']:<8}h {r['client']:<25} {r['espace']:<25} {r['type_espace']:<22} {r['statut']:<12} {r['montant_total']:<10.2f} EUR\n"
        
        output += "="*130 + "\n"
        output += f"\n>>> TOTAL: {len(reservations)} reservation(s) chargee(s)\n"
        
        self.text_area.insert(1.0, output)
    
    def afficher_indicateurs(self):
        """Affiche les indicateurs globaux"""
        self.text_area.delete(1.0, tk.END)
        
        stats = service.get_statistiques_globales()
        
        output = "\n" + "="*80 + "\n"
        output += "                   [ INDICATEURS GLOBAUX ]\n"
        output += "="*80 + "\n\n"
        output += f"┌─[ FINANCIER ]\n"
        output += f"│  CA TOTAL:        {stats['ca_total'] or 0:>12.2f} EUR\n"
        output += f"│  MONTANT MOYEN:   {stats['montant_moyen'] or 0:>12.2f} EUR\n"
        output += f"│\n"
        output += f"├─[ ACTIVITE ]\n"
        output += f"│  RESERVATIONS:    {stats['nombre_reservations'] or 0:>12}\n"
        output += f"│  HEURES TOTAL:    {stats['heures_totales'] or 0:>12} h\n"
        output += f"│  DUREE MOYENNE:   {stats['duree_moyenne'] or 0:>12.2f} h\n"
        output += f"│\n"
        output += f"└─[ FIN DES STATS ]\n"
        output += "\n" + "="*80 + "\n"
        
        self.text_area.insert(1.0, output)
    
    def afficher_espaces_demandes(self):
        """Affiche le classement des espaces"""
        self.text_area.delete(1.0, tk.END)
        espaces = service.get_espaces_les_plus_demandes()
        
        output = "\n" + "="*125 + "\n"
        output += "                         [ ESPACES LES PLUS DEMANDES ]\n"
        output += "="*125 + "\n\n"
        output += f"{'Espace':<30} {'Type':<22} {'Cap.':<6} {'Resa':<8} {'Heures':<10} {'CA (EUR)':<15} {'Moy (EUR)':<12}\n"
        output += "-"*125 + "\n"
        
        for i, e in enumerate(espaces, 1):
            rank = f"#{i}"
            output += f"{rank:>3} {e['espace']:<27} {e['type']:<22} {e['capacite']:<6} {e['nombre_reservations']:<8} {e['heures_totales'] or 0:<10} {e['ca_total'] or 0:<15.2f} {e['montant_moyen'] or 0:<12.2f}\n"
        
        output += "="*125 + "\n"
        
        self.text_area.insert(1.0, output)
    
    def afficher_meilleurs_clients(self):
        """Affiche le classement des clients"""
        self.text_area.delete(1.0, tk.END)
        clients = service.get_meilleurs_clients()
        
        output = "\n" + "="*115 + "\n"
        output += "                            [ TOP CLIENTS ]\n"
        output += "="*115 + "\n\n"
        output += f"{'Rang':<6} {'Client':<22} {'Entreprise':<18} {'Resa':<8} {'Total (EUR)':<13} {'Moy (EUR)':<12} {'Heures':<10}\n"
        output += "-"*115 + "\n"
        
        for i, c in enumerate(clients, 1):
            output += f"{i:<6} {c['client']:<22} {c['entreprise']:<18} {c['nombre_reservations']:<8} {c['montant_total']:<13.2f} {c['montant_moyen']:<12.2f} {c['heures_totales']:<10}\n"
        
        output += "="*115 + "\n"
        
        self.text_area.insert(1.0, output)
    
    def afficher_volume_periode(self):
        """Affiche le volume par période"""
        self.text_area.delete(1.0, tk.END)
        periodes = service.get_reservations_par_periode(2026, 1)
        
        output = "\n" + "="*90 + "\n"
        output += "              [ VOLUME JANVIER 2026 ]\n"
        output += "="*90 + "\n\n"
        output += f"{'Date':<15} {'Reservations':<15} {'Heures':<15} {'CA (EUR)':<20}\n"
        output += "-"*90 + "\n"
        
        for p in periodes:
            output += f"{p['date_reservation']:<15} {p['nombre_reservations']:<15} {p['heures_reservees']:<15} {p['ca_jour']:<20.2f}\n"
        
        output += "="*90 + "\n"
        
        self.text_area.insert(1.0, output)
    
    def afficher_ca_par_type(self):
        """Affiche le CA par type"""
        self.text_area.delete(1.0, tk.END)
        types = service.get_ca_par_type_espace()
        
        output = "\n" + "="*105 + "\n"
        output += "                      [ CHIFFRE D'AFFAIRES PAR TYPE ]\n"
        output += "="*105 + "\n\n"
        output += f"{'Type':<25} {'Reservations':<15} {'Heures':<12} {'CA (EUR)':<18} {'Moyenne (EUR)':<15}\n"
        output += "-"*105 + "\n"
        
        for t in types:
            output += f"{t['type']:<25} {t['nombre_reservations'] or 0:<15} {t['heures_totales'] or 0:<12} {t['ca_total'] or 0:<18.2f} {t['montant_moyen'] or 0:<15.2f}\n"
        
        output += "="*105 + "\n"
        
        self.text_area.insert(1.0, output)
    
    def afficher_taux_occupation(self):
        """Affiche les taux d'occupation (Python)"""
        self.text_area.delete(1.0, tk.END)
        taux = service.calculer_taux_occupation_espaces()
        
        output = "\n" + "="*110 + "\n"
        output += "                [ TAUX D'OCCUPATION - CALCUL PYTHON ]\n"
        output += "="*110 + "\n\n"
        output += f"{'Espace':<30} {'Type':<25} {'H. Resa':<13} {'H. Dispo':<12} {'Taux %':<10}\n"
        output += "-"*110 + "\n"
        
        for t in taux:
            output += f"{t['espace']:<30} {t['type']:<25} {t['heures_reservees']:<13} {t['heures_disponibles']:<12} {t['taux_occupation_pourcent']:<10.2f}%\n"
        
        output += "="*110 + "\n"
        output += "\n[i] Calcul Python: (H. reservees / 200h disponibles) x 100\n"
        output += "[i] Base: 10h/jour x 20 jours = 200h\n"
        
        self.text_area.insert(1.0, output)
    
    def afficher_indice_popularite(self):
        """Affiche l'indice de popularité (Python)"""
        self.text_area.delete(1.0, tk.END)
        indices = service.calculer_indice_popularite_espaces()
        
        output = "\n" + "="*110 + "\n"
        output += "                 [ INDICE POPULARITE - CALCUL PYTHON ]\n"
        output += "="*110 + "\n\n"
        output += f"{'Espace':<30} {'Type':<25} {'Resa':<10} {'CA (EUR)':<15} {'Indice':<15}\n"
        output += "-"*110 + "\n"
        
        for idx in indices:
            output += f"{idx['espace']:<30} {idx['type']:<25} {idx['nombre_reservations']:<10} {idx['ca_total']:<15.2f} {idx['indice_popularite']:<15.2f}\n"
        
        output += "="*110 + "\n"
        output += "\n[i] Formule Python: (Nb reservations x 10) + (CA / 100)\n"
        
        self.text_area.insert(1.0, output)
    
    def ouvrir_dialog_reservation(self):
        """Ouvre une fenêtre pour ajouter une réservation"""
        dialog = DialogReservation(self)
        self.wait_window(dialog)
        if hasattr(dialog, 'success') and dialog.success:
            self.afficher_reservations()
    
    def reinitialiser_base(self):
        """Réinitialise la base de données"""
        if messagebox.askyesno(
            "Confirmation",
            "ATTENTION!\n\nReinitialiser la base de donnees?\nToutes les donnees seront perdues."
        ):
            try:
                database.init_database()
                database.populate_sample_data()
                messagebox.showinfo("Succes", "Base de donnees reinitialisee!")
                self.afficher_message_accueil()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur: {e}")


class DialogReservation(tk.Toplevel):
    """Dialogue pour ajouter une réservation"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.success = False
        
        self.title("Nouvelle Reservation")
        self.geometry("500x450")
        self.configure(bg=COLORS['bg_dark'])
        self.resizable(False, False)
        
        # Titre
        title_frame = tk.Frame(self, bg=COLORS['bg_medium'], height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title = tk.Label(
            title_frame,
            text="✚ NOUVELLE RESERVATION",
            font=('Consolas', 14, 'bold'),
            bg=COLORS['bg_medium'],
            fg=COLORS['accent']
        )
        title.pack(expand=True)
        
        # Formulaire
        form_frame = tk.Frame(self, bg=COLORS['bg_dark'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Client ID
        tk.Label(form_frame, text="ID Client:", font=('Consolas', 10), bg=COLORS['bg_dark'], fg=COLORS['text']).pack(anchor=tk.W, pady=(0, 5))
        self.client_entry = tk.Entry(form_frame, font=('Consolas', 11), bg=COLORS['bg_card'], fg=COLORS['text'], insertbackground=COLORS['primary'], relief=tk.FLAT, bd=5)
        self.client_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Espace ID
        tk.Label(form_frame, text="ID Espace:", font=('Consolas', 10), bg=COLORS['bg_dark'], fg=COLORS['text']).pack(anchor=tk.W, pady=(0, 5))
        self.espace_entry = tk.Entry(form_frame, font=('Consolas', 11), bg=COLORS['bg_card'], fg=COLORS['text'], insertbackground=COLORS['primary'], relief=tk.FLAT, bd=5)
        self.espace_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Date
        tk.Label(form_frame, text="Date (AAAA-MM-JJ):", font=('Consolas', 10), bg=COLORS['bg_dark'], fg=COLORS['text']).pack(anchor=tk.W, pady=(0, 5))
        self.date_entry = tk.Entry(form_frame, font=('Consolas', 11), bg=COLORS['bg_card'], fg=COLORS['text'], insertbackground=COLORS['primary'], relief=tk.FLAT, bd=5)
        self.date_entry.insert(0, "2026-01-30")
        self.date_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Heure
        tk.Label(form_frame, text="Heure (HH:MM):", font=('Consolas', 10), bg=COLORS['bg_dark'], fg=COLORS['text']).pack(anchor=tk.W, pady=(0, 5))
        self.heure_entry = tk.Entry(form_frame, font=('Consolas', 11), bg=COLORS['bg_card'], fg=COLORS['text'], insertbackground=COLORS['primary'], relief=tk.FLAT, bd=5)
        self.heure_entry.insert(0, "09:00")
        self.heure_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Durée
        tk.Label(form_frame, text="Duree (heures):", font=('Consolas', 10), bg=COLORS['bg_dark'], fg=COLORS['text']).pack(anchor=tk.W, pady=(0, 5))
        self.duree_entry = tk.Entry(form_frame, font=('Consolas', 11), bg=COLORS['bg_card'], fg=COLORS['text'], insertbackground=COLORS['primary'], relief=tk.FLAT, bd=5)
        self.duree_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Boutons
        btn_frame = tk.Frame(self, bg=COLORS['bg_dark'])
        btn_frame.pack(fill=tk.X, padx=30, pady=(0, 30))
        
        btn_valider = FuturisticButton(btn_frame, "✓ VALIDER", self.valider_reservation, COLORS['success'])
        btn_valider.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        btn_annuler = FuturisticButton(btn_frame, "✕ ANNULER", self.destroy, COLORS['danger'])
        btn_annuler.pack(side=tk.LEFT, expand=True, fill=tk.X)
    
    def valider_reservation(self):
        """Valide et enregistre la réservation"""
        try:
            client_id = int(self.client_entry.get())
            espace_id = int(self.espace_entry.get())
            date_reservation = self.date_entry.get()
            heure_debut = self.heure_entry.get()
            duree_heures = int(self.duree_entry.get())
            
            if duree_heures <= 0:
                messagebox.showwarning("Erreur", "La duree doit etre superieure a 0")
                return
            
            resultat = service.ajouter_reservation(client_id, espace_id, date_reservation, heure_debut, duree_heures)
            
            if resultat['succes']:
                messagebox.showinfo(
                    "Succes",
                    f"{resultat['message']}\nMontant: {resultat['montant_total']:.2f} EUR"
                )
                self.success = True
                self.destroy()
            else:
                messagebox.showerror("Erreur", resultat['message'])
                
        except ValueError:
            messagebox.showwarning("Erreur", "Valeurs invalides")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))


if __name__ == "__main__":
    app = Application()
    app.mainloop()
