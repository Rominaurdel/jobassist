"""
Configuration et chargement des clés API
"""

import os
import sys

# Load environment variables
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False


def load_api_keys():
    """Charge les clés API depuis les variables d'environnement ou le fichier .env"""
    # Charger depuis .env si disponible
    if DOTENV_AVAILABLE:
        load_dotenv()
    
    perplexity_key = os.getenv('PERPLEXITY_KEY')
    gemini_key = os.getenv('GEMINI_KEY')
    
    if not perplexity_key or not gemini_key:
        print("❌ Erreur: Les clés API ne sont pas configurées!")
        print("\n📝 Configuration requise:")
        print("   Créez un fichier .env à la racine du projet avec:")
        print("   PERPLEXITY_KEY=pplx_votre_cle")
        print("   GEMINI_KEY=AIza_votre_cle")
        print("\n   Ou définissez les variables d'environnement:")
        print("   export PERPLEXITY_KEY=pplx_votre_cle")
        print("   export GEMINI_KEY=AIza_votre_cle")
        print("\n   Pour obtenir vos clés API:")
        print("   - Perplexity: https://www.perplexity.ai/")
        print("   - Gemini: https://ai.google.dev/")
        sys.exit(1)
    
    return perplexity_key, gemini_key
