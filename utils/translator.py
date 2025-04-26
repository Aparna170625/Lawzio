import os
import json
from googletrans import Translator
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL_NAME = "gpt-4o"

class TranslationHelper:
    def __init__(self):
        """Initialize translation helper with Google Translate and OpenAI backup"""
        self.google_translator = Translator()
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.openai_client = OpenAI(api_key=api_key)
        else:
            self.openai_client = None
        
        # Supported languages
        self.languages = {
            "english": "en",
            "hindi": "hi",
            "tamil": "ta"
        }
    
    def translate_text(self, text, target_language):
        """
        Translate text to the target language
        
        Args:
            text (str): Text to translate
            target_language (str): Target language name (english, hindi, tamil)
            
        Returns:
            str: Translated text
        """
        if not text:
            return ""
        
        if target_language.lower() not in self.languages:
            raise ValueError(f"Unsupported language: {target_language}. Supported languages are: {', '.join(self.languages.keys())}")
        
        lang_code = self.languages[target_language.lower()]
        
        # Try Google Translate first
        try:
            # If already in target language, return as is
            if (target_language.lower() == "english" and self._is_english(text)):
                return text
                
            result = self.google_translator.translate(text, dest=lang_code)
            return result.text
        except Exception as e:
            # Fallback to OpenAI if Google Translate fails
            if self.openai_client:
                try:
                    return self._translate_with_openai(text, target_language)
                except Exception as openai_error:
                    raise Exception(f"Translation failed: {str(e)}. OpenAI fallback also failed: {str(openai_error)}")
            else:
                raise Exception(f"Translation failed: {str(e)}. OpenAI fallback not available.")
    
    def _translate_with_openai(self, text, target_language):
        """Use OpenAI for translation as a fallback"""
        response = self.openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": f"You are a translator. Translate the following text to {target_language}."},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    
    def _is_english(self, text):
        """Simple check if text is primarily English"""
        # Sample first 100 characters to detect language
        sample = text[:100].lower()
        english_chars = set("abcdefghijklmnopqrstuvwxyz .,;:!?'\"()-")
        non_english_chars = [c for c in sample if c not in english_chars and not c.isdigit()]
        
        # If more than 15% non-English characters, assume it's not English
        return len(non_english_chars) / max(1, len(sample)) < 0.15
