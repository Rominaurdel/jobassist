# Documentation API

## CVAdapter

Classe principale pour l'adaptation de CV.

### Initialisation

```python
from jobassist import CVAdapter, load_api_keys

perplexity_key, gemini_key = load_api_keys()
adapter = CVAdapter(perplexity_key, gemini_key)
```

### Méthodes principales

#### `load_cv(cv_path: str) -> str`
Charge un CV depuis un fichier PDF ou TXT.

#### `analyze_job_offer(job_offer: str) -> str`
Analyse une offre d'emploi et extrait les éléments clés.

#### `adapt_cv(cv_text: str, job_offer: str, analysis: str, instructions: Optional[str] = None) -> str`
Adapte un CV à une offre d'emploi.

#### `calculate_score(adapted_cv: str, job_offer: str) -> int`
Calcule un score de pertinence (0-100).

#### `generate_adapted_cv_direct(cv_path: str, job_offer: str, output_path: str = "CV_Adapte.pdf", instructions: Optional[str] = None) -> dict`
Génère un CV adapté complet avec l'offre passée directement.

#### `generate_with_template(cv_path: str, job_offer: str, template_path: str, output_path: str = "CV_Adapte.docx", instructions: Optional[str] = None) -> dict`
Génère un CV adapté avec un template Word.
