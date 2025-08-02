# TelechargeurYouTube ✨

Un téléchargeur YouTube moderne avec interface graphique et web, développé en Python. Ce projet permet de télécharger facilement des vidéos et de l'audio depuis YouTube avec plusieurs options de qualité et formats.

## 🚀 Fonctionnalités

### Interface Graphique (Desktop)
- **Interface moderne** avec CustomTkinter
- **Mode sombre/clair** commutable
- **Prévisualisation** des vidéos avant téléchargement
- **Téléchargement multiple** (plusieurs URLs à la fois)
- **Choix de qualité** : best, 1080p, 720p, 480p, audio uniquement
- **Formats audio** : MP3, AAC, OGG, WAV, OPUS
- **Sélection du dossier** de téléchargement
- **Barre de progression** et logs en temps réel

### Interface Web
- **Interface web simple** avec Flask
- **Téléchargement direct** via navigateur
- **Support MP3 et MP4**
- **Génération automatique** de noms de fichiers

## 📋 Prérequis

- Python 3.7+
- FFmpeg (pour la conversion audio)

## 🛠️ Installation

1. **Clonez le repository :**
```bash
git clone https://github.com/DfAnaIII/TelechargeurYouTube.git
cd TelechargeurYouTube
```

2. **Installez les dépendances :**
```bash
pip install -r requirements.txt
```

3. **Installez FFmpeg :**
   - **Windows :** Téléchargez depuis [ffmpeg.org](https://ffmpeg.org/download.html)
   - **macOS :** `brew install ffmpeg`
   - **Linux :** `sudo apt install ffmpeg`

## 🚀 Utilisation

### Interface Graphique
```bash
python fichier/main.py
```

### Interface Web
```bash
python fichier/app.py
```
Puis ouvrez http://localhost:5000 dans votre navigateur.

## 📁 Structure du Projet

```
TelechargeurYouTube/
├── fichier/
│   ├── main.py               # Interface graphique principale
│   ├── app.py                # Application web Flask
│   └── main.html             # Templates HTML
│   └──requirement.txt        # Plugins Python  
├── TelechargeurYoutube.exe   # Dossier de téléchargements
└── README.md                 # Ce fichier
```

## 🎮 Utilisation de l'Interface Graphique

1. **Entrez l'URL** YouTube dans le champ de texte
2. **Cliquez sur "Prévisualiser"** pour voir les détails de la vidéo
3. **Choisissez la qualité** et le format souhaités
4. **Sélectionnez le dossier** de destination (optionnel)
5. **Cliquez sur "Télécharger Vidéo"** ou **"Télécharger Audio"**

## 🌐 Utilisation de l'Interface Web

1. Accédez à http://localhost:5000
2. Collez l'URL YouTube
3. Choisissez le format (MP3 ou MP4)
4. Cliquez sur télécharger

## 🔧 Technologies Utilisées

- **Python 3.x** - Langage principal
- **CustomTkinter** - Interface graphique moderne
- **Flask** - Framework web
- **yt-dlp** - Téléchargement YouTube
- **PIL/Pillow** - Traitement d'images
- **requests** - Requêtes HTTP

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

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## ⚠️ Avertissement

Assurez-vous de respecter les conditions d'utilisation de YouTube et les lois sur le copyright de votre pays lors de l'utilisation de cet outil.

## 🆘 Support

Si vous rencontrez des problèmes :
1. Vérifiez que FFmpeg est installé
2. Assurez-vous que toutes les dépendances sont installées
3. Ouvrez une issue sur GitHub

---

Développé avec ❤️ par [DfAnaIII](https://github.com/DfAnaIII)
