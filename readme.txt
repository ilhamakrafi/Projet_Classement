# Classement de photos

## Description

Ce projet consiste à réaliser un script Python qui trie automatiquement des photos dans des dossiers organisés par **année/mois**. Il génère également un fichier CSV listant les photos, leur chemin de destination et la source de leur date.

## Fonctionnement

### Parcours et filtrage

Le script parcourt le dossier de photos de manière récursive. Il identifie les fichiers images grâce à une expression régulière qui accepte les extensions `.jpg`, `.jpeg` et `.png`, en minuscules comme en majuscules.

### Extraction de la date

Pour chaque image, le script récupère d’abord la date de stockage du fichier avec `os.path.getmtime()`. Il essaie ensuite de lire les métadonnées EXIF avec `PIL` afin d’obtenir la date de prise de vue (`DateTimeOriginal`).

Si les métadonnées EXIF sont disponibles, elles sont utilisées en priorité. Sinon, le script utilise la date de stockage du fichier.

La source de la date est indiquée dans le CSV :
- `EXIF` : date extraite des métadonnées de la photo ;
- `Stockage` : date de modification du fichier.

### Classement des photos

À partir de l’année et du mois récupérés, le script crée une arborescence de la forme :

```text
photos_projet/
├── 2020/
│   ├── 01/
│   └── 05/
├── 2021/
│   ├── 03/
│   └── 12/
```

Les photos sont ensuite déplacées dans le dossier correspondant à leur année et à leur mois.

### Génération du CSV

Le script enregistre les informations de chaque photo dans une liste, puis les trie chronologiquement selon la date au format `AAAA/MM`.

Il génère ensuite un fichier `listePhotos.csv` contenant, pour chaque photo :

```text
NomFichier;Chemin;SourceDate
```

## Bugs et difficultés

- **Conversion HEIC en JPG/PNG** : les fichiers `.HEIC` ne sont pas pris en charge par le script. Ils doivent être convertis en `.jpg` ou `.png` avant l’exécution.
- **Filtre des extensions** : le symbole `$` a été ajouté à la fin de l’expression régulière afin de vérifier que l’extension se trouve bien à la fin du nom du fichier.
- **Extensions en majuscules** : les extensions `.JPG`, `.JPEG` et `.PNG` ont été ajoutées pour éviter que certaines photos soient ignorées.
- **Tri chronologique** : le tri initial sur tout le tuple ne donnait pas le bon ordre. Il a été corrigé avec `photos_a_classer.sort(key=lambda x: x[0])`, qui trie sur la date.

## Prérequis

- Python 3
- Bibliothèque Pillow (`PIL`)

Installation de Pillow :

```bash
pip install Pillow
```

Modules utilisés :

- `sys`
- `os`
- `re`
- `PIL`

## Structure du projet

```text
projet/
├── comptages.py
├── images_test/
└── listePhotos.csv
```

- `comptages.py` : script principal.
- `images_test/` : dossier contenant les photos à classer.
- `listePhotos.csv` : fichier généré après l’exécution.

## Exécution

1. Placer les photos à classer dans le dossier `images_test/`.
2. Ouvrir un terminal dans le répertoire contenant `comptages.py`.
3. Lancer le script en passant le dossier de photos en paramètre.

Si vous êtes déjà dans le dossier `images_test/` :

```bash
python3 comptages.py .
```

Sinon :

```bash
python3 comptages.py /chemin/vers/images_test
```

## Résultat attendu

Après l’exécution, le script :

- crée des dossiers par année ;
- crée des sous-dossiers par mois ;
- déplace les photos dans les bons dossiers ;
- génère un fichier `listePhotos.csv` trié chronologiquement.