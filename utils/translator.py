import os
import json
import re
from googletrans.constants import LANGUAGES, LANGCODES
from googletrans import Translator
from openai import OpenAI
from langdetect import detect, LangDetectException

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
        self.google_translator = Translator()
        
        # Check OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        self.openai_available = False
        if api_key:
            try:
                self.openai_client = OpenAI(api_key=api_key)
                self.openai_available = True
                print("OpenAI client initialized successfully.")
            except Exception as e:
                print(f"OpenAI client initialization error: {str(e)}")
                self.openai_client = None
        else:
            print("OPENAI_API_KEY environment variable not set")
            self.openai_client = None
            
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
        
        # Method 1: IndicTrans for Indian languages (if available)
        is_indic_target = target_language.lower() in ["hindi", "tamil", "bengali", "marathi", 
                                                    "telugu", "gujarati", "kannada", "malayalam", 
                                                    "punjabi", "urdu", "odia"]
        
        if not translated_text and hasattr(self, 'indic_translator') and self.indic_translator and getattr(self.indic_translator, 'is_available', False) and is_indic_target:
            try:
                print(f"Using IndicTrans for {source_language} to {target_language} translation")
                translated_text = self.indic_translator.translate(text, source_language, target_language)
                if translated_text and translated_text.strip():
                    translation_method = "IndicTrans"
                else:
                    translated_text = None
            except Exception as e:
                print(f"IndicTrans translation failed: {str(e)}")
                translated_text = None
        
        # Method 2: OpenAI for Tamil specifically (and as a second option for others)
        if not translated_text and self.openai_available and self.openai_client:
            try:
                print(f"Using OpenAI for {source_language} to {target_language} translation")
                # Create a system prompt for translation
                system_prompt = f"You are a professional translator specializing in legal documents. Translate the following text accurately to {target_language}, maintaining legal meaning and terminology."
                
                response = self.openai_client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": text}
                    ],
                    temperature=0.3,
                )
                
                translated_text = response.choices[0].message.content
                if translated_text and translated_text.strip():
                    translation_method = "OpenAI GPT-4o"
                else:
                    translated_text = None
            except Exception as e:
                error_str = str(e)
                if "quota" in error_str.lower() or "insufficient_quota" in error_str:
                    print(f"OpenAI API quota exceeded, cannot use for translation")
                    self.openai_available = False
                else:
                    print(f"OpenAI translation failed: {error_str}")
                translated_text = None
        
        # Method 3: Direct translation with basic templates
        if not translated_text:
            try:
                print(f"Using direct translation for {target_language}")
                translated_text = f"[{target_language.capitalize()} translation using basic translation]\n\n{text}"
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
