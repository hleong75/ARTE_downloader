import yt_dlp
import argparse
import os

def download_video(url, path, quality):
    """Télécharge une vidéo depuis une URL ARTE vers le dossier spécifié avec la qualité désirée"""
    options = {
        'outtmpl': f'{path}/%(title)s.%(ext)s',
        'format': quality,  # Définit la qualité selon l'argument passé
        'progress_hooks': [progress_hook]
    }
    
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        print(f"Téléchargement terminé pour : {url}")
    except Exception as e:
        print(f"Erreur lors du téléchargement de {url} : {e}")

def progress_hook(d):
    """Affiche la progression du téléchargement dans la console"""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%').strip()
        speed = d.get('_speed_str', 'N/A').strip()
        print(f"Téléchargement... {percent} à {speed}")
    elif d['status'] == 'finished':
        print("Téléchargement terminé !")

def main():
    # Configuration des arguments de ligne de commande
    parser = argparse.ArgumentParser(description="Téléchargeur d'émissions ARTE")
    parser.add_argument('--url', type=str, required=True, help="URL de la vidéo ARTE à télécharger")
    parser.add_argument('--quality', type=str, default="bestvideo+bestaudio/best",
                        help="Qualité de la vidéo à télécharger (ex: 'best', 'worst', 'bestvideo+bestaudio/best')")
    parser.add_argument('--output', type=str, default=os.getcwd(),
                        help="Dossier de destination pour enregistrer la vidéo (par défaut : dossier courant)")
    
    args = parser.parse_args()

    # Vérification du dossier de sortie
    if not os.path.isdir(args.output):
        print(f"Le dossier spécifié n'existe pas : {args.output}")
        return

    # Lancer le téléchargement avec les paramètres fournis
    download_video(args.url, args.output, args.quality)

if __name__ == "__main__":
    main()
