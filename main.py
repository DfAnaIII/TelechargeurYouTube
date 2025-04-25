import customtkinter as ctk
import subprocess, threading, requests, json
from PIL import Image, ImageTk
from io import BytesIO
import re

# Initialisation Dark Mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def clean_title(title):
    # Supprimer (xxx) et [xxx] du titre
    cleaned = re.sub(r"\s*\(.*?\)", "", title)
    cleaned = re.sub(r"\s*\[.*?\]", "", cleaned)
    return cleaned.strip()

def telecharger_video():
    url = entry_url.get()

    # On récupère d'abord les infos de la vidéo pour extraire un titre propre
    try:
        result = subprocess.run(["yt-dlp", "-j", url], capture_output=True, text=True, check=True)
        video_info = json.loads(result.stdout)
        raw_title = video_info.get("title", "video")
        clean_file_title = clean_title(raw_title)

        # On définit un nom de fichier propre
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

    try:
        # On récupère les infos de la vidéo
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
        return

    try:
        result = subprocess.run(["yt-dlp", "-j", url], capture_output=True, text=True, check=True)
        video_info = json.loads(result.stdout)
        titre = video_info.get('title', 'Titre non disponible')
        miniature_url = video_info.get('thumbnail', '')

        label_titre.configure(text=f"Titre : {titre}")

        if miniature_url:
            img_data = requests.get(miniature_url).content
            img = Image.open(BytesIO(img_data))
            img.thumbnail((180, 180))
            img_tk = ImageTk.PhotoImage(img)
            label_image.configure(image=img_tk)
            label_image.image = img_tk
        else:
            label_image.configure(image="")

    except Exception as e:
        print("Erreur :", e)

def lancer_telechargement(commande, message_succes):
    def run():
        label_animation.configure(text="⏳ Téléchargement en cours...")
        try:
            subprocess.run(commande, check=True)
            label_animation.configure(text="✅ " + message_succes)
        except:
            label_animation.configure(text="❌ Échec du téléchargement.")
    threading.Thread(target=run).start()

# === Interface ===
app = ctk.CTk()
app.title("Téléchargeur YouTube yt-dlp")
app.geometry("500x600")

entry_url = ctk.CTkEntry(app, placeholder_text="URL de la vidéo YouTube", width=400)
entry_url.pack(pady=15)

btn_previsu = ctk.CTkButton(app, text="👁️ Prévisualiser", command=obtenir_previsualisation, corner_radius=20)
btn_previsu.pack(pady=10)

label_titre = ctk.CTkLabel(app, text="", font=("Segoe UI", 14))
label_titre.pack(pady=5)

label_image = ctk.CTkLabel(app, text="")
label_image.pack(pady=5)

btn_video = ctk.CTkButton(app, text="⬇️ Télécharger Vidéo", command=telecharger_video, corner_radius=20, width=200)
btn_video.pack(pady=8)

btn_audio = ctk.CTkButton(app, text="🎧 Télécharger Audio", command=telecharger_audio, corner_radius=20, width=200)
btn_audio.pack(pady=8)

label_animation = ctk.CTkLabel(app, text="", font=("Segoe UI", 11, "italic"))
label_animation.pack(pady=15)

app.mainloop()
