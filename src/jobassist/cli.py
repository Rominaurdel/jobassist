"""
Interface en ligne de commande pour JobAssist
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from .adapter import CVAdapter
from .config import load_api_keys


def get_job_offer_from_console() -> str:
    """Récupère l'offre d'emploi depuis la console"""
    print("\n📋 Collez l'offre d'emploi:")
    print("   (Appuyez 2x sur Entrée quand vous avez terminé)\n")
    
    lines = []
    empty_line_count = 0
    
    try:
        while True:
            line = input()
            
            if line.strip() == "":
                empty_line_count += 1
                if empty_line_count >= 2:
                    lines = lines[:-1] if lines else []
                    break
            else:
                empty_line_count = 0
                lines.append(line)
    except EOFError:
        pass
    
    return '\n'.join(lines)


def interactive_mode():
    """Mode interactif avec input console"""
    print("🤖 Agent IA - Adaptation CV (Mode Interactif)\n")
    
    perplexity_key, gemini_key = load_api_keys()
    adapter = CVAdapter(perplexity_key, gemini_key)
    
    cv_path = input("📄 Chemin du CV (PDF ou TXT): ").strip()
    if not Path(cv_path).exists():
        print(f"❌ Erreur: {cv_path} n'existe pas")
        sys.exit(1)
    
    job_offer = get_job_offer_from_console()
    if not job_offer.strip():
        print("❌ L'offre d'emploi est vide")
        sys.exit(1)
    
    print("\n💡 Instructions additionnelles (appuyez sur Entrée si rien):")
    instructions = input().strip() or None
    
    print("\n📝 Utiliser un template Word? (appuyez sur Entrée si non): ", end='')
    template = input().strip() or None
    
    if template and not Path(template).exists():
        print(f"❌ Erreur: {template} n'existe pas")
        sys.exit(1)
    
    if template:
        default_output = "CV_Adapte.docx"
        print(f"📤 Chemin de sortie (défaut: {default_output}): ", end='')
    else:
        default_output = "CV_Adapte.pdf"
        print(f"📤 Chemin de sortie (défaut: {default_output}): ", end='')
    
    output = input().strip() or default_output
    
    try:
        if template:
            result = adapter.generate_with_template(
                cv_path,
                job_offer,
                template,
                output,
                instructions
            )
        else:
            result = adapter.generate_adapted_cv_direct(
                cv_path,
                job_offer,
                output,
                instructions
            )
        
        print(f"\n🎯 Analyse:\n{result['analysis']}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(
        description="JobAssist - Agent IA d'adaptation de CV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  # Mode interactif
  python -m jobassist -i
  
  # Avec fichiers
  python -m jobassist --cv CV.pdf --job-offer offre.txt
  
  # Avec template Word
  python -m jobassist --cv CV.pdf --job-offer offre.txt --template template.docx
        """
    )
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Mode interactif (défaut si pas d\'autres args)')
    parser.add_argument('--cv', help='Chemin du CV (PDF ou TXT)')
    parser.add_argument('--job-offer', help='Chemin de l\'offre d\'emploi (TXT)')
    parser.add_argument('--template', help='Chemin du template Word (.docx)')
    parser.add_argument('--output', help='Chemin du fichier de sortie')
    parser.add_argument('--instructions', help='Instructions additionnelles')
    
    args = parser.parse_args()
    
    if args.interactive or (not args.cv and not args.job_offer):
        interactive_mode()
        return
    
    if not args.cv or not args.job_offer:
        print("❌ Arguments manquants.")
        sys.exit(1)
    
    if not Path(args.cv).exists() or not Path(args.job_offer).exists():
        print("❌ Fichiers non trouvés")
        sys.exit(1)
    
    if args.template and not Path(args.template).exists():
        print(f"❌ Erreur: {args.template} n'existe pas")
        sys.exit(1)
    
    perplexity_key, gemini_key = load_api_keys()
    adapter = CVAdapter(perplexity_key, gemini_key)
    output = args.output or ('CV_Adapte.docx' if args.template else 'CV_Adapte.pdf')
    
    try:
        if args.template:
            with open(args.job_offer, encoding='utf-8') as f:
                job_offer = f.read()
            result = adapter.generate_with_template(
                args.cv, job_offer, args.template, output, args.instructions
            )
        else:
            result = adapter.generate_adapted_cv(
                args.cv, args.job_offer, output, args.instructions
            )
        
        print(f"\n🎯 Analyse:\n{result['analysis']}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
