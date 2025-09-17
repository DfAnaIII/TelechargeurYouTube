# Telechargeur YouTube ✨

Un téléchargeur YouTube moderne avec interface graphique, développé en Python. Ce projet permet de télécharger facilement des vidéos et de l'audio depuis YouTube avec plusieurs options avancées.

---

## 🚀 Fonctionnalités principales

### Interface Graphique (Desktop)
- Interface moderne avec CustomTkinter
- Mode sombre/clair commutable
- **Barre de menu dynamique** : sélection de tous les thèmes existants via le menu "Thème"
- Prévisualisation des vidéos avant téléchargement
- Téléchargement multiple (plusieurs URLs à la fois)
- Choix de qualité : best, 1080p, 720p, 480p, audio uniquement
- Formats audio : MP3, AAC, OGG, WAV, OPUS
- Sélection du dossier de téléchargement
- Barre de progression et logs en temps réel
- Personnalisation des thèmes via l’éditeur intégré

---

## 📋 Prérequis

- Python 3.7+
- FFmpeg (pour la conversion audio)
- yt-dlp, PIL/Pillow, requests, customtkinter, flask

---

## 🛠️ Installation

1. **Clonez le repository :**
   ```bash
   git clone https://github.com/DfAnaIII/TelechargeurYouTube.git
   cd TelechargeurYouTube
   ```

2. **Installez les dépendances :**
   ```bash
   pip install -r fichier/requirements.txt
   ```

3. **Installez FFmpeg :**
   - **Windows :** Téléchargez depuis [ffmpeg.org](https://ffmpeg.org/download.html)
   - **macOS :** `brew install ffmpeg`
   - **Linux :** `sudo apt install ffmpeg`

---

## 🚀 Utilisation

### Interface Graphique

```bash
python fichier/main.py
```

---

## 📁 Structure du Projet

```
TelechargeurYouTube/
├── fichier/
│   ├── main.py               # Interface graphique principale
│   ├── main.html             # Template HTML
│   └── requirements.txt      # Dépendances Python  
├── themes.json               # Thèmes personnalisés
├── last_theme.json           # Dernier thème utilisé
├── README.md                 # Ce fichier
```

---

## 🎨 Barre de menu et gestion des thèmes

- La barre de menu propose :
  - **Thème** : tous les thèmes présents dans `themes.json` sont listés et sélectionnables dynamiquement
  - **Aide** (À propos)
- Un éditeur graphique permet de créer et sauvegarder vos propres thèmes.
- Le thème sélectionné est mémorisé pour la prochaine ouverture.

---

## 🎮 Utilisation de l'Interface Graphique

1. Entrez l'URL YouTube dans le champ de texte
2. Cliquez sur "Prévisualiser" pour voir les détails de la vidéo
3. Choisissez la qualité et le format souhaités
4. Sélectionnez le dossier de destination (optionnel)
5. Cliquez sur "Télécharger Vidéo" ou "Télécharger Audio"
6. Changez le thème via la barre de menu ou le bouton

---

## 🔧 Technologies Utilisées

- Python 3.x
- CustomTkinter
- Flask
- yt-dlp
- PIL/Pillow
- requests

---

## 📝 Configuration

### Formats Audio Supportés
- MP3 (par défaut)
- AAC
- OGG
- WAV
- OPUS

### Qualités Vidéo Supportées
- Best (meilleure qualité disponible)
- 1080p
- 720p
- 480p
- Audio uniquement

---

## 🤝 Contribution

Les contributions sont les bienvenues !
1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Commitez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## ⚠️ Avertissement

Assurez-vous de respecter les conditions d'utilisation de YouTube et les lois sur le copyright de votre pays lors de l'utilisation de cet outil.

---

## 🆘 Support

Si vous rencontrez des problèmes :
1. Vérifiez que FFmpeg est installé
2. Assurez-vous que toutes les dépendances sont installées
3. Ouvrez une issue sur GitHub

---

Développé avec ❤️ par [DfAnaIII](https://github.com/DfAnaIII)