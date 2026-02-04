"""
Classe principale CVAdapter pour l'adaptation de CV
"""

import sys
from pathlib import Path
from typing import Optional

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    from docxtpl import DocxTemplate
except ImportError:
    DocxTemplate = None

from .api_client import PerplexityClient, GeminiClient
from .pdf_generator import generate_pdf
from .utils import Loader


class CVAdapter:
    """Adaptateur CV utilisant Perplexity et Gemini"""
    
    def __init__(self, perplexity_key: str, gemini_key: str):
        """Initialise l'adaptateur CV"""
        self.perplexity_client = PerplexityClient(perplexity_key)
        self.gemini_client = GeminiClient(gemini_key)
        self.gemini_available = True
        self._test_api_connections()
    
    def _test_api_connections(self):
        """Test la connexion aux APIs"""
        print("\n🔐 Vérification des clés API et connexions...\n")
        
        # Test Perplexity
        loader = Loader("Vérification Perplexity API")
        loader.start()
        try:
            import requests
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    'Authorization': f'Bearer {self.perplexity_client.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'sonar-pro',
                    'messages': [{'role': 'user', 'content': 'test'}]
                },
                timeout=10
            )
            loader.stop()
            
            if response.status_code == 401:
                print("❌ Erreur Perplexity: Clé API invalide")
                sys.exit(1)
            elif response.status_code == 429:
                print("⚠️  Perplexity: Quota atteint")
                sys.exit(1)
            elif response.status_code == 200:
                print("✅ Perplexity API: OK")
            else:
                print(f"⚠️  Perplexity: Statut {response.status_code}")
        except Exception as e:
            loader.stop()
            print(f"❌ Erreur Perplexity: {str(e)[:100]}")
            sys.exit(1)
        
        # Test Gemini
        loader = Loader("Vérification Gemini API")
        loader.start()
        self.gemini_available = True
        try:
            import requests
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.gemini_client.api_key}",
                headers={'Content-Type': 'application/json'},
                json={
                    'contents': [{'role': 'user', 'parts': [{'text': 'test'}]}]
                },
                timeout=10
            )
            loader.stop()
            
            if response.status_code == 401 or 'INVALID_ARGUMENT' in response.text:
                print("❌ Erreur Gemini: Clé API invalide")
                sys.exit(1)
            elif response.status_code == 429:
                print("⚠️  Gemini: Quota atteint - utilisation exclusive de Perplexity")
                self.gemini_available = False
            elif response.status_code == 200:
                print("✅ Gemini API: OK")
                self.gemini_available = True
            elif response.status_code == 503:
                print("⚠️  Gemini: Overloadé (fallback sur Perplexity)")
                self.gemini_available = False
            else:
                print(f"⚠️  Gemini: Statut {response.status_code}")
                self.gemini_available = False
        except Exception as e:
            loader.stop()
            print(f"❌ Erreur Gemini: {str(e)[:100]}")
            sys.exit(1)
        
        print("\n✅ Configuration complète!\n")
    
    def extract_pdf_text(self, pdf_path: str) -> str:
        """Extrait le texte d'un PDF"""
        if not PdfReader:
            raise ImportError("pypdf not installed. Run: pip install -r requirements.txt")
        
        print(f"📄 Extraction du PDF: {pdf_path}...")
        reader = PdfReader(pdf_path)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        return text
    
    def extract_text_file(self, txt_path: str) -> str:
        """Extrait le texte d'un fichier .txt"""
        print(f"📄 Lecture du fichier: {txt_path}...")
        with open(txt_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_cv(self, cv_path: str) -> str:
        """Charge le CV (PDF ou TXT)"""
        ext = Path(cv_path).suffix.lower()
        
        if ext == '.pdf':
            return self.extract_pdf_text(cv_path)
        elif ext == '.txt':
            return self.extract_text_file(cv_path)
        else:
            raise ValueError(f"Format non supporté: {ext}. Utilisez PDF ou TXT.")
    
    def analyze_job_offer(self, job_offer: str) -> str:
        """Analyse l'offre d'emploi avec Perplexity"""
        loader = Loader("🔍 Analyse de l'offre d'emploi")
        loader.start()
        try:
            result = self.perplexity_client.analyze_job_offer(job_offer)
            loader.stop()
            return result
        except Exception as e:
            loader.stop()
            raise e
    
    def adapt_cv(self, cv_text: str, job_offer: str, analysis: str, instructions: Optional[str] = None) -> str:
        """Adapte le CV: essaye Gemini, fallback sur Perplexity si quota/overload"""
        
        # Si Gemini n'est pas disponible, utiliser directement Perplexity
        if not self.gemini_available:
            loader = Loader("✍️  Adaptation du CV (Perplexity)")
            loader.start()
            try:
                result = self.perplexity_client.adapt_cv(cv_text, job_offer, analysis, instructions)
                loader.stop()
                return result
            except Exception as e:
                loader.stop()
                raise e
        
        # Sinon, essayer Gemini d'abord
        loader = Loader("✍️  Adaptation du CV (Gemini)")
        loader.start()
        
        try:
            result = self.gemini_client.adapt_cv(cv_text, job_offer, analysis, instructions)
            
            if result is None:
                # Gemini overloadé (503) ou quota (429), basculer sur Perplexity
                loader.stop()
                loader = Loader("✍️  Adaptation du CV (Perplexity - fallback)")
                loader.start()
                result = self.perplexity_client.adapt_cv(cv_text, job_offer, analysis, instructions)
            
            loader.stop()
            return result
            
        except Exception as e:
            loader.stop()
            # Si Gemini échoue pour une autre raison, essayer Perplexity
            print(f"⚠️  Gemini indisponible, utilisation de Perplexity...")
            loader = Loader("✍️  Adaptation du CV (Perplexity - fallback)")
            loader.start()
            try:
                result = self.perplexity_client.adapt_cv(cv_text, job_offer, analysis, instructions)
                loader.stop()
                return result
            except Exception as e2:
                loader.stop()
                raise e2
    
    def calculate_score(self, adapted_cv: str, job_offer: str) -> int:
        """Calcule le score: essaye Gemini, fallback sur Perplexity"""
        
        # Si Gemini n'est pas disponible, utiliser directement Perplexity
        if not self.gemini_available:
            loader = Loader("📊 Calcul du score (Perplexity)")
            loader.start()
            try:
                score = self.perplexity_client.calculate_score(adapted_cv, job_offer)
                loader.stop()
                
                if score is None:
                    print("⚠️  Score non disponible")
                    return 0
                return score
            except Exception as e:
                loader.stop()
                print(f"⚠️  Score non disponible: {str(e)[:100]}")
                return 0
        
        # Sinon, essayer Gemini d'abord
        loader = Loader("📊 Calcul du score (Gemini)")
        loader.start()
        
        try:
            score = self.gemini_client.calculate_score(adapted_cv, job_offer)
            
            if score is None:
                # Gemini overloadé ou erreur, basculer sur Perplexity
                loader.stop()
                loader = Loader("📊 Calcul du score (Perplexity - fallback)")
                loader.start()
                score = self.perplexity_client.calculate_score(adapted_cv, job_offer)
            
            loader.stop()
            
            if score is None:
                print("⚠️  Score non disponible")
                return 0
            
            return score
            
        except Exception as e:
            loader.stop()
            print(f"⚠️  Score non disponible: {str(e)[:100]}")
            return 0
    
    def generate_adapted_cv(self, 
                          cv_path: str, 
                          job_offer_path: str, 
                          output_path: str = "CV_Adapte.pdf",
                          instructions: Optional[str] = None) -> dict:
        """Génère le CV adapté complet (offre depuis fichier)"""
        
        cv_text = self.load_cv(cv_path)
        
        with open(job_offer_path, 'r', encoding='utf-8') as f:
            job_offer = f.read()
        
        analysis = self.analyze_job_offer(job_offer)
        adapted_cv = self.adapt_cv(cv_text, job_offer, analysis, instructions)
        score = self.calculate_score(adapted_cv, job_offer)
        
        # Générer PDF par défaut
        if output_path.endswith('.pdf'):
            loader = Loader("📝 Génération du PDF")
            loader.start()
            try:
                generate_pdf(adapted_cv, output_path)
                loader.stop()
            except Exception as e:
                loader.stop()
                raise e
        else:
            # Fallback sur TXT si extension différente
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(adapted_cv)
        
        print(f"\n✅ CV adapté sauvegardé: {output_path}")
        print(f"📈 Score de pertinence: {score}%")
        
        return {
            'cv': adapted_cv,
            'analysis': analysis,
            'score': score,
            'output_file': output_path
        }
    
    def generate_adapted_cv_direct(self, 
                                   cv_path: str, 
                                   job_offer: str,
                                   output_path: str = "CV_Adapte.pdf",
                                   instructions: Optional[str] = None) -> dict:
        """Génère le CV adapté avec l'offre passée directement (pas de fichier)"""
        
        cv_text = self.load_cv(cv_path)
        
        analysis = self.analyze_job_offer(job_offer)
        adapted_cv = self.adapt_cv(cv_text, job_offer, analysis, instructions)
        score = self.calculate_score(adapted_cv, job_offer)
        
        # Générer PDF par défaut
        if output_path.endswith('.pdf'):
            loader = Loader("📝 Génération du PDF")
            loader.start()
            try:
                generate_pdf(adapted_cv, output_path)
                loader.stop()
            except Exception as e:
                loader.stop()
                raise e
        else:
            # Fallback sur TXT si extension différente
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(adapted_cv)
        
        print(f"\n✅ CV adapté sauvegardé: {output_path}")
        print(f"📈 Score de pertinence: {score}%")
        
        return {
            'cv': adapted_cv,
            'analysis': analysis,
            'score': score,
            'output_file': output_path
        }
    
    def generate_with_template(self,
                              cv_path: str,
                              job_offer: str,
                              template_path: str,
                              output_path: str = "CV_Adapte.docx",
                              instructions: Optional[str] = None) -> dict:
        """Génère le CV adapté en préservant la mise en page du template Word"""
        
        if not DocxTemplate:
            raise ImportError("docxtpl not installed. Run: pip install -r requirements.txt")
        
        cv_text = self.load_cv(cv_path)
        
        analysis = self.analyze_job_offer(job_offer)
        adapted_cv = self.adapt_cv(cv_text, job_offer, analysis, instructions)
        score = self.calculate_score(adapted_cv, job_offer)
        
        loader = Loader("📝 Création du document Word")
        loader.start()
        try:
            tpl = DocxTemplate(template_path)
            context = {'cv_content': adapted_cv}
            tpl.render(context)
            tpl.save(output_path)
            loader.stop()
        except Exception as e:
            loader.stop()
            raise e
        
        print(f"\n✅ CV adapté sauvegardé: {output_path}")
        print(f"📈 Score de pertinence: {score}%")
        
        return {
            'cv': adapted_cv,
            'analysis': analysis,
            'score': score,
            'output_file': output_path
        }
