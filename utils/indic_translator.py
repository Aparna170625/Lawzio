import os
import io
import requests
import zipfile
import tempfile
from pathlib import Path
import ctranslate2
import sentencepiece as spm
from indicnlp.tokenize import indic_tokenize
from sacremoses import MosesPunctNormalizer, MosesTokenizer, MosesDetokenizer

# Define model paths
MODELS_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "indictrans2")

# Define language mappings with ISO codes
INDIC_LANGUAGE_CODES = {
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

# Define the language-family mapping
LANGUAGE_FAMILIES = {
    "en": "en",  # English
    "hi": "indic",  # Hindi
    "ta": "indic",  # Tamil
    "bn": "indic",  # Bengali
    "mr": "indic",  # Marathi
    "te": "indic",  # Telugu
    "gu": "indic",  # Gujarati
    "kn": "indic",  # Kannada
    "ml": "indic",  # Malayalam
    "pa": "indic",  # Punjabi
    "ur": "indic",  # Urdu
    "or": "indic",  # Odia
}

class IndicTranslator:
    def __init__(self):
        """Initialize the IndicTrans2 based translation system"""
        self.models = {}
        self.tokenizers = {}
        self.detokenizers = {}
        try:
            self.normalize_punctuation = MosesPunctNormalizer()
            # Initialize base tokenizers and detokenizers
            self.en_tokenizer = MosesTokenizer(lang='en')
            self.en_detokenizer = MosesDetokenizer(lang='en')
        except Exception as e:
            print(f"Failed to initialize MosesPunctNormalizer and tokenizers: {e}")
            # Set default empty implementations if Moses fails
            self.normalize_punctuation = lambda text: text  # Just return text as is
            self.en_tokenizer = lambda text: text.split()  # Simple split by space
            self.en_detokenizer = lambda tokens: ' '.join(tokens)  # Simple join by space
            
        self.is_available = False
        self.supported_languages = list(INDIC_LANGUAGE_CODES.keys())
        
        # Try to initialize the models
        try:
            print("Attempting to initialize IndicTrans models...")
            self._download_and_setup_models()
            self.is_available = True
            print("IndicTrans models initialized successfully!")
        except Exception as e:
            print(f"IndicTrans initialization error: {e}")
            self.is_available = False
            print("IndicTrans will not be available for translation. Using fallback translators.")
    
    def _download_and_setup_models(self):
        """Download and setup the required IndicTrans2 models"""
        # Create cache directory if it doesn't exist
        os.makedirs(MODELS_CACHE_DIR, exist_ok=True)
        
        # Check if model files already exist
        en_indic_dir = os.path.join(MODELS_CACHE_DIR, "en-indic")
        indic_en_dir = os.path.join(MODELS_CACHE_DIR, "indic-en")
        
        # Download the models if they don't exist
        if not os.path.exists(en_indic_dir) or not os.path.exists(indic_en_dir):
            try:
                self._download_models()
            except Exception as e:
                raise Exception(f"Failed to download models: {e}")
        
        # Load the models
        try:
            # English to Indic
            self.models["en-indic"] = ctranslate2.Translator(
                os.path.join(MODELS_CACHE_DIR, "en-indic"),
                device="cpu"
            )
            self.tokenizers["en"] = spm.SentencePieceProcessor()
            self.tokenizers["en"].Load(os.path.join(MODELS_CACHE_DIR, "en-indic", "sp_en.model"))
            
            # Indic to English
            self.models["indic-en"] = ctranslate2.Translator(
                os.path.join(MODELS_CACHE_DIR, "indic-en"),
                device="cpu"
            )
            self.tokenizers["indic"] = spm.SentencePieceProcessor()
            self.tokenizers["indic"].Load(os.path.join(MODELS_CACHE_DIR, "indic-en", "sp_indic.model"))
        except Exception as e:
            raise Exception(f"Failed to load translation models: {e}")
    
    def _download_models(self):
        """Download the IndicTrans2 models"""
        # Updated IndicTrans2 models URLs
        model_urls = {
            "en-indic": "https://indic-nlp-public.objectstore.e2enetworks.net/ai4bharat/indictrans2/indictrans2-en-indic-ct2_int8.zip",
            "indic-en": "https://indic-nlp-public.objectstore.e2enetworks.net/ai4bharat/indictrans2/indictrans2-indic-en-ct2_int8.zip"
        }
        
        for model_name, url in model_urls.items():
            try:
                # Download the model zip file
                print(f"Downloading {model_name} model...")
                response = requests.get(url, stream=True)
                response.raise_for_status()
                
                # Save to a temporary file
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        temp_file.write(chunk)
                
                # Extract the zip file
                print(f"Extracting {model_name} model...")
                model_dir = os.path.join(MODELS_CACHE_DIR, model_name)
                os.makedirs(model_dir, exist_ok=True)
                
                with zipfile.ZipFile(temp_file.name, 'r') as zip_ref:
                    zip_ref.extractall(model_dir)
                
                # Clean up temporary file
                os.remove(temp_file.name)
                print(f"Model {model_name} downloaded and extracted successfully.")
            except Exception as e:
                raise Exception(f"Failed to download {model_name} model: {e}")
    
    def _preprocess_indic_text(self, text, lang_code):
        """Preprocess Indic language text"""
        if lang_code == "en":
            # For English, use Moses tokenizer
            text = self.normalize_punctuation.normalize(text)
            tokenized_text = " ".join(self.en_tokenizer.tokenize(text))
            return tokenized_text
        else:
            # For Indic languages use indicnlp tokenizer
            text = self.normalize_punctuation.normalize(text)
            tokenized_text = indic_tokenize.trivial_tokenize(text, lang_code)
            return tokenized_text
    
    def _postprocess_indic_text(self, text, lang_code):
        """Postprocess translated text"""
        if lang_code == "en":
            # For English use Moses detokenizer
            return self.en_detokenizer.detokenize(text.split())
        else:
            # For Indic languages, just return as is (detokenization handled by the model)
            return text
    
    def translate(self, text, source_language, target_language):
        """
        Translate text from source language to target language
        
        Args:
            text (str): Text to translate
            source_language (str): Source language name (english, hindi, etc.)
            target_language (str): Target language name (english, hindi, etc.)
            
        Returns:
            str: Translated text
        """
        if not self.is_available:
            raise Exception("IndicTrans models are not available. Translation cannot be performed.")
        
        if not text:
            return ""
        
        # Convert language names to ISO codes
        if source_language.lower() not in INDIC_LANGUAGE_CODES:
            raise ValueError(f"Unsupported source language: {source_language}")
        if target_language.lower() not in INDIC_LANGUAGE_CODES:
            raise ValueError(f"Unsupported target language: {target_language}")
            
        source_code = INDIC_LANGUAGE_CODES[source_language.lower()]
        target_code = INDIC_LANGUAGE_CODES[target_language.lower()]
        
        # If the source and target languages are the same, return the original text
        if source_code == target_code:
            return text
            
        # Determine translation direction
        source_family = LANGUAGE_FAMILIES[source_code]
        target_family = LANGUAGE_FAMILIES[target_code]
        
        if source_family == target_family:
            # Language families are the same, this is not supported by IndicTrans
            # For indic-to-indic, translate to English first, then to target
            if source_family == "indic":
                english_trans = self.translate(text, source_language, "english")
                return self.translate(english_trans, "english", target_language)
            else:
                # Both languages are English, just return
                return text
        
        # Select appropriate model for translation direction
        if source_family == "en" and target_family == "indic":
            model = self.models["en-indic"]
            tokenizer = self.tokenizers["en"]
            direction = "en-indic"
        elif source_family == "indic" and target_family == "en":
            model = self.models["indic-en"]
            tokenizer = self.tokenizers["indic"]
            direction = "indic-en"
        else:
            raise ValueError(f"Unsupported translation direction: {source_family} to {target_family}")
        
        try:
            # Preprocess
            processed_text = self._preprocess_indic_text(text, source_code)
            
            # Tokenize
            tokenized_text = tokenizer.encode(processed_text, out_type=str)
            
            # Translate
            translation_results = model.translate_batch([tokenized_text], target_prefix=[[target_code]])
            translated_tokens = translation_results[0].hypotheses[0]
            
            # Detokenize
            translated_text = tokenizer.decode(translated_tokens)
            
            # Postprocess
            final_translation = self._postprocess_indic_text(translated_text, target_code)
            
            return final_translation
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")