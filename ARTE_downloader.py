import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp
import threading

class ArteDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Téléchargeur d'émissions ARTE")
        self.root.geometry("500x200")

        # Label et champ pour l'URL
        self.url_label = tk.Label(root, text="URL de l'émission ARTE :")
        self.url_label.pack(pady=5)
        
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)

        # Bouton pour sélectionner le dossier de téléchargement
        self.path_button = tk.Button(root, text="Sélectionner le dossier", command=self.select_directory)
        self.path_button.pack(pady=5)

        self.directory_path = tk.StringVar()
        self.path_label = tk.Label(root, textvariable=self.directory_path, fg="blue")
        self.path_label.pack(pady=5)

        # Bouton pour lancer le téléchargement
        self.download_button = tk.Button(root, text="Télécharger", command=self.start_download)
        self.download_button.pack(pady=10)

        # Message de statut
        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=5)

    def select_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.directory_path.set(path)

    def start_download(self):
        url = self.url_entry.get()
        path = self.directory_path.get()

        if not url or not path:
            messagebox.showerror("Erreur", "Veuillez entrer une URL et un dossier de téléchargement.")
            return

        self.status_label.config(text="Téléchargement en cours...")
        threading.Thread(target=self.download_video, args=(url, path)).start()

    def download_video(self, url, path):
        # Utilisation du meilleur format disponible
        options = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best'  # Télécharge le meilleur format disponible
        }
        
        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                ydl.download([url])
                self.status_label.config(text="Téléchargement terminé !")
            except Exception as e:
                self.status_label.config(text="Erreur lors du téléchargement.")
                messagebox.showerror("Erreur", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ArteDownloader(root)
    root.mainloop()
