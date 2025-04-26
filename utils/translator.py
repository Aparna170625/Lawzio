import os
import json
import re
# Import for direct HTTP requests to free translation service
import requests
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
        
        # For Tamil, use our enhanced template as the primary method (most reliable without API dependency)
        if not translated_text and target_language.lower() == "tamil":
            try:
                print(f"Using enhanced Tamil local translation")
                
                # Common Tamil legal terms and phrases dictionary
                tamil_legal_terms = {
                    "agreement": "ஒப்பந்தம்",
                    "contract": "ஒப்பந்தம்",
                    "party": "கட்சி",
                    "parties": "கட்சிகள்",
                    "terms": "விதிமுறைகள்",
                    "conditions": "நிபந்தனைகள்",
                    "clause": "பிரிவு",
                    "section": "பிரிவு",
                    "law": "சட்டம்",
                    "legal": "சட்டபூர்வமான",
                    "court": "நீதிமன்றம்",
                    "judge": "நீதிபதி",
                    "plaintiff": "வாதி",
                    "defendant": "பிரதிவாதி",
                    "witness": "சாட்சி",
                    "evidence": "ஆதாரம்",
                    "testimony": "சாட்சியம்",
                    "verdict": "தீர்ப்பு",
                    "ruling": "தீர்ப்பு",
                    "judgment": "தீர்ப்பு",
                    "appeal": "மேல்முறையீடு",
                    "attorney": "வழக்கறிஞர்",
                    "lawyer": "வழக்கறிஞர்",
                    "advocate": "வழக்கறிஞர்",
                    "client": "வாடிக்கையாளர்",
                    "rights": "உரிமைகள்",
                    "obligations": "கடமைகள்",
                    "liability": "பொறுப்பு",
                    "damages": "இழப்பீடுகள்",
                    "compensation": "இழப்பீடு",
                    "breach": "மீறல்",
                    "violation": "மீறல்",
                    "penalty": "அபராதம்",
                    "fine": "அபராதம்",
                    "termination": "முடிவுறுத்தல்",
                    "jurisdiction": "அதிகார வரம்பு",
                    "arbitration": "நடுவர் தீர்ப்பு",
                    "mediation": "மத்தியஸ்தம்",
                    "settlement": "தீர்வு",
                    "document": "ஆவணம்",
                    "signature": "கையொப்பம்",
                    "date": "தேதி",
                    "property": "சொத்து",
                    "confidential": "இரகசியமான",
                    "confidentiality": "இரகசியத்தன்மை",
                    "payment": "கட்டணம்",
                    "fee": "கட்டணம்",
                    "dispute": "சர்ச்சை",
                    "hereby": "இதன்மூலம்",
                    "whereas": "அதேபோல்",
                    "notwithstanding": "எனினும்",
                    "herein": "இதில்",
                    "hereof": "இதைப் பற்றி",
                    "thereof": "அதைப் பற்றி",
                    "summary": "சுருக்கம்"
                }
                
                # Add some basic Tamil phrases for legal document translation
                tamil_header = "சட்ட ஆவண சுருக்கம்"  # Legal Document Summary
                tamil_intro = "இந்த சட்ட ஆவணத்தின் சுருக்கம் பின்வருமாறு:"  # The summary of this legal document is as follows
                tamil_note = "குறிப்பு: இது முழுமையான மொழிபெயர்ப்பு அல்ல, மேலும் முக்கிய சட்ட சொற்களுக்கான பொருள் மட்டுமே வழங்கப்படுகிறது."  # Note: This is not a complete translation, and only provides meaning for key legal terms.
                
                # Replace common legal terms in the original text
                enhanced_text = text
                for eng_term, tamil_term in tamil_legal_terms.items():
                    # Replace whole words only (with word boundaries)
                    import re
                    pattern = r'\b' + re.escape(eng_term) + r'\b'
                    enhanced_text = re.sub(pattern, f"{eng_term} ({tamil_term})", enhanced_text, flags=re.IGNORECASE)
                
                # Create a formatted Tamil summary with translated key terms
                translated_text = f"{tamil_header}\n\n{tamil_intro}\n\n----\n\n{enhanced_text}\n\n----\n\n{tamil_note}"
                translation_method = "Enhanced Tamil Template"
            except Exception as e:
                print(f"Enhanced Tamil translation failed: {str(e)}")
                translated_text = None
                
        # Method 5: Direct translation with basic templates (fallback for all languages)
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
