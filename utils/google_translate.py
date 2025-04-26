"""
Direct implementation of Google Translate API without dependencies
Uses direct HTTP requests to unofficial free translation endpoints
"""
import requests
import json
import random
import time
import urllib.parse

def translate_text(text, target_language, source_language='auto'):
    """
    Translate text using Google Translate free API
    
    Args:
        text (str): Text to translate
        target_language (str): Target language code (e.g., 'hi', 'ta')
        source_language (str): Source language code or 'auto' for auto-detection
        
    Returns:
        str: Translated text or original text if translation fails
    """
    if not text:
        return ""
    
    # Standard language code mapping (Google uses different codes)
    language_code_map = {
        'hi': 'hi',  # Hindi
        'ta': 'ta',  # Tamil
        'bn': 'bn',  # Bengali
        'mr': 'mr',  # Marathi
        'te': 'te',  # Telugu
        'gu': 'gu',  # Gujarati
        'kn': 'kn',  # Kannada
        'ml': 'ml',  # Malayalam
        'pa': 'pa',  # Punjabi
        'ur': 'ur',  # Urdu
        'or': 'or',  # Odia
        'en': 'en',  # English
    }
    
    # Map language code to Google's format
    google_target_lang = language_code_map.get(target_language.lower(), target_language.lower())
    google_source_lang = language_code_map.get(source_language.lower(), source_language.lower()) if source_language != 'auto' else 'auto'
    
    # Method 1: Direct API Call (most reliable)
    try:
        # Google Translate API URL
        url = "https://translate.googleapis.com/translate_a/single"
        
        # Request parameters
        params = {
            "client": "gtx",
            "sl": google_source_lang,
            "tl": google_target_lang,
            "dt": "t",  # Return translated text
            "q": text
        }
        
        # Add a random delay to avoid rate limits (0.1 to 0.5 seconds)
        time.sleep(random.uniform(0.1, 0.5))
        
        # Make the request
        response = requests.get(url, params=params)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse the response
            result = response.json()
            
            # Extract translated text
            translated_text = ""
            if result and isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
                for sentence in result[0]:
                    if len(sentence) > 0:
                        translated_text += sentence[0]
            
            return translated_text
        else:
            print(f"Google Translate API error: {response.status_code}")
            return text
            
    except Exception as e:
        print(f"Google Translate error: {str(e)}")
        return text
        
    # If we reach here, all methods have failed
    return text