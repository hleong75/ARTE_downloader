import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import threading

class ArteDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Téléchargeur d'émissions ARTE")
        self.root.geometry("600x500")

        # Interface de base
        self.url_label = tk.Label(root, text="URL de l'émission ARTE :")
        self.url_label.pack(pady=5)
        
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)

        self.path_button = tk.Button(root, text="Sélectionner le dossier", command=self.select_directory)
        self.path_button.pack(pady=5)

        self.directory_path = tk.StringVar()
        self.path_label = tk.Label(root, textvariable=self.directory_path, fg="blue")
        self.path_label.pack(pady=5)

        self.fetch_versions_button = tk.Button(root, text="Lister les versions", command=self.list_versions)
        self.fetch_versions_button.pack(pady=10)

        self.version_frame = tk.Frame(root)
        self.version_frame.pack(pady=10)

        self.version_combobox = ttk.Combobox(self.version_frame, state="readonly", width=50)
        self.version_combobox.pack(side="left", padx=5)

        self.add_version_button = tk.Button(self.version_frame, text="Ajouter cette version", command=self.add_version)
        self.add_version_button.pack(side="left", padx=5)

        self.selected_versions = []

        self.download_button = tk.Button(root, text="Télécharger les versions sélectionnées", command=self.start_downloads)
        self.download_button.pack(pady=10)

        self.download_frame = tk.Frame(root)
        self.download_frame.pack(fill="both", expand=True)

        self.active_downloads = []

    def select_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.directory_path.set(path)

    def list_versions(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Erreur", "Veuillez entrer une URL valide.")
            return

        try:
            options = {'listformats': True, 'quiet': True}
            with yt_dlp.YoutubeDL(options) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                formats = info_dict.get("formats", [])
                self.version_combobox['values'] = [f"{f['format_id']} - {f['format_note']} ({f['ext']})" for f in formats]
                if formats:
                    self.version_combobox.current(0)
                else:
                    messagebox.showinfo("Info", "Aucune version disponible.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lister les versions : {e}")

    def add_version(self):
        version = self.version_combobox.get()
        if version and version not in self.selected_versions:
            self.selected_versions.append(version)
            label = tk.Label(self.download_frame, text=version)
            label.pack(anchor="w")

    def start_downloads(self):
        url = self.url_entry.get()
        path = self.directory_path.get()

        if not url or not path or not self.selected_versions:
            messagebox.showerror("Erreur", "Veuillez entrer une URL, sélectionner un dossier et choisir des versions.")
            return

        for version in self.selected_versions:
            format_id = version.split(" - ")[0]
            download_status = tk.StringVar()
            download_status.set(f"Téléchargement de la version {format_id} en attente...")
            label = tk.Label(self.download_frame, textvariable=download_status)
            label.pack(anchor="w")

            self.active_downloads.append(download_status)

            thread = threading.Thread(target=self.download_video, args=(url, path, format_id, download_status))
            thread.start()

    def download_video(self, url, path, format_id, status_var):
        options = {
            'outtmpl': f'{path}/%(title)s_%(format_id)s.%(ext)s',
            'format': format_id,
            'progress_hooks': [self.create_progress_hook(status_var)]
        }
        
        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                ydl.download([url])
                status_var.set(f"Téléchargement de la version {format_id} terminé !")
            except Exception as e:
                status_var.set(f"Erreur lors du téléchargement de la version {format_id}.")
                messagebox.showerror("Erreur", str(e))

    def create_progress_hook(self, status_var):
        """Crée un hook de progression pour mettre à jour le statut du téléchargement"""
        def progress_hook(d):
            if d['status'] == 'downloading':
                percent = d.get('_percent_str', '').strip()
                speed = d.get('_speed_str', '').strip()
                status_var.set(f"Téléchargement... {percent} à {speed}")
            elif d['status'] == 'finished':
                status_var.set("Téléchargement terminé !")
        return progress_hook

if __name__ == "__main__":
    root = tk.Tk()
    app = ArteDownloader(root)
    root.mainloop()
