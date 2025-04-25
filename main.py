import customtkinter as ctk
import tkinter.messagebox as messagebox
import subprocess
import threading
import requests
import json
import re
from PIL import Image
from io import BytesIO
from customtkinter import CTkImage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def clean_title(title):
    cleaned = re.sub(r"\s*\(.*?\)", "", title)
    cleaned = re.sub(r"\s*\[.*?\]", "", cleaned)
    return cleaned.strip()


def telecharger_video():
    url = entry_url.get()
    if not url:
        messagebox.showwarning("Attention", "Veuillez entrer une URL.")
        return

    try:
        result = subprocess.run(["yt-dlp", "-j", url], capture_output=True, text=True, check=True)
        video_info = json.loads(result.stdout)
        raw_title = video_info.get("title", "video")
        clean_file_title = clean_title(raw_title)
        output_path = f"{clean_file_title}.%(ext)s"

        commande = [
            "yt-dlp",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "--output", output_path,
            "--ffmpeg-location", r"C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin",
            url
        ]
        lancer_telechargement(commande, f"Vidéo téléchargée : {clean_file_title}.mp4")

    except subprocess.CalledProcessError:
        messagebox.showerror("Erreur", "Impossible de récupérer les infos de la vidéo.")


def telecharger_audio():
    url = entry_url.get()
    if not url:
        messagebox.showwarning("Attention", "Veuillez entrer une URL.")
        return

    try:
        result = subprocess.run(["yt-dlp", "-j", url], capture_output=True, text=True, check=True)
        video_info = json.loads(result.stdout)
        raw_title = video_info.get("title", "audio")
        clean_file_title = clean_title(raw_title)
        output_path = f"{clean_file_title}.%(ext)s"

        commande = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--output", output_path,
            "--ffmpeg-location", r"C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin",
            url
        ]
        lancer_telechargement(commande, f"Audio téléchargé : {clean_file_title}.mp3")

    except subprocess.CalledProcessError:
        messagebox.showerror("Erreur", "Impossible de récupérer les infos de la vidéo.")


def obtenir_previsualisation():
    url = entry_url.get()
    if not url:
        messagebox.showwarning("Attention", "Veuillez entrer une URL.")
        return

    try:
        result = subprocess.run(["yt-dlp", "-j", url], capture_output=True, text=True, check=True)
        video_info = json.loads(result.stdout)
        title = video_info.get("title", "Titre non disponible")
        thumbnail_url = video_info.get("thumbnail", "")

        label_titre.configure(text=f"Titre : {title}")

        if thumbnail_url:
            response = requests.get(thumbnail_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img.thumbnail((300, 200))
            img_ctk = CTkImage(light_image=img, size=(300, 200))
            label_image.configure(image=img_ctk)
            label_image.image = img_ctk
        else:
            label_image.configure(image="")
            label_titre.configure(text="Miniature non disponible.")

    except subprocess.CalledProcessError:
        messagebox.showerror("Erreur", "Erreur lors de la récupération des informations de la vidéo.")


def lancer_telechargement(commande, message_succes):
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


def animer_label(en_cours):
    if en_cours:
        label_animation.configure(text="⏳ Téléchargement en cours...")
    else:
        label_animation.configure(text="")


# Interface
fenetre = ctk.CTk()
fenetre.title("YouTube Downloader")
fenetre.geometry("500x600")

label = ctk.CTkLabel(fenetre, text="URL de la vidéo YouTube :", font=("Arial", 14))
label.pack(pady=10)

entry_url = ctk.CTkEntry(fenetre, width=400, height=35)
entry_url.pack(pady=5)

btn_previsualiser = ctk.CTkButton(fenetre, text="Prévisualiser", corner_radius=20, command=obtenir_previsualisation)
btn_previsualiser.pack(pady=10)

label_titre = ctk.CTkLabel(fenetre, text="", font=("Arial", 13, "bold"))
label_titre.pack(pady=10)

label_image = ctk.CTkLabel(fenetre, text="")
label_image.pack(pady=5)

btn_telecharger_video = ctk.CTkButton(fenetre, text="Télécharger Vidéo MP4", corner_radius=20, fg_color="#006699", command=telecharger_video)
btn_telecharger_video.pack(pady=10)

btn_telecharger_audio = ctk.CTkButton(fenetre, text="Télécharger Audio MP3", corner_radius=20, fg_color="#009966", command=telecharger_audio)
btn_telecharger_audio.pack(pady=10)

label_animation = ctk.CTkLabel(fenetre, text="", font=("Arial", 12, "italic"), text_color="#bbbbbb")
label_animation.pack(pady=20)

fenetre.mainloop()
