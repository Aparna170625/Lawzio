"""
Localization module for translating the UI elements
Uses language-specific dictionaries for UI translations
"""

# Translation dictionaries for UI elements in different languages
TRANSLATIONS = {
    "english": {
        # App title and description
        "app_title": "⚖️ Lawzio - Legal Document Summarizer",
        "app_description": "Simplify complex legal documents with AI-powered summarization and translation",
        
        # Settings
        "settings": "Settings",
        "summary_detail_level": "Summary Detail Level:",
        "simple": "Simple",
        "detailed": "Detailed",
        "output_language": "Output Language:",
        
        # About section
        "about_lawzio": "About Lawzio",
        "about_description": """
        Lawzio helps users understand complex legal documents by:
        - Summarizing lengthy legal texts
        - Simplifying legal jargon
        - Assessing document risk levels
        - Identifying potential risk factors
        - Translating content across languages
        - Highlighting key points
        """,
        
        # Translation methods
        "translation_methods": "Translation Methods",
        "indictrans_available": "✅ **IndicTrans**: Native Indian language translation",
        "indictrans_unavailable": "❌ **IndicTrans**: Not available",
        "openai_available": "✅ **OpenAI GPT-4o**: AI-powered translation",
        "openai_unavailable": "❌ **OpenAI GPT-4o**: Not available (needs API key)",
        "google_available": "✅ **Google Translate**: General translation",
        "google_unavailable": "❌ **Google Translate**: Not available",
        
        # Privacy section
        "privacy_notice": "Privacy Notice",
        "privacy_content": """
        - All documents are processed securely
        - Documents are not stored permanently
        - AI processing is used for summarization
        - We recommend removing sensitive information
        """,
        
        # Document upload
        "document_upload": "Document Upload",
        "upload_prompt": "Upload a legal document",
        "upload_help": "Supported formats: PDF, DOCX, TXT, and Images (JPG, PNG, TIFF, BMP)",
        "processing_document": "Processing document...",
        "processed_success": "Document '{0}' processed successfully!",
        
        # Document info
        "document_information": "Document Information",
        "filename": "Filename:",
        "size": "Size:",
        "content_length": "Content Length:",
        "detected_language": "Detected Language:",
        "kb": "KB",
        "characters": "characters",
        
        # Risk assessment
        "assessing_risk": "Assessing document risk level...",
        "risk_level": "Risk Level:",
        "risk_factors_detected": "Risk Factors Detected:",
        "no_risk_factors": "No specific risk factors detected",
        
        # Document preview
        "document_preview": "Document Preview",
        
        # Actions
        "summarize_document": "Summarize Document",
        "clear_all": "Clear All",
        "generating_summary": "Generating {0} summary...",
        "translating_to": "Translating to {0}...",
        "translation_error": "Translation error: {0}. Showing original summary.",
        "translation_error_msg": "**Translation Error**: Could not translate to {0}. Showing original summary in English.",
        
        # Results section
        "summary_results": "Summary Results",
        "summary_in": "{0} Summary in {1}",
        "translation_method_used": "Translation method used: **{0}**",
        "download_summary": "Download Summary",
        "empty_state": "Upload a document and click 'Summarize Document' to see results here.",
        
        # Sample capabilities
        "lawzio_can_help": "Lawzio Can Help You With:",
        "legal_judgments": "Legal Judgments",
        "contracts_agreements": "Contracts & Agreements",
        "court_orders": "Court Orders",
        "legal_notices": "Legal Notices",
        "legal_opinions": "Legal Opinions",
        "terms_conditions": "Terms & Conditions",
        
        # Footer
        "footer": "Lawzio - Making legal documents accessible for everyone"
    },
    
    "hindi": {
        # App title and description
        "app_title": "⚖️ लॉज़िओ - कानूनी दस्तावेज़ सारांशकर्ता",
        "app_description": "AI-संचालित सारांश और अनुवाद के साथ जटिल कानूनी दस्तावेजों को सरल बनाएं",
        
        # Settings
        "settings": "सेटिंग्स",
        "summary_detail_level": "सारांश विवरण स्तर:",
        "simple": "सरल",
        "detailed": "विस्तृत",
        "output_language": "आउटपुट भाषा:",
        
        # About section
        "about_lawzio": "लॉज़िओ के बारे में",
        "about_description": """
        लॉज़िओ उपयोगकर्ताओं को जटिल कानूनी दस्तावेजों को समझने में मदद करता है:
        - लंबे कानूनी पाठों का सारांश
        - कानूनी जटिल भाषा को सरल बनाना
        - दस्तावेज़ जोखिम स्तरों का आकलन
        - संभावित जोखिम कारकों की पहचान
        - भाषाओं में सामग्री का अनुवाद
        - महत्वपूर्ण बिंदुओं को हाइलाइट करना
        """,
        
        # Translation methods
        "translation_methods": "अनुवाद विधियाँ",
        "indictrans_available": "✅ **IndicTrans**: भारतीय भाषा अनुवाद",
        "indictrans_unavailable": "❌ **IndicTrans**: उपलब्ध नहीं",
        "openai_available": "✅ **OpenAI GPT-4o**: AI-संचालित अनुवाद",
        "openai_unavailable": "❌ **OpenAI GPT-4o**: उपलब्ध नहीं (API कुंजी की आवश्यकता है)",
        "google_available": "✅ **Google Translate**: सामान्य अनुवाद",
        "google_unavailable": "❌ **Google Translate**: उपलब्ध नहीं",
        
        # Privacy section
        "privacy_notice": "गोपनीयता सूचना",
        "privacy_content": """
        - सभी दस्तावेज़ सुरक्षित रूप से संसाधित किए जाते हैं
        - दस्तावेज़ स्थायी रूप से संग्रहित नहीं किए जाते हैं
        - सारांश के लिए AI प्रसंस्करण का उपयोग किया जाता है
        - हम संवेदनशील जानकारी हटाने की सलाह देते हैं
        """,
        
        # Document upload
        "document_upload": "दस्तावेज़ अपलोड",
        "upload_prompt": "कानूनी दस्तावेज़ अपलोड करें",
        "upload_help": "समर्थित प्रारूप: PDF, DOCX, TXT, और छवियां (JPG, PNG, TIFF, BMP)",
        "processing_document": "दस्तावेज़ प्रोसेसिंग...",
        "processed_success": "दस्तावेज़ '{0}' सफलतापूर्वक प्रोसेस किया गया!",
        
        # Document info
        "document_information": "दस्तावेज़ जानकारी",
        "filename": "फ़ाइल का नाम:",
        "size": "आकार:",
        "content_length": "सामग्री की लंबाई:",
        "detected_language": "पहचानी गई भाषा:",
        "kb": "KB",
        "characters": "अक्षर",
        
        # Risk assessment
        "assessing_risk": "दस्तावेज़ जोखिम स्तर का आकलन...",
        "risk_level": "जोखिम स्तर:",
        "risk_factors_detected": "पहचाने गए जोखिम कारक:",
        "no_risk_factors": "कोई विशिष्ट जोखिम कारक नहीं मिला",
        
        # Document preview
        "document_preview": "दस्तावेज़ पूर्वावलोकन",
        
        # Actions
        "summarize_document": "दस्तावेज़ सारांश करें",
        "clear_all": "सब साफ करें",
        "generating_summary": "{0} सारांश उत्पन्न कर रहा है...",
        "translating_to": "{0} में अनुवाद कर रहा है...",
        "translation_error": "अनुवाद त्रुटि: {0}। मूल सारांश दिखा रहा है।",
        "translation_error_msg": "**अनुवाद त्रुटि**: {0} में अनुवाद नहीं कर सका। अंग्रेजी में मूल सारांश दिखा रहा है।",
        
        # Results section
        "summary_results": "सारांश परिणाम",
        "summary_in": "{0} सारांश {1} में",
        "translation_method_used": "उपयोग की गई अनुवाद विधि: **{0}**",
        "download_summary": "सारांश डाउनलोड करें",
        "empty_state": "दस्तावेज़ अपलोड करें और परिणाम देखने के लिए 'दस्तावेज़ सारांश करें' पर क्लिक करें।",
        
        # Sample capabilities
        "lawzio_can_help": "लॉज़िओ आपकी इनमें मदद कर सकता है:",
        "legal_judgments": "कानूनी निर्णय",
        "contracts_agreements": "अनुबंध और समझौते",
        "court_orders": "न्यायालय के आदेश",
        "legal_notices": "कानूनी नोटिस",
        "legal_opinions": "कानूनी राय",
        "terms_conditions": "नियम और शर्तें",
        
        # Footer
        "footer": "लॉज़िओ - कानूनी दस्तावेजों को सभी के लिए सुलभ बनाना"
    },
    
    "tamil": {
        # App title and description
        "app_title": "⚖️ லாசியோ - சட்ட ஆவண சுருக்கி",
        "app_description": "AI-சக்தி சுருக்கம் மற்றும் மொழிபெயர்ப்புடன் சிக்கலான சட்ட ஆவணங்களை எளிதாக்குங்கள்",
        
        # Settings
        "settings": "அமைப்புகள்",
        "summary_detail_level": "சுருக்க விவர நிலை:",
        "simple": "எளிய",
        "detailed": "விரிவான",
        "output_language": "வெளியீட்டு மொழி:",
        
        # About section
        "about_lawzio": "லாசியோ பற்றி",
        "about_description": """
        லாசியோ பயனர்களுக்கு சிக்கலான சட்ட ஆவணங்களைப் புரிந்துகொள்ள உதவுகிறது:
        - நீண்ட சட்ட உரைகளை சுருக்குதல்
        - சட்ட சொற்களை எளிமைப்படுத்துதல்
        - ஆவண ஆபத்து நிலைகளை மதிப்பீடு செய்தல்
        - சாத்தியமான ஆபத்து காரணிகளை அடையாளம் காணுதல்
        - மொழிகள் முழுவதும் உள்ளடக்கத்தை மொழிபெயர்த்தல்
        - முக்கிய புள்ளிகளை முன்னிலைப்படுத்துதல்
        """,
        
        # Translation methods
        "translation_methods": "மொழிபெயர்ப்பு முறைகள்",
        "indictrans_available": "✅ **IndicTrans**: இந்திய மொழி மொழிபெயர்ப்பு",
        "indictrans_unavailable": "❌ **IndicTrans**: கிடைக்கவில்லை",
        "openai_available": "✅ **OpenAI GPT-4o**: AI-சக்தி மொழிபெயர்ப்பு",
        "openai_unavailable": "❌ **OpenAI GPT-4o**: கிடைக்கவில்லை (API விசை தேவை)",
        "google_available": "✅ **Google Translate**: பொது மொழிபெயர்ப்பு",
        "google_unavailable": "❌ **Google Translate**: கிடைக்கவில்லை",
        
        # Privacy section
        "privacy_notice": "தனியுரிமை அறிவிப்பு",
        "privacy_content": """
        - அனைத்து ஆவணங்களும் பாதுகாப்பாக செயலாக்கப்படுகின்றன
        - ஆவணங்கள் நிரந்தரமாக சேமிக்கப்படுவதில்லை
        - சுருக்கத்திற்கு AI செயலாக்கம் பயன்படுத்தப்படுகிறது
        - உணர்திறன் தகவலை அகற்ற பரிந்துரைக்கிறோம்
        """,
        
        # Document upload
        "document_upload": "ஆவண பதிவேற்றம்",
        "upload_prompt": "சட்ட ஆவணத்தைப் பதிவேற்றவும்",
        "upload_help": "ஆதரிக்கப்படும் வடிவங்கள்: PDF, DOCX, TXT, மற்றும் படங்கள் (JPG, PNG, TIFF, BMP)",
        "processing_document": "ஆவணத்தை செயலாக்குகிறது...",
        "processed_success": "ஆவணம் '{0}' வெற்றிகரமாக செயலாக்கப்பட்டது!",
        
        # Document info
        "document_information": "ஆவண தகவல்",
        "filename": "கோப்பு பெயர்:",
        "size": "அளவு:",
        "content_length": "உள்ளடக்க நீளம்:",
        "detected_language": "கண்டறியப்பட்ட மொழி:",
        "kb": "KB",
        "characters": "எழுத்துக்கள்",
        
        # Risk assessment
        "assessing_risk": "ஆவண ஆபத்து நிலையை மதிப்பிடுகிறது...",
        "risk_level": "ஆபத்து நிலை:",
        "risk_factors_detected": "கண்டறியப்பட்ட ஆபத்து காரணிகள்:",
        "no_risk_factors": "குறிப்பிட்ட ஆபத்து காரணிகள் எதுவும் கண்டறியப்படவில்லை",
        
        # Document preview
        "document_preview": "ஆவண முன்னோட்டம்",
        
        # Actions
        "summarize_document": "ஆவணத்தை சுருக்கவும்",
        "clear_all": "அனைத்தையும் அழிக்கவும்",
        "generating_summary": "{0} சுருக்கத்தை உருவாக்குகிறது...",
        "translating_to": "{0} க்கு மொழிபெயர்க்கிறது...",
        "translation_error": "மொழிபெயர்ப்பு பிழை: {0}. அசல் சுருக்கத்தைக் காட்டுகிறது.",
        "translation_error_msg": "**மொழிபெயர்ப்பு பிழை**: {0} க்கு மொழிபெயர்க்க முடியவில்லை. ஆங்கிலத்தில் அசல் சுருக்கத்தைக் காட்டுகிறது.",
        
        # Results section
        "summary_results": "சுருக்க முடிவுகள்",
        "summary_in": "{0} சுருக்கம் {1} இல்",
        "translation_method_used": "பயன்படுத்தப்பட்ட மொழிபெயர்ப்பு முறை: **{0}**",
        "download_summary": "சுருக்கத்தைப் பதிவிறக்கவும்",
        "empty_state": "ஆவணத்தைப் பதிவேற்றி, முடிவுகளைக் காண 'ஆவணத்தை சுருக்கவும்' என்பதைக் கிளிக் செய்யவும்.",
        
        # Sample capabilities
        "lawzio_can_help": "லாசியோ உங்களுக்கு இதில் உதவ முடியும்:",
        "legal_judgments": "சட்ட தீர்ப்புகள்",
        "contracts_agreements": "ஒப்பந்தங்கள் & உடன்படிக்கைகள்",
        "court_orders": "நீதிமன்ற ஆணைகள்",
        "legal_notices": "சட்ட அறிவிப்புகள்",
        "legal_opinions": "சட்ட கருத்துகள்",
        "terms_conditions": "விதிமுறைகள் & நிபந்தனைகள்",
        
        # Footer
        "footer": "லாசியோ - சட்ட ஆவணங்களை அனைவருக்கும் அணுகக்கூடியதாக்குதல்"
    },
    
    # Add more languages as needed
}

def get_ui_text(key, language='english', *format_args):
    """
    Get UI text for the specified key in the given language
    
    Args:
        key (str): The text key to look up
        language (str): The language to use (default: english)
        format_args: Arguments to format into the string if needed
        
    Returns:
        str: The translated text string
    """
    # Default to English if language not available
    if language not in TRANSLATIONS:
        language = 'english'
    
    # Get the translated text dictionary for the language
    texts = TRANSLATIONS.get(language, TRANSLATIONS['english'])
    
    # Get the text for the key, fallback to English if missing
    text = texts.get(key, TRANSLATIONS['english'].get(key, f"Missing text: {key}"))
    
    # Format the text if arguments are provided
    if format_args:
        try:
            return text.format(*format_args)
        except Exception as e:
            print(f"Error formatting text '{key}': {e}")
            return text
    
    return text