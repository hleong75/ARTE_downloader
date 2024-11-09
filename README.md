# ARTE_downloader

Ceci est un programme pour capturer uniquement les vidéos ARTE.tv. Le direct est exclu.

## Requirements
```bash
pip install yt_dlp
```

## Installation et utilisation
<h4>Sous Windows</h4>
<h5>I. Pour les débutants :</h5>
<p>Ouvrir le fichier `ARTE_downloader.py` avec spyder.</p>
<h5>II. Pour les experts :</h5>
<p>On suppose Python installé. Ouvrir la CMD</p>

```bash
git clone https://github.com/hleong75/ARTE_downloader/
cd ARTE_downloader
python ARTE_downloader.py
```

<h4>Sous linux</h4>
<h5>On suppose pour les experts :</h5>
<p>Python étant normalement préinstallé</p>

```bash
git clone https://github.com/hleong75/ARTE_downloader/
cd ARTE_downloader
python ARTE_downloader_linux.py --url [url] --quality [qual] --output [path]
```
<h6>Explications</h6>
Utilisation
Exécutez le script avec les options souhaitées :

```bash
python3 arte_downloader.py --url "https://www.arte.tv/fr/videos/XXXXXX/titre-video" --quality "best" --output "/chemin/vers/dossier"
```
<li>Remplacez [url] par l’URL de la vidéo ARTE.</li>
<li>Choisissez [qual] pour indiquer la qualité (best, worst, bestvideo, etc.).</li>
<li>Spécifiez [path] pour définir le dossier de destination.</li>
Exemples :

Télécharger en qualité best dans le dossier courant :

```bash
python3 arte_downloader.py --url "https://www.arte.tv/fr/videos/XXXXXX/titre-video" --quality "best"
```
Télécharger en qualité worst dans un dossier spécifique :

```bash
python3 arte_downloader.py --url "https://www.arte.tv/fr/videos/XXXXXX/titre-video" --quality "worst" --output "/home/user/Vidéos"
```
Vérification :

Le téléchargement se lancera immédiatement, avec la progression affichée dans le terminal.
Une fois terminé, la vidéo sera enregistrée dans le dossier de sortie spécifié.
Ce script en ligne de commande est flexible et permet de gérer facilement plusieurs vidéos en les lançant avec différentes configurations ou en exécutant plusieurs commandes en parallèle.
