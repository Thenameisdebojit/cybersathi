"""
Internationalization (i18n) Module for CyberSathi
Supports English (en) and Odia (od) languages
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional


class I18nService:
    """
    Service for managing multilingual content.
    Loads and provides translations for English and Odia languages.
    """
    
    def __init__(self):
        self.translations: Dict[str, Dict] = {}
        self.default_language = "en"
        self.supported_languages = ["en", "od"]
        self._load_translations()
    
    def _load_translations(self):
        """Load all translation files from the i18n directory."""
        i18n_dir = Path(__file__).parent
        
        for lang in self.supported_languages:
            file_path = i18n_dir / f"{lang}.json"
            
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.translations[lang] = json.load(f)
                except Exception as e:
                    print(f"Error loading {lang}.json: {e}")
                    self.translations[lang] = {}
            else:
                print(f"Translation file not found: {file_path}")
                self.translations[lang] = {}
    
    def get(self, key: str, language: str = "en", **kwargs) -> str:
        """
        Get translated text by key.
        
        Args:
            key: Dot-notation key (e.g., "greeting.welcome")
            language: Language code (en, od)
            **kwargs: Variables to format into the translation
            
        Returns:
            Translated and formatted text
        """
        if language not in self.supported_languages:
            language = self.default_language
        
        keys = key.split('.')
        translation = self.translations.get(language, {})
        
        for k in keys:
            if isinstance(translation, dict):
                translation = translation.get(k)
            else:
                break
        
        if translation is None or not isinstance(translation, str):
            translation = self.translations.get(self.default_language, {})
            for k in keys:
                if isinstance(translation, dict):
                    translation = translation.get(k)
                else:
                    break
        
        if isinstance(translation, str):
            try:
                return translation.format(**kwargs)
            except KeyError:
                return translation
        
        return key
    
    def detect_language(self, text: str) -> str:
        """
        Detect language from user input.
        Simple detection based on character sets and keywords.
        
        Args:
            text: User input text
            
        Returns:
            Detected language code
        """
        if not text:
            return self.default_language
        
        odia_chars = any(char in text for char in 'ଅଆଇଈଉଊଋଏଐଓଔକଖଗଘଙଚଛଜଝଞଟଠଡଢଣତଥଦଧନପଫବଭମଯରଲଳଵଶଷସହୟ')
        if odia_chars:
            return "od"
        
        odia_keywords = ['ନମସ୍କାର', 'ସାହାଯ୍ୟ', 'ରିପୋର୍ଟ', 'ଅଭିଯୋଗ']
        if any(keyword in text for keyword in odia_keywords):
            return "od"
        
        return "en"
    
    def get_all(self, language: str = "en") -> Dict:
        """
        Get all translations for a specific language.
        
        Args:
            language: Language code
            
        Returns:
            Dictionary of all translations
        """
        return self.translations.get(language, {})


i18n = I18nService()
