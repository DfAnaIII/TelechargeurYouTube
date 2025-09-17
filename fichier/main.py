import tkinter.filedialog as filedialog
import customtkinter as ctk
import tkinter as tk
import subprocess
import webbrowser
import threading
import requests
import json
import os
import sys
import shutil
from PIL import Image, ImageTk
from io import BytesIO

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

def save_last_theme(theme_name):
    with open("../last_theme.json", "w") as f:
        json.dump({"last_theme": theme_name}, f)

def load_last_theme():
    try:
        with open("../last_theme.json", "r") as f:
            data = json.load(f)
            return data.get("last_theme", "dark-blue")
    except Exception:
        return "dark-blue"

def load_theme(theme_name):
    if not os.path.exists("../themes.json"):
        with open("../themes.json", "w") as f:
            json.dump({"dark-blue": {
                "bg_color": "#222E3C",
                "fg_color": "#3D4A5A",
                "button_color": "#22577A",
                "text_color": "#FFFFFF",
                "border_color": "#1A2332",
                "hover_color": "#294157"
            }}, f, indent=2)
    with open("../themes.json", "r") as f:
        themes = json.load(f)
    return themes.get(theme_name, themes["dark-blue"])

def save_theme_to_file(theme_name, theme_dict):
    if not os.path.exists("../themes.json"):
        with open("../themes.json", "w") as f:
            json.dump({theme_name: theme_dict}, f, indent=2)
    else:
        with open("../themes.json", "r") as f:
            try:
                themes = json.load(f)
            except Exception:
                themes = {}
        themes[theme_name] = theme_dict
        with open("../themes.json", "w") as f:
            json.dump(themes, f, indent=2)

def get_all_themes():
    if not os.path.exists("../themes.json"):
        return ["dark-blue"]
    with open("../themes.json", "r") as f:
        themes = json.load(f)
    return list(themes.keys())

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Icône d'application (PNG)
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        try:
            img = tk.PhotoImage(file=icon_path)
            self.iconphoto(True, img)
        except Exception as e:
            print("Erreur chargement icône :", e)

        self.title("Téléchargeur YouTube ✨")
        self.geometry("1000x750")

        # ----- Barre de menu -----
        menubar = tk.Menu(self)
        theme_menu = tk.Menu(menubar, tearoff=0)
        for theme_name in get_all_themes():
            theme_menu.add_command(
                label=theme_name,
                command=lambda tn=theme_name: self.change_theme(tn)
            )
        theme_menu.add_separator()
        theme_menu.add_command(label="Éditeur de thème", command=self.ouvrir_editeur_theme)
        menubar.add_cascade(label="Thème", menu=theme_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(
            label="Site du projet",
            command=lambda: webbrowser.open("https://github.com/DfAnaIII/TelechargeurYouTube")
        )
        help_menu.add_command(label="À propos", command=self.afficher_a_propos)
        menubar.add_cascade(label="Aide", menu=help_menu)
        self.config(menu=menubar)

        self.dossier_telechargement = os.getcwd()

        # --- Zone URL
        self.label_url = ctk.CTkLabel(self, text="Entrez une ou plusieurs URLs (une par ligne) :")
        self.label_url.pack(pady=(10, 0))
        self.text_urls = ctk.CTkTextbox(self, height=100)
        self.text_urls.pack(padx=20, pady=(5, 10), fill="x")

        self.btn_previsualiser = ctk.CTkButton(self, text="Prévisualiser", command=self.previsualiser)
        self.btn_previsualiser.pack(pady=(0, 10))

        # --- Infos vidéo
        self.frame_info = ctk.CTkFrame(self)
        self.frame_info.pack(pady=(0,10), padx=20, fill="x")
        self.label_titre = ctk.CTkLabel(self.frame_info, text="", font=("Arial", 15, "bold"))
        self.label_titre.grid(row=0, column=0, sticky="w", padx=5)
        self.label_stats = ctk.CTkLabel(self.frame_info, text="", font=("Arial", 12))
        self.label_stats.grid(row=1, column=0, sticky="w", padx=5)
        self.image_preview = ctk.CTkLabel(self.frame_info, text="")
        self.image_preview.grid(row=0, column=1, rowspan=2, padx=5)

        # --- Options
        self.label_options = ctk.CTkLabel(self, text="Options de téléchargement :")
        self.label_options.pack(pady=(10, 0))
        self.choix_qualite = ctk.CTkComboBox(self, values=["best", "1080p", "720p", "480p", "audio"], width=120)
        self.choix_qualite.set("best")
        self.choix_qualite.pack(pady=5)
        self.format_audio = ctk.CTkComboBox(self, values=["mp3", "aac", "ogg", "wav", "opus"], width=120)
        self.format_audio.set("mp3")
        self.format_audio.pack(pady=5)
        self.btn_dossier = ctk.CTkButton(self, text="📂 Choisir dossier de téléchargement", command=self.choisir_dossier)
        self.btn_dossier.pack(pady=5)
        self.btn_video = ctk.CTkButton(self, text="Télécharger Vidéo", command=self.telecharger_video)
        self.btn_video.pack(pady=5)
        self.btn_audio = ctk.CTkButton(self, text="Télécharger Audio", command=self.telecharger_audio)
        self.btn_audio.pack(pady=5)

        # --- Barre de progression détaillée
        self.progress_frame = ctk.CTkFrame(self)
        self.progress_frame.pack(pady=10, padx=20, fill="x")
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=5, fill="x", padx=5)
        self.label_progress = ctk.CTkLabel(self.progress_frame, text="")
        self.label_progress.pack(pady=0)

        # --- Logs
        self.logs = ctk.CTkTextbox(self, height=100)
        self.logs.pack(padx=20, pady=(5, 10), fill="x")

        # --- Thèmes
        self.theme_list = get_all_themes()
        self.current_theme = load_last_theme()
        if self.current_theme in self.theme_list:
            self.current_theme_idx = self.theme_list.index(self.current_theme)
        else:
            self.current_theme_idx = 0
            self.current_theme = self.theme_list[0]
        self.btn_theme = ctk.CTkButton(self, text=f"Thème : {self.current_theme}", command=self.changer_theme)
        self.btn_theme.pack(pady=5)
        self.btn_theme_editor = ctk.CTkButton(self, text="Éditeur de thème", command=self.ouvrir_editeur_theme)
        self.btn_theme_editor.pack(pady=5)

        self.apply_theme(load_theme(self.current_theme))
        self.btn_theme.configure(text=f"Thème : {self.current_theme}")

    # --- Barre de menu : actions ---
    def menu_ouvrir(self):
        file = filedialog.askopenfilename(title="Ouvrir un fichier", filetypes=[("JSON", "*.json"), ("Tout", "*.*")])
        if file:
            self.notif_popup(f"Fichier ouvert :\n{file}", "Info")

    def menu_quitter(self):
        self.destroy()

    def afficher_a_propos(self):
        self.notif_popup("Téléchargeur YouTube\nVersion 2.0\npar DfAnaIII", "À propos")

    # --- Notifications pop-up ---
    def notif_popup(self, message, title="Notification"):
        top = ctk.CTkToplevel(self)
        top.title(title)
        top.geometry("340x120")
        label = ctk.CTkLabel(top, text=message, font=("Arial", 15))
        label.pack(pady=20)
        btn = ctk.CTkButton(top, text="OK", command=top.destroy)
        btn.pack(pady=5)

    # --- Notifications système adaptées à macOS ---
    def notif_systeme(self, titre, message):
        if sys.platform == "darwin":
            # Utilisation d'osascript natif Mac
            script = f'display notification "{message}" with title "{titre}"'
            try:
                subprocess.run(["osascript", "-e", script])
            except Exception as e:
                print("Notification système impossible :", e)
        else:
            try:
                from plyer import notification
                notification.notify(title=titre, message=message, timeout=5)
            except Exception as e:
                print("Notification système impossible :", e)

    def change_theme(self, new_theme):
        self.current_theme = new_theme
        self.apply_theme(load_theme(new_theme))
        save_last_theme(new_theme)
        self.btn_theme.configure(text=f"Thème : {new_theme}")

    def changer_theme(self):
        self.current_theme_idx = (self.current_theme_idx + 1) % len(self.theme_list)
        theme_name = self.theme_list[self.current_theme_idx]
        self.change_theme(theme_name)

    def apply_theme(self, theme):
        self.configure(fg_color=theme["bg_color"])
        self.label_url.configure(bg_color=theme["bg_color"], text_color=theme["text_color"])
        self.label_titre.configure(bg_color=theme["bg_color"], text_color=theme["text_color"])
        self.label_options.configure(bg_color=theme["bg_color"], text_color=theme["text_color"])
        self.text_urls.configure(fg_color=theme["fg_color"], text_color=theme["text_color"])
        self.logs.configure(fg_color=theme["fg_color"], text_color=theme["text_color"])
        self.btn_previsualiser.configure(fg_color=theme["button_color"], text_color=theme["text_color"])
        self.btn_dossier.configure(fg_color=theme["button_color"], text_color=theme["text_color"])
        self.btn_video.configure(fg_color=theme["button_color"], text_color=theme["text_color"])
        self.btn_audio.configure(fg_color=theme["button_color"], text_color=theme["text_color"])
        self.btn_theme.configure(fg_color=theme["button_color"], text_color=theme["text_color"])
        self.btn_theme_editor.configure(fg_color=theme["button_color"], text_color=theme["text_color"])
        self.choix_qualite.configure(
            fg_color=theme["fg_color"],
            bg_color=theme["bg_color"],
            border_color=theme.get("border_color", theme["button_color"]),
            text_color=theme["text_color"],
            button_color=theme["button_color"]
        )
        self.format_audio.configure(
            fg_color=theme["fg_color"],
            bg_color=theme["bg_color"],
            border_color=theme.get("border_color", theme["button_color"]),
            text_color=theme["text_color"],
            button_color=theme["button_color"]
        )
        self.progress_bar.configure(
            fg_color=theme["button_color"],
            bg_color=theme["fg_color"],
            border_color=theme.get("border_color", theme["button_color"])
        )
        self.image_preview.configure(bg_color=theme["bg_color"])
        self.frame_info.configure(fg_color=theme["fg_color"])
        self.progress_frame.configure(fg_color=theme["fg_color"])

    def choisir_dossier(self):
        dossier = filedialog.askdirectory()
        if dossier:
            self.dossier_telechargement = dossier

    def afficher_logs(self, texte):
        self.logs.insert("end", texte + "\n")
        self.logs.see("end")

    def previsualiser(self):
        url = self.text_urls.get("1.0", "end").strip().splitlines()[0]
        if not url:
            self.afficher_logs("Aucune URL valide.")
            self.notif_popup("Aucune URL valide.", "Erreur")
            return
        try:
            result = subprocess.run(["yt-dlp", "-j", url], capture_output=True, text=True, check=True)
            info = json.loads(result.stdout)
            titre = info.get("title", "Titre non trouvé")
            image_url = info.get("thumbnail", None)
            vues = info.get("view_count", None)
            duree = info.get("duration", None)
            self.label_titre.configure(text=f"Titre : {titre}")

            stats = []
            if vues: stats.append(f"{vues:,} vues")
            if duree: stats.append(f"Durée : {int(duree//60)}:{int(duree%60):02d}")
            self.label_stats.configure(text=" | ".join(stats) if stats else "")

            if image_url:
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content)).resize((160, 90))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(160, 90))
                self.image_preview.configure(image=ctk_img, text="")
            self.notif_popup(f"Prévisualisation OK : {titre}", "Succès")
        except Exception as e:
            self.afficher_logs(f"Erreur prévisualisation : {e}")
            self.notif_popup(f"Erreur prévisualisation : {e}", "Erreur")

    def nettoyer_nom(self, titre):
        import re
        return re.sub(r"\s*(\(.*?\)|\[.*?\])", "", titre).strip()

    def telecharger_video(self):
        urls = self.text_urls.get("1.0", "end").strip().splitlines()
        qualite = self.choix_qualite.get()
        self.telecharger(urls, mode="video", qualite=qualite)

    def telecharger_audio(self):
        urls = self.text_urls.get("1.0", "end").strip().splitlines()
        format_audio = self.format_audio.get()
        self.telecharger(urls, mode="audio", format_audio=format_audio)

    def telecharger(self, urls, mode, qualite="best", format_audio="mp3"):
        import re
        def thread_func():
            self.progress_bar.set(0)
            self.label_progress.configure(text="")
            # Détection automatique de ffmpeg
            ffmpeg_path = shutil.which("ffmpeg")
            for url in urls:
                try:
                    commande = ["yt-dlp", url]
                    if mode == "video":
                        if qualite != "best":
                            commande += ["-f", f"bestvideo[height<={qualite}]+bestaudio"]
                    elif mode == "audio":
                        commande += ["-x", "--audio-format", format_audio]
                    if ffmpeg_path:
                        commande += ["--ffmpeg-location", ffmpeg_path]
                    else:
                        self.afficher_logs("⚠️ ffmpeg n'est pas installé, conversion mp3 impossible !")
                    commande += ["-P", self.dossier_telechargement, "--restrict-filenames"]
                    commande += ["--output", "%(title).80s.%(ext)s"]
                    commande += ["--no-playlist", "--progress"]
                    self.afficher_logs(f"Téléchargement : {url}")
                    process = subprocess.Popen(commande, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                    nom_fichier = None
                    taille_mo = 0.0
                    total_percent = 0.0
                    while True:
                        line = process.stdout.readline()
                        if not line:
                            break
                        self.afficher_logs(line.strip())
                        # Extraction du nom de fichier
                        if "Destination:" in line:
                            match = re.search(r'Destination:\s*(.+)$', line)
                            if match and match.group(1).strip():
                                nom_fichier = match.group(1).strip()
                        # Progression
                        if "[download]" in line and "%" in line:
                            try:
                                parts = line.split()
                                percent = float(parts[1].replace('%', '').replace(',', '.'))
                                total_percent = percent
                                taille_str = [p for p in parts if "MiB" in p]
                                if taille_str:
                                    taille_mo = float(taille_str[0].replace('MiB', '').replace(',', '.'))
                                self.progress_bar.set(total_percent/100)
                                self.label_progress.configure(text=f"Téléchargement: {nom_fichier if nom_fichier else ''} - {total_percent:.1f}% ({taille_mo:.1f} MiB)")
                            except Exception:
                                pass
                    process.wait()
                    # Correction: valeur par défaut si rien trouvé
                    if not nom_fichier or nom_fichier in ["", None]:
                        nom_fichier = "Fichier téléchargé"
                    if process.returncode == 0:
                        self.afficher_logs("✔️ Terminé")
                        self.notif_popup("Téléchargement terminé !", "Succès")
                        self.notif_systeme("Téléchargement terminé", f"{nom_fichier}")
                    else:
                        self.afficher_logs("❌ Erreur lors du téléchargement")
                        self.notif_popup("Erreur lors du téléchargement", "Erreur")
                        self.notif_systeme("Erreur téléchargement", f"{nom_fichier}")
                except Exception as e:
                    self.afficher_logs(f"❌ Erreur : {e}")
                    self.notif_popup(f"Erreur : {e}", "Erreur")
                    self.notif_systeme("Erreur téléchargement", str(e))
            self.progress_bar.set(1.0)
            self.label_progress.configure(text="Téléchargement(s) terminé(s)")
        threading.Thread(target=thread_func, daemon=True).start()

    def ouvrir_editeur_theme(self):
        top = ctk.CTkToplevel(self)
        top.title("Éditeur de thème")
        top.geometry("350x420")
        labels = [
            ("Nom du thème", "theme_name"),
            ("bg_color", "bg_color"),
            ("fg_color", "fg_color"),
            ("button_color", "button_color"),
            ("text_color", "text_color"),
            ("border_color", "border_color"),
            ("hover_color", "hover_color"),
        ]
        entries = {}
        for idx, (lbl, key) in enumerate(labels):
            lab = ctk.CTkLabel(top, text=lbl)
            lab.pack()
            ent = ctk.CTkEntry(top, placeholder_text=f"{lbl} (#RRGGBB ou nom)")
            ent.pack(pady=2)
            entries[key] = ent

        def preview_theme():
            theme = {k: v.get() for k, v in entries.items() if k != "theme_name"}
            self.apply_theme(theme)

        def save_theme():
            theme_name = entries["theme_name"].get().strip()
            if not theme_name:
                self.notif_popup("Nom du thème manquant", "Erreur")
                return
            theme = {k: v.get().strip() for k, v in entries.items() if k != "theme_name"}
            save_theme_to_file(theme_name, theme)
            self.notif_popup(f"Thème '{theme_name}' sauvegardé !", "Succès")
            self.theme_list = get_all_themes()
            self.current_theme_idx = self.theme_list.index(theme_name)
            self.change_theme(theme_name)

        btn_preview = ctk.CTkButton(top, text="Prévisualiser", command=preview_theme)
        btn_preview.pack(pady=5)
        btn_save = ctk.CTkButton(top, text="Sauvegarder", command=save_theme)
        btn_save.pack(pady=5)

if __name__ == '__main__':
    app = App()
    app.mainloop()