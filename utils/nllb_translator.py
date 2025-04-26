"""
NLLB-200 Translator Implementation
Based on Meta's No Language Left Behind model
"""

import torch
import os
import numpy as np
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# NLLB language codes for our supported languages
NLLB_LANGUAGE_CODES = {
    "english": "eng_Latn",
    "hindi": "hin_Deva",
    "tamil": "tam_Taml",
    "bengali": "ben_Beng",
    "marathi": "mar_Deva",
    "telugu": "tel_Telu",
    "gujarati": "guj_Gujr",
    "kannada": "kan_Knda",
    "malayalam": "mal_Mlym",
    "punjabi": "pan_Guru",
    "urdu": "urd_Arab",
    "odia": "ory_Orya"
}

class NLLBTranslator:
    def __init__(self):
        """Initialize the NLLB-200 translator"""
        self.is_available = False
        try:
            # Use smaller distilled model for better performance
            model_name = "facebook/nllb-200-distilled-600M"
            
            print(f"Loading NLLB-200 model: {model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            # Set to CPU - our environment doesn't have a GPU
            self.device = "cpu"
            self.model.to(self.device)
            
            self.is_available = True
            print("NLLB-200 model loaded successfully!")
        except Exception as e:
            print(f"Error initializing NLLB-200 translator: {str(e)}")
            self.is_available = False
    
    def translate(self, text, source_language, target_language):
        """
        Translate text using NLLB-200
        
        Args:
            text (str): Text to translate
            source_language (str): Source language name (english, hindi, etc.)
            target_language (str): Target language name (english, hindi, etc.)
            
        Returns:
            str: Translated text
        """
        if not self.is_available:
            return None
            
        if not text or len(text.strip()) == 0:
            return ""
            
        try:
            # Convert to NLLB language codes
            source_lang_code = NLLB_LANGUAGE_CODES.get(source_language.lower(), "eng_Latn")
            target_lang_code = NLLB_LANGUAGE_CODES.get(target_language.lower(), "eng_Latn")
            
            # Handle longer texts by breaking into chunks
            max_length = 512  # NLLB has a context length of around 512 tokens
            words = text.split()
            chunks = []
            current_chunk = []
            current_length = 0
            
            for word in words:
                if current_length + len(word.split()) + 1 > max_length:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = [word]
                    current_length = len(word.split()) + 1
                else:
                    current_chunk.append(word)
                    current_length += len(word.split()) + 1
                    
            if current_chunk:
                chunks.append(' '.join(current_chunk))
                
            # If text is short enough, just use a single chunk
            if not chunks:
                chunks = [text]
                
            # Translate each chunk
            translated_chunks = []
            for chunk in chunks:
                # Tokenize the text
                inputs = self.tokenizer(chunk, return_tensors="pt").to(self.device)
                
                # Set the language for translation
                self.tokenizer.src_lang = source_lang_code
                
                # Generate translation
                translated_tokens = self.model.generate(
                    **inputs, 
                    forced_bos_token_id=self.tokenizer.lang_code_to_id[target_lang_code],
                    max_length=512,
                    num_beams=5,
                    length_penalty=1.0
                )
                
                # Decode the generated tokens
                translated_text = self.tokenizer.batch_decode(
                    translated_tokens, 
                    skip_special_tokens=True
                )[0]
                
                translated_chunks.append(translated_text)
                
            # Join the translated chunks
            return " ".join(translated_chunks)
            
        except Exception as e:
            print(f"NLLB translation error: {str(e)}")
            return None