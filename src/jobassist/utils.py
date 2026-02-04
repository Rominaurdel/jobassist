"""
Utilitaires : loader, nettoyage Markdown, etc.
"""

import time
import threading
import re


class Loader:
    """Afficheur de loader animé"""
    
    FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    def __init__(self, message: str = "Traitement en cours"):
        self.message = message
        self.stop_event = threading.Event()
        self.thread = None
    
    def _animate(self):
        """Animation du loader"""
        i = 0
        while not self.stop_event.is_set():
            print(f"\r{self.FRAMES[i % len(self.FRAMES)]} {self.message}", end='', flush=True)
            i += 1
            time.sleep(0.1)
        print(f"\r{' ' * (len(self.message) + 2)}\r", end='', flush=True)
    
    def start(self):
        """Démarre le loader"""
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Arrête le loader"""
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=1)


def clean_markdown(text: str) -> str:
    """Nettoie le texte en enlevant les symboles Markdown"""
    # Enlever les références [1], [2], etc.
    text = re.sub(r'\[\d+\]', '', text)
    # Enlever les liens markdown [texte](url)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Enlever le gras **texte** ou __texte__ (gérer les cas multiples)
    text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    # Enlever l'italique *texte* ou _texte_ (mais pas les astérisques seuls)
    text = re.sub(r'(?<!\*)\*([^\*\n]+)\*(?!\*)', r'\1', text)
    text = re.sub(r'(?<!_)_([^_\n]+)_(?!_)', r'\1', text)
    # Enlever les titres ### Titre, ## Titre, # Titre
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # Enlever les listes numérotées 1. 2. etc. (garder juste le contenu)
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)
    # Enlever les puces - * + (mais garder le contenu)
    text = re.sub(r'^[-*+]\s+', '', text, flags=re.MULTILINE)
    # Enlever les blocs de code ```
    text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Enlever les tableaux markdown | | | (remplacer par espaces)
    text = re.sub(r'\s*\|\s*', ' ', text)
    # Enlever les lignes de séparation --- ou ===
    text = re.sub(r'^[-=]{3,}$', '', text, flags=re.MULTILINE)
    # Enlever les caractères spéciaux markdown restants
    text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)  # Citations
    # Nettoyer les espaces multiples (mais garder les retours à la ligne)
    text = re.sub(r'[ \t]+', ' ', text)
    # Nettoyer les espaces en début/fin de ligne
    text = '\n'.join(line.strip() for line in text.split('\n'))
    # Nettoyer les lignes vides multiples (max 2 consécutives)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Nettoyer les espaces en début/fin de texte
    return text.strip()
