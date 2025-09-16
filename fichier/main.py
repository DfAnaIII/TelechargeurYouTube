import customtkinter as ctk
import tkinter.filedialog as filedialog
import subprocess
import threading
import requests
from PIL import Image
from io import BytesIO
import json
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

def load_theme(theme_name):
    with open("themes.json", "r") as f:
        themes = json.load(f)
    return themes.get(theme_name, themes["dark-blue"])

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Téléchargeur YouTube ✨")
        self.geometry("1000x1750")


        self.dossier_telechargement = os.getcwd()

        self.label_url = ctk.CTkLabel(self, text="Entrez une ou plusieurs URLs (une par ligne) :")
        self.label_url.pack(pady=(10, 0))

        self.text_urls = ctk.CTkTextbox(self, height=100)
        self.text_urls.pack(padx=20, pady=(5, 10), fill="x")

        self.btn_previsualiser = ctk.CTkButton(self, text="Prévisualiser", command=self.previsualiser)
        self.btn_previsualiser.pack(pady=(0, 10))

        self.label_titre = ctk.CTkLabel(self, text="")
        self.label_titre.pack()

        self.image_preview = ctk.CTkLabel(self, text="")
        self.image_preview.pack(pady=5)

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

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10, fill="x", padx=20)

        self.logs = ctk.CTkTextbox(self, height=100)
        self.logs.pack(padx=20, pady=(5, 10), fill="x")

        self.btn_theme = ctk.CTkButton(self, text="Changer de thème", command=self.changer_theme)
        self.btn_theme.pack(pady=5)
        self.theme_list = ["dark-blue", "light", "green","rose","violette"]
        self.current_theme_idx = 0
        self.btn_theme.configure(text=f"Thème : {self.theme_list[self.current_theme_idx]}")

        # Appliquer le thème de base
        self.apply_theme(load_theme("dark-blue"))

    def toggle_theme(self):
        theme_mode = "Dark" if self.switch_theme.get() else "Light"
        ctk.set_appearance_mode(theme_mode)

    def changer_theme(self):
        self.current_theme_idx = (self.current_theme_idx + 1) % len(self.theme_list)
        theme_name = self.theme_list[self.current_theme_idx]
        theme = load_theme(theme_name)
        self.apply_theme(theme)
        self.btn_theme.configure(text=f"Thème : {theme_name}")

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

        self.choix_qualite.configure(
            fg_color=theme["fg_color"],
            bg_color=theme["bg_color"],
            border_color=theme.get("border_color", theme["button_color"]),  # couleur du contour
            text_color=theme["text_color"],
            button_color=theme["button_color"]
        )
        self.format_audio.configure(
            fg_color=theme["fg_color"],
            bg_color=theme["bg_color"],
            border_color=theme["border_color"],
            text_color=theme["text_color"],
            button_color=theme["button_color"]
        )

        self.progress_bar.configure(
            fg_color=theme["button_color"],
            bg_color=theme["fg_color"],
            border_color=theme["border_color"]
        )

        self.image_preview.configure(bg_color=theme["bg_color"])

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
            return
        try:
            result = subprocess.run(["yt-dlp", "-j", url], capture_output=True, text=True, check=True)
            info = json.loads(result.stdout)
            titre = info.get("title", "Titre non trouvé")
            image_url = info.get("thumbnail", None)
            self.label_titre.configure(text=f"Titre : {titre}")

            if image_url:
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content)).resize((160, 90))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(160, 90))
                self.image_preview.configure(image=ctk_img, text="")
        except Exception as e:
            self.afficher_logs(f"Erreur prévisualisation : {e}")

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
        def thread_func():
            self.progress_bar.set(0.1)
            for url in urls:
                try:
                    commande = ["yt-dlp", url, "--ffmpeg-location", r"C:\\ProgramData\\chocolatey\\lib\\ffmpeg\\tools\\ffmpeg\\bin"]
                    if mode == "video":
                        if qualite != "best":
                            commande += ["-f", f"bestvideo[height<={qualite}]+bestaudio"]
                    elif mode == "audio":
                        commande += ["-x", "--audio-format", format_audio]

                    commande += ["-P", self.dossier_telechargement, "--restrict-filenames"]
                    commande += ["--output", f"%(title).80s.%(ext)s"]

                    self.afficher_logs(f"Téléchargement : {url}")
                    subprocess.run(commande, check=True)
                    self.afficher_logs("✔️ Terminé")
                except subprocess.CalledProcessError as e:
                    self.afficher_logs(f"❌ Erreur : {e}")
            self.progress_bar.set(1.0)

        threading.Thread(target=thread_func, daemon=True).start()

if __name__ == '__main__':
    app = App()
    app.mainloop()