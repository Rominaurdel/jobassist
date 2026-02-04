# 🤖 JobAssist - Agent IA d'Adaptation de CV

Outil Python intelligent qui adapte automatiquement votre CV à chaque offre d'emploi en utilisant **Perplexity AI** et **Google Gemini**. Analyse l'offre, identifie les compétences clés, réécrit votre CV de manière optimale et calcule un score de pertinence.

## ✨ Fonctionnalités

✅ **Mode interactif** - Copie-colle l'offre directement dans la console  
✅ **Extraction PDF/TXT** - Lit votre CV en PDF ou texte  
✅ **Analyse IA** - Perplexity analyse l'offre d'emploi (compétences, responsabilités)  
✅ **Adaptation intelligente** - Gemini adapte votre CV pour matcher l'offre  
✅ **Génération PDF** - Export automatique en PDF professionnel (format par défaut)  
✅ **Nettoyage automatique** - Suppression des symboles Markdown (###, **, [1], etc.) pour un CV propre  
✅ **Scoring** - Calcule le score de pertinence (0-100%)  
✅ **Template Word** - Export avec mise en page préservée (optionnel)  
✅ **Rapide** - ~30-45 secondes par adaptation

## 📦 Installation

### Étape 1 : Cloner le projet

```bash
git clone https://github.com/rominaurdel/jobassist.git
cd jobassist
```

### Étape 2 : Installer le package

**⚠️ Important : Exécutez cette commande depuis la racine du projet (où se trouve `setup.py`)**

```bash
# Installer le package et ses dépendances en mode développement
pip install -e .
```

Cette commande :
- Installe toutes les dépendances depuis `requirements.txt`
- Installe le package `jobassist` en mode éditable
- Permet d'utiliser `python -m jobassist` depuis n'importe où

**Alternative : Installation manuelle (si pip install -e ne fonctionne pas)**

```bash
# Installer uniquement les dépendances
pip install -r requirements.txt

# Puis utiliser le chemin direct
python -m src.jobassist.cli -i
```

### Étape 3 : Configurer les clés API

Créez un fichier `.env` à la racine du projet :

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

Puis éditez `.env` avec vos clés API (voir section Configuration ci-dessous).

### Utilisation

Une fois installé, vous pouvez utiliser JobAssist depuis n'importe quel répertoire :

```bash
# Mode interactif
python -m jobassist -i

# Ou avec arguments
python -m jobassist --cv CV.pdf --job-offer offre.txt
```

**Important** : Assurez-vous d'être dans un environnement où le package est installé, ou exécutez depuis la racine du projet après installation.

## 🔐 Configuration des clés API

**IMPORTANT** : Les clés API doivent être configurées dans un fichier `.env` (jamais dans le code source).

### Étape 1 : Créer le fichier .env

Créez un fichier `.env` à la racine du projet :

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

### Étape 2 : Remplir vos clés API

Éditez le fichier `.env` et remplacez les valeurs par vos clés :

```env
PERPLEXITY_KEY=pplx_votre_cle_perplexity
GEMINI_KEY=AIza_votre_cle_gemini
```

### Où obtenir vos clés API ?

- **Perplexity** : https://www.perplexity.ai/ → Créez un compte et obtenez votre clé API
- **Google Gemini** : https://ai.google.dev/ → Créez un projet et obtenez votre clé API

### Alternative : Variables d'environnement système

Vous pouvez aussi définir les clés comme variables d'environnement :

```powershell
# Windows PowerShell
$env:PERPLEXITY_KEY="pplx_votre_cle"
$env:GEMINI_KEY="AIza_votre_cle"
```

```bash
# Linux/Mac
export PERPLEXITY_KEY="pplx_votre_cle"
export GEMINI_KEY="AIza_votre_cle"
```

⚠️ **Sécurité** : Le fichier `.env` est automatiquement ignoré par Git (voir `.gitignore`). Ne commitez jamais vos clés API !

## 🚀 Utilisation

### Mode interactif (Recommandé) 🎯

Le mode interactif te permet de copier-coller l'offre d'emploi directement dans la console :

```bash
python -m jobassist -i
```

Ou simplement (c'est le mode par défaut) :

```bash
python -m jobassist
```

**Flux interactif :**
```
🤖 Agent IA - Adaptation CV (Mode Interactif)

🔑 Clé API Perplexity (pplx_...): [rentre ta clé]
🔑 Clé API Gemini (AIza-...): [rentre ta clé]

📄 Chemin du CV (PDF ou TXT): mon_cv.pdf

📋 Collez l'offre d'emploi (Ctrl+D ou Ctrl+Z + Entrée pour terminer):
[Copie-colle l'offre ici]
[Appuie sur Ctrl+D (Mac/Linux) ou Ctrl+Z + Entrée (Windows)]

💡 Instructions additionnelles (optionnel, appuyez sur Entrée si rien):
[Ajoute des instructions ou appuie sur Entrée]

📝 Utiliser un template Word? (laisser vide pour non): [optionnel]

📤 Chemin de sortie (défaut: CV_Adapte.pdf): [optionnel]
```

### Mode CLI classique (fichier offre)

Si tu préfères garder l'offre dans un fichier `.txt` :

```bash
python -m jobassist \
  --cv "mon_cv.pdf" \
  --job-offer "offre.txt" \
  --output "CV_Adapte.pdf"
```

### Avec template Word (mise en page préservée)

En mode interactif :

```bash
python -m jobassist -i
# Puis fournir le template quand demandé
```

En mode CLI :

```bash
python -m jobassist \
  --cv "mon_cv.pdf" \
  --job-offer "offre.txt" \
  --template "template_cv.docx" \
  --output "CV_Adapte.docx"
```

## 📋 Arguments CLI

| Argument | Requis | Description |
|----------|--------|-------------|
| `-i, --interactive` | ❌ | Mode interactif (défaut si pas d'autres args) |
| `--cv` | ✅ (CLI) | Chemin du CV (PDF ou TXT) |
| `--job-offer` | ✅ (CLI) | Chemin de l'offre d'emploi (TXT) |
| `--template` | ❌ | Chemin du template Word (.docx) |
| `--output` | ❌ | Chemin du fichier résultat (défaut: `CV_Adapte.pdf`) |
| `--instructions` | ❌ | Instructions additionnelles |

## 📁 Structure de fichiers

```
jobassist/
├── src/
│   └── jobassist/        # Code source principal
│       ├── __init__.py
│       ├── adapter.py    # Classe CVAdapter principale
│       ├── api_client.py # Clients API Perplexity/Gemini
│       ├── config.py     # Configuration et chargement des clés
│       ├── pdf_generator.py # Génération PDF
│       ├── utils.py      # Utilitaires (loader, nettoyage)
│       ├── cli.py        # Interface en ligne de commande
│       └── __main__.py   # Point d'entrée module
├── docs/                # Documentation
│   └── API.md
├── scripts/             # Scripts utilitaires
│   └── make_template.py # Création de templates Word
├── requirements.txt      # Dépendances Python
├── setup.py             # Installation package
├── .env.example          # Template de configuration
├── .gitignore           # Fichiers ignorés par Git
├── LICENSE              # Licence MIT
├── CONTRIBUTING.md      # Guide de contribution
└── README.md            # Ce fichier
```

## 🔧 Préparation du template Word

Si tu veux utiliser la mise en page de ton CV original :

1. **Ouvre Microsoft Word** (ou LibreOffice)
2. **Crée un template** avec la mise en page souhaitée
3. **Place un placeholder** pour le contenu du CV :
   ```
   {{ cv_content }}
   ```
4. **Sauvegarde** en `.docx`

Example template structure:
```
┌─────────────────────────────┐
│ NOM - PRÉNOM                │
│ 123 Rue de Paris | 75000    │
├─────────────────────────────┤
│ {{ cv_content }}            │
└─────────────────────────────┘
```

## 📊 Résultats

Le script affiche :

```
📄 Extraction du PDF: mon_cv.pdf...
🔍 Analyse de l'offre d'emploi avec Perplexity...
✍️  Adaptation du CV avec Gemini...
📊 Calcul du score de pertinence...
📝 Génération du PDF

✅ CV adapté sauvegardé: CV_Adapte.pdf
📈 Score de pertinence: 87%

🎯 Analyse:
1. Compétences techniques requises:
   - Next.js, React
   - Node.js, PostgreSQL
   ...
```

**Note:** Le CV généré est automatiquement nettoyé de tous les symboles Markdown (###, **, [1], etc.) pour un rendu professionnel.

## 🔐 Sécurité des clés API

**Ne commit pas tes clés API !** Utilise des variables d'environnement :

Le fichier `.env` est déjà configuré si vous avez suivi les étapes d'installation ci-dessus.

## 🐛 Troubleshooting

### Erreur: "pypdf not installed"
```bash
pip install pypdf
```

### Erreur: "python-docx-template not installed"
```bash
pip install python-docx-template
```

### Erreur: "reportlab not installed"
```bash
pip install reportlab
```

### Erreur: "No module named jobassist"

Cette erreur signifie que le package n'est pas installé. Solutions :

**Solution 1 : Installer le package (recommandé)**
```bash
# Depuis la racine du projet (où se trouve setup.py)
cd "c:\Users\Romain\Dev projects\jobassist"
pip install -e .
```

**Solution 2 : Exécuter depuis la racine du projet**
```bash
# Assurez-vous d'être dans la racine du projet, pas dans src/jobassist
cd "c:\Users\Romain\Dev projects\jobassist"
python -m jobassist -i
```

**Solution 3 : Utiliser le chemin direct (sans installation)**
```bash
# Depuis la racine du projet
python -m src.jobassist.cli -i
```

### Erreur Perplexity/Gemini: "Unauthorized"
- Vérifie que les clés API sont correctes
- Assure-toi qu'elles n'ont pas expiré
- Vérifie tes quotas sur la console de chaque service

### Problème avec Ctrl+D (Windows)
Sur Windows, utilise **Ctrl+Z** puis **Entrée** pour terminer l'input.

### Le template Word ne fonctionne pas
- Assure-toi que le fichier est en `.docx` (pas `.docm` ou `.doc`)
- Vérifie que le placeholder `{{ cv_content }}` existe dans le document

## 💡 Conseils d'usage

### 1. Première utilisation (mode interactif)

```bash
python -m jobassist
# Remplis les infos demandées
# Copie-colle l'offre depuis LinkedIn/Indeed/etc
# Reçois ton CV adapté !
```

### 2. Batch processing (plusieurs offres)

Crée un dossier `offres/` avec toutes les offres en `.txt` :

```powershell
# PowerShell (Windows)
$offers = Get-ChildItem "offres\*.txt"

foreach ($offer in $offers) {
    $filename = [System.IO.Path]::GetFileNameWithoutExtension($offer.Name)
    Write-Host "Traitement de $filename..."
    python -m jobassist `
        --cv "mon_cv.pdf" `
        --job-offer $offer.FullName `
        --output "resultats\${filename}_adapte.pdf"
}
```

### 3. Workflow quotidien

1. Vois une offre intéressante → Copie le texte
2. Lance `python -m jobassist`
3. Colle l'offre → Reçois le CV adapté en PDF en 30 secondes
4. Le CV est automatiquement nettoyé (pas de symboles Markdown)
5. Envoie le CV ! 🚀

## 📈 Coûts API estimés

- **Perplexity** : ~0.01-0.03€ par adaptation (modèle sonar-pro)
- **Gemini** : ~0.0005-0.002€ par adaptation (gemini-2.5-flash)
- **Total** : ~0.02€ par CV adapté

Pour 100 candidatures : ~2€ seulement ! 🎯

## 🤝 Support

Pour les bugs ou questions :
1. Vérifie les logs du script
2. Teste chaque API séparément
3. Consulte la documentation : 
   - Perplexity: https://docs.perplexity.ai
   - Gemini: https://ai.google.dev

---

**Happy job hunting!** 🚀
