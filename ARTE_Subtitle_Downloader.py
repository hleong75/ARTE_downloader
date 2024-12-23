import os
import yt_dlp
import webvtt
import tkinter as tk
from tkinter import filedialog, messagebox

def download_and_convert_subtitles(video_url, languages=None, output_dir='.'):
    """
    Télécharge les sous-titres d'une vidéo et les convertit en SRT.

    :param video_url: URL de la vidéo.
    :param languages: Liste des langues souhaitées, ou None pour toutes les langues disponibles.
    :param output_dir: Répertoire de sauvegarde des sous-titres.
    """
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'allsubtitles': languages is None,
        'subtitleslangs': languages if languages else [],
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'quiet': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Téléchargement des sous-titres pour : {video_url}")
            ydl.download([video_url])
        
        # Conversion des fichiers .vtt en .srt
        for file in os.listdir(output_dir):
            if file.endswith('.vtt'):
                vtt_file = os.path.join(output_dir, file)
                srt_file = vtt_file.replace('.vtt', '.srt')
                try:
                    webvtt.read(vtt_file).save_as_srt(srt_file)
                    os.remove(vtt_file)  # Supprime le fichier .vtt après conversion
                    print(f"Converti : {vtt_file} → {srt_file}")
                except Exception as e:
                    print(f"Erreur lors de la conversion de {vtt_file} : {e}")
        messagebox.showinfo("Succès", "Sous-titres téléchargés et convertis en SRT avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

def download_subtitles_gui():
    def start_download():
        video_url = url_entry.get()
        languages = lang_entry.get().split(',') if lang_entry.get() else None
        output_dir = dir_entry.get()

        if not video_url:
            messagebox.showerror("Erreur", "L'URL de la vidéo est obligatoire.")
            return

        if not os.path.exists(output_dir):
            messagebox.showerror("Erreur", f"Le répertoire {output_dir} n'existe pas.")
            return

        download_and_convert_subtitles(video_url, languages, output_dir)

    def browse_directory():
        directory = filedialog.askdirectory()
        if directory:
            dir_entry.delete(0, tk.END)
            dir_entry.insert(0, directory)

    # Interface graphique
    root = tk.Tk()
    root.title("Téléchargeur de sous-titres")
    root.geometry("600x250")

    # URL
    tk.Label(root, text="URL de la vidéo :").grid(row=0, column=0, sticky="w", padx=10, pady=10)
    url_entry = tk.Entry(root, width=50)
    url_entry.grid(row=0, column=1, padx=10, pady=10)

    # Langues
    tk.Label(root, text="Langues (ex: fr,en) :").grid(row=1, column=0, sticky="w", padx=10, pady=10)
    lang_entry = tk.Entry(root, width=50)
    lang_entry.grid(row=1, column=1, padx=10, pady=10)

    # Répertoire
    tk.Label(root, text="Répertoire de sauvegarde :").grid(row=2, column=0, sticky="w", padx=10, pady=10)
    dir_entry = tk.Entry(root, width=50)
    dir_entry.grid(row=2, column=1, padx=10, pady=10)
    browse_button = tk.Button(root, text="Parcourir", command=browse_directory)
    browse_button.grid(row=2, column=2, padx=10, pady=10)

    # Bouton Télécharger
    download_button = tk.Button(root, text="Télécharger et Convertir", command=start_download, bg="green", fg="white")
    download_button.grid(row=3, column=1, pady=20)

    # Lancer l'interface
    root.mainloop()

if __name__ == "__main__":
    download_subtitles_gui()
