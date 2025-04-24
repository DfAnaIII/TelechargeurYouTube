import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import requests
from PIL import Image, ImageTk
from io import BytesIO
import json


def telecharger_video():
    # Initialisation de la commande pour télécharger la vidéo
    commande = ["yt-dlp", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4", entry_url.get()]
    # Ajouter le chemin de ffmpeg
    commande += ["--ffmpeg-location", r"C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin"]
    lancer_telechargement(commande, "Vidéo téléchargée !")


def telecharger_audio():
    # Initialisation de la commande pour télécharger l'audio
    commande = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        entry_url.get()
    ]
    # Ajouter le chemin de ffmpeg
    commande += ["--ffmpeg-location", r"C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin"]
    lancer_telechargement(commande, "Audio téléchargé en MP3 !")


def obtenir_previsualisation():
    url = entry_url.get()
    if not url:
        messagebox.showwarning("Attention", "Veuillez entrer une URL.")
        return

    try:
        # Utilisation de yt-dlp pour obtenir les métadonnées
        result = subprocess.run(
            ["yt-dlp", "-j", url],
            capture_output=True, text=True, check=True
        )
        data = result.stdout

        # Extraction de la miniature et du titre
        import json
        video_info = json.loads(data)
        title = video_info.get('title', 'Titre non disponible')
        thumbnail_url = video_info.get('thumbnail', '')

        # Affichage du titre
        label_titre.config(text=f"Titre : {title}")

        # Télécharger et afficher la miniature
        if thumbnail_url:
            response = requests.get(thumbnail_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img.thumbnail((150, 150))  # Redimensionner l'image
            img_tk = ImageTk.PhotoImage(img)
            label_image.config(image=img_tk)
            label_image.image = img_tk  # Garder la référence pour ne pas perdre l'image
        else:
            label_image.config(image="")
            label_titre.config(text="Miniature non disponible.")

    except subprocess.CalledProcessError:
        messagebox.showerror("Erreur", "Erreur lors de la récupération des informations de la vidéo.")


def lancer_telechargement(commande, message_succes):
    url = entry_url.get()
    if not url:
        messagebox.showwarning("Attention", "Veuillez entrer une URL.")
        return

    def telechargement():
        animer_label(True)
        try:
            subprocess.run(commande, check=True)
            messagebox.showinfo("Succès", message_succes)
        except subprocess.CalledProcessError:
            messagebox.showerror("Erreur", "Le téléchargement a échoué.")
        finally:
            animer_label(False)

    threading.Thread(target=telechargement).start()


# Animation : affichage / masquage du texte pendant le téléchargement

def animer_label(en_cours):
    label_animation.config(text="⏳ Téléchargement en cours..." if en_cours else "")# === Interface graphique ===


# === Interface graphique ===

fenetre = tk.Tk()
fenetre.title("🎬 Téléchargeur YouTube - yt-dlp")
fenetre.geometry("500x400")
fenetre.configure(bg="#f4f4f4")

style_btn = {"bg": "#4285F4", "fg": "white", "activebackground": "#3367D6", "relief": "raised", "bd": 2, "font": ("Helvetica", 10, "bold")}

frame_url = tk.Frame(fenetre, bg="#f4f4f4")
frame_url.pack(pady=10)

label = tk.Label(frame_url, text="🎯 URL YouTube :", bg="#f4f4f4", font=("Helvetica", 11))
label.pack()

entry_url = tk.Entry(frame_url, width=50, bd=2, relief="solid", font=("Helvetica", 10))
entry_url.pack(pady=5)

btn_previsualiser = tk.Button(fenetre, text="👁️ Prévisualiser", command=obtenir_previsualisation, **style_btn)
btn_previsualiser.pack(pady=8)

label_titre = tk.Label(fenetre, text="", bg="#f4f4f4", font=("Helvetica", 12, "bold"))
label_titre.pack(pady=5)

label_image = tk.Label(fenetre, bg="#f4f4f4")
label_image.pack(pady=5)

frame_btn = tk.Frame(fenetre, bg="#f4f4f4")
frame_btn.pack(pady=10)

btn_telecharger_video = tk.Button(frame_btn, text="⬇️ Télécharger Vidéo", command=telecharger_video, width=20, **style_btn)
btn_telecharger_video.grid(row=0, column=0, padx=10)

btn_telecharger_audio = tk.Button(frame_btn, text="🎧 Télécharger Audio", command=telecharger_audio, width=20, **style_btn)
btn_telecharger_audio.grid(row=0, column=1, padx=10)

label_animation = tk.Label(fenetre, text="", bg="#f4f4f4", fg="#333", font=("Arial", 10, "italic"))
label_animation.pack(pady=15)

fenetre.mainloop()