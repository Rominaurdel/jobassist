"""
Clients API pour Perplexity et Gemini
"""

import requests
from typing import Optional

# API Endpoints
PERPLEXITY_API = "https://api.perplexity.ai/chat/completions"
GEMINI_API = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


class PerplexityClient:
    """Client pour l'API Perplexity"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def analyze_job_offer(self, job_offer: str) -> str:
        """Analyse l'offre d'emploi avec Perplexity"""
        prompt = f"""Analyse cette offre d'emploi et extrais les éléments clés:
1. Compétences techniques requises
2. Compétences humaines
3. Années d'expérience
4. Secteur/domaine
5. Responsabilités principales

Offre d'emploi:
{job_offer}

Réponse (format structuré):"""
        
        response = requests.post(
            PERPLEXITY_API,
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'sonar-pro',
                'messages': [
                    {'role': 'system', 'content': 'Tu es un assistant expert en ressources humaines et CV.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.7,
                'max_tokens': 2000
            },
            timeout=120
        )
        
        if response.status_code != 200:
            raise Exception(f"Erreur Perplexity ({response.status_code}): {response.text[:200]}")
        
        return response.json()['choices'][0]['message']['content']
    
    def adapt_cv(self, cv_text: str, job_offer: str, analysis: str, instructions: Optional[str] = None) -> str:
        """Adapte le CV avec Perplexity"""
        prompt = f"""Tu es un expert en CV. Adapte ce CV à l'offre d'emploi suivante:

CV original:
{cv_text}

Offre d'emploi:
{job_offer}

Analyse clés:
{analysis}

{f'Instructions supplémentaires:\n{instructions}' if instructions else ''}

Instructions:
- Garde la structure du CV
- Mets en avant les compétences pertinentes
- Adapte les descriptions pour matcher l'offre
- Utilise les mots-clés de l'offre
- Sois concis et impactant

Fournit uniquement le CV adapté, sans explications additionnelles."""
        
        response = requests.post(
            PERPLEXITY_API,
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'sonar-pro',
                'messages': [
                    {'role': 'system', 'content': 'Tu es un expert en CV.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.7,
                'max_tokens': 3000
            },
            timeout=120
        )
        
        if response.status_code != 200:
            raise Exception(f"Erreur Perplexity ({response.status_code}): {response.text[:200]}")
        
        return response.json()['choices'][0]['message']['content']
    
    def calculate_score(self, adapted_cv: str, job_offer: str) -> Optional[int]:
        """Calcule le score de pertinence avec Perplexity"""
        prompt = f"""Sur une échelle de 0 à 100, quel est le score de pertinence entre ce CV et cette offre?
Réponds uniquement avec un nombre entre 0 et 100.

CV adapté:
{adapted_cv[:1000]}

Offre:
{job_offer[:1000]}"""
        
        try:
            response = requests.post(
                PERPLEXITY_API,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'sonar-pro',
                    'messages': [
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.3,
                    'max_tokens': 10
                },
                timeout=60
            )
            
            if response.status_code != 200:
                return None
            
            score_text = response.json()['choices'][0]['message']['content']
            import re
            match = re.search(r'\d+', score_text)
            score = int(match.group()) if match else 0
            return min(100, max(0, score))
        except Exception:
            return None


class GeminiClient:
    """Client pour l'API Gemini"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def adapt_cv(self, cv_text: str, job_offer: str, analysis: str, instructions: Optional[str] = None) -> Optional[str]:
        """Adapte le CV avec Gemini (retourne None si erreur 503/429)"""
        prompt = f"""Tu es un expert en CV. Adapte ce CV à l'offre d'emploi suivante:

CV original:
{cv_text}

Offre d'emploi:
{job_offer}

Analyse clés:
{analysis}

{f'Instructions supplémentaires:\n{instructions}' if instructions else ''}

Instructions:
- Garde la structure du CV
- Mets en avant les compétences pertinentes
- Adapte les descriptions pour matcher l'offre
- Utilise les mots-clés de l'offre
- Sois concis et impactant

Fournit uniquement le CV adapté, sans explications additionnelles."""
        
        try:
            response = requests.post(
                f"{GEMINI_API}?key={self.api_key}",
                headers={'Content-Type': 'application/json'},
                json={
                    'contents': [
                        {'role': 'user', 'parts': [{'text': prompt}]}
                    ],
                    'generationConfig': {
                        'temperature': 0.7,
                        'maxOutputTokens': 3000
                    }
                },
                timeout=120
            )
            
            # Si Gemini est overloadé (503) ou quota atteint (429), retourner None pour fallback
            if response.status_code == 503 or response.status_code == 429:
                return None
            
            if response.status_code != 200:
                error_msg = response.text[:200]
                try:
                    json_error = response.json()
                    if 'error' in json_error:
                        error_msg = json_error['error'].get('message', error_msg)
                except:
                    pass
                raise Exception(f"Erreur Gemini ({response.status_code}): {error_msg}")
            
            data = response.json()
            
            if 'candidates' not in data or not data['candidates']:
                raise Exception(f"Réponse Gemini invalide (pas de candidates)")
            
            candidate = data['candidates'][0]
            if 'content' not in candidate or 'parts' not in candidate['content']:
                raise Exception(f"Réponse Gemini invalide (structure)")
            
            return candidate['content']['parts'][0]['text']
        except Exception as e:
            if '503' in str(e) or '429' in str(e):
                return None
            raise e
    
    def calculate_score(self, adapted_cv: str, job_offer: str) -> Optional[int]:
        """Calcule le score de pertinence avec Gemini (retourne None si erreur)"""
        prompt = f"""Sur une échelle de 0 à 100, quel est le score de pertinence entre ce CV et cette offre?
Réponds uniquement avec un nombre entre 0 et 100.

CV adapté:
{adapted_cv[:1000]}

Offre:
{job_offer[:1000]}"""
        
        try:
            response = requests.post(
                f"{GEMINI_API}?key={self.api_key}",
                headers={'Content-Type': 'application/json'},
                json={
                    'contents': [
                        {'role': 'user', 'parts': [{'text': prompt}]}
                    ],
                    'generationConfig': {
                        'temperature': 0.3,
                        'maxOutputTokens': 10
                    }
                },
                timeout=60
            )
            
            # Si Gemini est overloadé ou quota atteint, retourner None pour fallback
            if response.status_code == 503 or response.status_code == 429:
                return None
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            
            if 'candidates' not in data or not data['candidates']:
                return None
            
            candidate = data['candidates'][0]
            if 'content' not in candidate or 'parts' not in candidate['content']:
                return None
            
            score_text = candidate['content']['parts'][0]['text']
            import re
            match = re.search(r'\d+', score_text)
            score = int(match.group()) if match else 0
            return min(100, max(0, score))
        except Exception:
            return None
