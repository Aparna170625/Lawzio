import os
import json
import re
import requests
from openai import OpenAI
from langdetect import detect, LangDetectException

# Import our direct translators
from utils.direct_translator import get_translator, TamilLegalTranslator, HindiLegalTranslator, BasicLegalTranslator

# Try to import IndicTranslator
try:
    from utils.indic_translator import IndicTranslator
    INDIC_TRANS_AVAILABLE = True
except Exception as e:
    print(f"IndicTrans not available: {e}")
    INDIC_TRANS_AVAILABLE = False

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL_NAME = "gpt-4o"

class TranslationHelper:
    def __init__(self):
        """Initialize translation helper with Google Translate and OpenAI backup"""
        # We no longer use the googletrans library due to coroutine issues
        # Instead we'll use direct API calls with requests
            
        # Check OpenAI API key
        self.openai_available = False
        self.openai_client = None
        
        # Extract a clean API key - looking specifically for the service account key
        api_key = os.getenv("OPENAI_API_KEY", "")
        
        # Look for a service account key pattern (starts with sk-svcacct-)
        service_key = None
        if "sk-svcacct-" in api_key:
            start_idx = api_key.find("sk-svcacct-")
            end_idx = start_idx + 87  # Standard OpenAI key length is 51 chars, but service keys are longer
            if start_idx >= 0 and start_idx + 11 < len(api_key):
                service_key = api_key[start_idx:min(end_idx, len(api_key))]
                print(f"Found service account key, using that for OpenAI API")
            
        # Use the extracted service key or the original if not found
        working_key = service_key if service_key else api_key
            
        if working_key:
            try:
                print("Initializing OpenAI client with provided key")
                self.openai_client = OpenAI(api_key=working_key)
                self.openai_available = True
            except Exception as e:
                print(f"OpenAI client initialization error: {str(e)}")
                self.openai_client = None
                self.openai_available = False
        else:
            print("No valid OpenAI API key found. Using local translation only.")
            self.openai_client = None
            self.openai_available = False
            
        # Try to initialize IndicTranslator
        if INDIC_TRANS_AVAILABLE:
            try:
                self.indic_translator = IndicTranslator()
                print("IndicTrans initialized successfully.")
            except Exception as e:
                print(f"IndicTrans initialization failed: {e}")
                self.indic_translator = None
        else:
            self.indic_translator = None
        
        # Supported languages with their codes
        self.languages = {
            "english": "en",
            "hindi": "hi",
            "tamil": "ta",
            "bengali": "bn",
            "marathi": "mr",
            "telugu": "te",
            "gujarati": "gu",
            "kannada": "kn",
            "malayalam": "ml",
            "punjabi": "pa",
            "urdu": "ur",
            "odia": "or"
        }
        
        # Language code to name mapping for detection
        self.lang_code_to_name = {
            "en": "english",
            "hi": "hindi", 
            "ta": "tamil",
            "bn": "bengali",
            "mr": "marathi",
            "te": "telugu",
            "gu": "gujarati",
            "kn": "kannada",
            "ml": "malayalam",
            "pa": "punjabi",
            "ur": "urdu",
            "or": "odia"
        }
    
    def detect_language(self, text):
        """
        Detect the language of the text
        
        Args:
            text (str): Text to detect language of
            
        Returns:
            str: Detected language name (english, hindi, etc.)
        """
        if not text or len(text.strip()) < 20:
            return "english"  # Default to English for very short or empty text
            
        try:
            # Use langdetect library
            lang_code = detect(text)
            
            # Map language code to language name
            if lang_code in self.lang_code_to_name:
                return self.lang_code_to_name[lang_code]
            else:
                # If not in our supported languages, default to English
                return "english"
        except LangDetectException:
            # Fallback to our simple English detection
            if self._is_english(text):
                return "english"
            else:
                # Default to English if detection fails
                return "english"
    
    def translate_text(self, text, target_language):
        """
        Translate text to the target language
        
        Args:
            text (str): Text to translate
            target_language (str): Target language name (english, hindi, tamil, etc.)
            
        Returns:
            str: Translated text
        """
        if not text:
            return ""
        
        if target_language.lower() not in self.languages:
            return f"Unsupported language: {target_language}. Supported languages are: {', '.join(self.languages.keys())}"
        
        # Get source language
        source_language = "english"  # Assume English source for summaries
        
        # If already in target language, return as is
        if source_language.lower() == target_language.lower():
            return text
        
        lang_code = self.languages[target_language.lower()]
        print(f"Translating from {source_language} to {target_language} (code: {lang_code})")
        
        translated_text = None
        translation_method = None
        
        # Use a simpler approach - try each method in sequence until one works
        
        # Use our specialized direct translators - most reliable and no API dependency
        translator = get_translator(lang_code)
        if translator:
            try:
                print(f"Using direct translator for {target_language}")
                if isinstance(translator, TamilLegalTranslator):
                    translated_text = translator.translate(text)
                    translation_method = "Enhanced Tamil Template"
                else:
                    translated_text = translator.translate(text)
                    translation_method = f"Direct {target_language.capitalize()} Translation"
            except Exception as e:
                print(f"Direct translator failed: {str(e)}")
                translated_text = None
                
        # Method 5: Basic language formatter with proper headers and formatting
        if not translated_text:
            try:
                print(f"Using basic language formatter for {target_language}")
                # This will use our BasicLegalTranslator for languages without specialized translations
                # It will format the text with proper headers in the target language
                translator = get_translator(lang_code)
                if translator:
                    translated_text = translator.translate(text)
                    if isinstance(translator, BasicLegalTranslator):
                        translation_method = f"Basic {target_language.capitalize()} Template"
                    else:
                        translation_method = f"Direct {target_language.capitalize()} Translation"
                else:
                    # Very unlikely fallback
                    translated_text = f"[{target_language.capitalize()} translation using basic template]\n\n{text}"
                    translation_method = "Basic Template"
            except Exception as e:
                print(f"Basic translation failed: {str(e)}")
                translated_text = None
        
        # Final fallback
        if not translated_text:
            return f"[Translation to {target_language} failed. All translation services failed.]\n\n{text}"
        
        # Prepend translation method for transparency
        if translation_method:
            return f"Translation method used: {translation_method}\n\n{translated_text}"
        else:
            return translated_text
    
    def _translate_with_openai(self, text, target_language):
        """Use OpenAI for translation as a fallback"""
        if not self.openai_client:
            print("OpenAI client not available for translation")
            raise Exception("OpenAI API key not configured or invalid")
            
        try:
            response = self.openai_client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": f"You are a professional translator specializing in legal documents. Translate the following text accurately to {target_language}, maintaining legal meaning and terminology."},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            error_str = str(e)
            if "quota" in error_str.lower() or "insufficient_quota" in error_str:
                print(f"OpenAI API quota exceeded, cannot use for translation")
                raise Exception("OpenAI API quota exceeded")
            else:
                print(f"OpenAI translation failed: {error_str}")
                raise Exception(f"OpenAI translation error: {error_str}")
    
    def _is_english(self, text):
        """Simple check if text is primarily English"""
        # Sample first 100 characters to detect language
        sample = text[:100].lower()
        english_chars = set("abcdefghijklmnopqrstuvwxyz .,;:!?'\"()-")
        non_english_chars = [c for c in sample if c not in english_chars and not c.isdigit()]
        
        # If more than 15% non-English characters, assume it's not English
        return len(non_english_chars) / max(1, len(sample)) < 0.15
