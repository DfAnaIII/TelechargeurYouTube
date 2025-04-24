import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import requests
from PIL import Image, ImageTk
from io import BytesIO


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
    if en_cours:
        label_animation.config(text="⏳ Téléchargement en cours...")
    else:
        label_animation.config(text="")


# Interface graphique
fenetre = tk.Tk()
fenetre.title("Téléchargeur YouTube")
fenetre.geometry("420x400")  # Augmentation de la taille de la fenêtre pour inclure la prévisualisation

label = tk.Label(fenetre, text="URL de la vidéo YouTube :")
label.pack(pady=10)

entry_url = tk.Entry(fenetre, width=50)
entry_url.pack(pady=5)

btn_previsualiser = tk.Button(fenetre, text="Prévisualiser", command=obtenir_previsualisation)
btn_previsualiser.pack(pady=5)

label_titre = tk.Label(fenetre, text="", font=("Arial", 12, "bold"))
label_titre.pack(pady=10)

label_image = tk.Label(fenetre)
label_image.pack(pady=5)

btn_telecharger_video = tk.Button(fenetre, text="Télécharger Vidéo", command=telecharger_video)
btn_telecharger_video.pack(pady=5)

btn_telecharger_audio = tk.Button(fenetre, text="Télécharger Audio (MP3)", command=telecharger_audio)
btn_telecharger_audio.pack(pady=5)

label_animation = tk.Label(fenetre, text="", font=("Arial", 10, "italic"))
label_animation.pack(pady=10)

fenetre.mainloop()
