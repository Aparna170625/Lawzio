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
        "simple_summary": "Simple Summary", 
        "detailed_summary": "Detailed Summary",
        "in_language": "in {0}",
        "translation_method_used": "Translation method used",
        "download_summary": "Download Summary",
        "empty_state_msg": "Upload a document and click 'Summarize Document' to see results here.",
        "failed": "Failed",
        "translation_error_title": "Translation Error",
        
        # Sample capabilities
        "lawzio_can_help": "Lawzio Can Help You With:",
        "lawzio_capabilities": "Lawzio Can Help You With:",
        "legal_judgments": "Legal Judgments",
        "contracts_agreements": "Contracts & Agreements",
        "court_orders": "Court Orders",
        "legal_notices": "Legal Notices",
        "legal_opinions": "Legal Opinions",
        "terms_conditions": "Terms & Conditions",
        
        # Footer
        "footer": "Lawzio - Making legal documents accessible for everyone | Created by M APARNA & PRAVEEN R",
        "footer_tagline": "Lawzio - Making legal documents accessible for everyone | Created by M APARNA & PRAVEEN R"
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
        "simple_summary": "सरल सारांश", 
        "detailed_summary": "विस्तृत सारांश",
        "in_language": "{0} में",
        "translation_method_used": "उपयोग की गई अनुवाद विधि",
        "download_summary": "सारांश डाउनलोड करें",
        "empty_state_msg": "दस्तावेज़ अपलोड करें और परिणाम देखने के लिए 'दस्तावेज़ सारांश करें' पर क्लिक करें।",
        "failed": "विफल",
        "translation_error_title": "अनुवाद त्रुटि",
        
        # Sample capabilities
        "lawzio_can_help": "लॉज़िओ आपकी इनमें मदद कर सकता है:",
        "lawzio_capabilities": "लॉज़िओ आपकी इनमें मदद कर सकता है:",
        "legal_judgments": "कानूनी निर्णय",
        "contracts_agreements": "अनुबंध और समझौते",
        "court_orders": "न्यायालय के आदेश",
        "legal_notices": "कानूनी नोटिस",
        "legal_opinions": "कानूनी राय",
        "terms_conditions": "नियम और शर्तें",
        
        # Footer
        "footer": "लॉज़िओ - कानूनी दस्तावेजों को सभी के लिए सुलभ बनाना | M APARNA & PRAVEEN R द्वारा निर्मित",
        "footer_tagline": "लॉज़िओ - कानूनी दस्तावेजों को सभी के लिए सुलभ बनाना | M APARNA & PRAVEEN R द्वारा निर्मित"
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
        "simple_summary": "எளிய சுருக்கம்", 
        "detailed_summary": "விரிவான சுருக்கம்",
        "in_language": "{0} இல்",
        "translation_method_used": "பயன்படுத்தப்பட்ட மொழிபெயர்ப்பு முறை",
        "download_summary": "சுருக்கத்தைப் பதிவிறக்கவும்",
        "empty_state_msg": "ஆவணத்தைப் பதிவேற்றி, முடிவுகளைக் காண 'ஆவணத்தை சுருக்கவும்' என்பதைக் கிளிக் செய்யவும்.",
        "failed": "தோல்வி",
        "translation_error_title": "மொழிபெயர்ப்பு பிழை",
        
        # Sample capabilities
        "lawzio_can_help": "லாசியோ உங்களுக்கு இதில் உதவ முடியும்:",
        "lawzio_capabilities": "லாசியோ உங்களுக்கு இதில் உதவ முடியும்:",
        "legal_judgments": "சட்ட தீர்ப்புகள்",
        "contracts_agreements": "ஒப்பந்தங்கள் & உடன்படிக்கைகள்",
        "court_orders": "நீதிமன்ற ஆணைகள்",
        "legal_notices": "சட்ட அறிவிப்புகள்",
        "legal_opinions": "சட்ட கருத்துகள்",
        "terms_conditions": "விதிமுறைகள் & நிபந்தனைகள்",
        
        # Footer
        "footer": "லாசியோ - சட்ட ஆவணங்களை அனைவருக்கும் அணுகக்கூடியதாக்குதல் | M APARNA & PRAVEEN R ஆல் உருவாக்கப்பட்டது",
        "footer_tagline": "லாசியோ - சட்ட ஆவணங்களை அனைவருக்கும் அணுகக்கூடியதாக்குதல் | M APARNA & PRAVEEN R ஆல் உருவாக்கப்பட்டது"
    },
    
    # Add basic templates for other Indian languages
    
    "bengali": {
        # App title and description
        "app_title": "⚖️ লাজিও - আইনি নথি সারাংশকারী",
        "app_description": "AI-পাওয়ারড সারাংশ এবং অনুবাদের সাথে জটিল আইনি নথি সহজ করুন",
        
        # Common labels
        "settings": "সেটিংস",
        "summary_detail_level": "সারাংশ বিবরণ স্তর:",
        "simple": "সহজ",
        "detailed": "বিস্তারিত",
        "output_language": "আউটপুট ভাষা:",
        
        # Document actions
        "upload_prompt": "আইনি নথি আপলোড করুন",
        "document_upload": "নথি আপলোড",
        "summarize_document": "নথি সারাংশ করুন",
        "document_information": "নথি তথ্য", 
        "clear_all": "সব পরিষ্কার করুন",
        
        # Results display
        "summary_results": "সারাংশ ফলাফল",
        "simple_summary": "সহজ সারাংশ",
        "detailed_summary": "বিস্তারিত সারাংশ",
        "lawzio_capabilities": "লাজিও আপনাকে এতে সাহায্য করতে পারে:",
        
        # Footer
        "footer": "লাজিও - সবার জন্য আইনি নথি অ্যাক্সেসযোগ্য করে তোলা",
        "footer_tagline": "লাজিও - সবার জন্য আইনি নথি অ্যাক্সেসযোগ্য করে তোলা"
    },
    
    "marathi": {
        # App title and description
        "app_title": "⚖️ लॉझिओ - कायदेशीर दस्तऐवज सारांशकर्ता",
        "app_description": "AI-संचालित सारांश आणि अनुवादासह जटिल कायदेशीर दस्तऐवज सुलभ करा",
        
        # Common labels
        "settings": "सेटिंग्ज",
        "summary_detail_level": "सारांश तपशील पातळी:",
        "simple": "साधे",
        "detailed": "तपशीलवार",
        "output_language": "आउटपुट भाषा:",
        
        # Document actions
        "upload_prompt": "कायदेशीर दस्तऐवज अपलोड करा",
        "document_upload": "दस्तऐवज अपलोड",
        "summarize_document": "दस्तऐवजाचा सारांश करा",
        "document_information": "दस्तऐवज माहिती", 
        "clear_all": "सर्व साफ करा",
        
        # Results display
        "summary_results": "सारांश परिणाम",
        "simple_summary": "साधा सारांश",
        "detailed_summary": "तपशीलवार सारांश",
        "lawzio_capabilities": "लॉझिओ आपल्याला यामध्ये मदत करू शकते:",
        
        # Footer
        "footer": "लॉझिओ - कायदेशीर दस्तऐवज सर्वांसाठी सुलभ करणे",
        "footer_tagline": "लॉझिओ - कायदेशीर दस्तऐवज सर्वांसाठी सुलभ करणे"
    },
    
    "telugu": {
        # App title and description
        "app_title": "⚖️ లాజియో - చట్టపరమైన పత్రాల సంక్షిప్తీకరణి",
        "app_description": "AI-శక్తితో సారాంశం మరియు అనువాదంతో క్లిష్టమైన చట్టపరమైన పత్రాలను సరళీకరించండి",
        
        # Common labels
        "settings": "సెట్టింగ్‌లు",
        "summary_detail_level": "సారాంశ వివరాల స్థాయి:",
        "simple": "సాధారణ",
        "detailed": "వివరణాత్మక",
        "output_language": "అవుట్‌పుట్ భాష:",
        
        # Document actions
        "upload_prompt": "చట్టపరమైన పత్రాన్ని అప్‌లోడ్ చేయండి",
        "document_upload": "పత్రం అప్‌లోడ్",
        "summarize_document": "పత్రాన్ని సంక్షిప్తీకరించండి",
        "document_information": "పత్రం సమాచారం", 
        "clear_all": "అన్నింటినీ క్లియర్ చేయండి",
        
        # Results display
        "summary_results": "సారాంశ ఫలితాలు",
        "simple_summary": "సాధారణ సారాంశం",
        "detailed_summary": "వివరణాత్మక సారాంశం",
        "lawzio_capabilities": "లాజియో మీకు వీటిలో సహాయపడగలదు:",
        
        # Footer
        "footer": "లాజియో - చట్టపరమైన పత్రాలను అందరికీ అందుబాటులో ఉంచడం",
        "footer_tagline": "లాజియో - చట్టపరమైన పత్రాలను అందరికీ అందుబాటులో ఉంచడం"
    },
    
    "gujarati": {
        # App title and description
        "app_title": "⚖️ લોઝિઓ - કાયદાકીય દસ્તાવેજ સારાંશકાર",
        "app_description": "AI-સંચાલિત સારાંશ અને અનુવાદ સાથે જટિલ કાયદાકીય દસ્તાવેજોને સરળ બનાવો",
        
        # Common labels
        "settings": "સેટિંગ્સ",
        "summary_detail_level": "સારાંશ વિગત સ્તર:",
        "simple": "સરળ",
        "detailed": "વિગતવાર",
        "output_language": "આઉટપુટ ભાષા:",
        
        # Document actions
        "upload_prompt": "કાયદાકીય દસ્તાવેજ અપલોડ કરો",
        "document_upload": "દસ્તાવેજ અપલોડ",
        "summarize_document": "દસ્તાવેજનો સારાંશ કરો",
        "document_information": "દસ્તાવેજ માહિતી", 
        "clear_all": "બધું સાફ કરો",
        
        # Results display
        "summary_results": "સારાંશ પરિણામો",
        "simple_summary": "સરળ સારાંશ",
        "detailed_summary": "વિગતવાર સારાંશ",
        "lawzio_capabilities": "લોઝિઓ તમને આમાં મદદ કરી શકે છે:",
        
        # Footer
        "footer": "લોઝિઓ - કાયદાકીય દસ્તાવેજોને દરેક માટે સુલભ બનાવવા",
        "footer_tagline": "લોઝિઓ - કાયદાકીય દસ્તાવેજોને દરેક માટે સુલભ બનાવવા"
    },
    
    "kannada": {
        # App title and description
        "app_title": "⚖️ ಲಾಜಿಯೋ - ಕಾನೂನು ದಾಖಲೆ ಸಾರಾಂಶಗಾರ",
        "app_description": "AI-ಚಾಲಿತ ಸಾರಾಂಶ ಮತ್ತು ಅನುವಾದದೊಂದಿಗೆ ಸಂಕೀರ್ಣ ಕಾನೂನು ದಾಖಲೆಗಳನ್ನು ಸರಳಗೊಳಿಸಿ",
        
        # Common labels
        "settings": "ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
        "summary_detail_level": "ಸಾರಾಂಶ ವಿವರ ಮಟ್ಟ:",
        "simple": "ಸರಳ",
        "detailed": "ವಿವರವಾದ",
        "output_language": "ಔಟ್‌ಪುಟ್ ಭಾಷೆ:",
        
        # Document actions
        "upload_prompt": "ಕಾನೂನು ದಾಖಲೆಯನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "document_upload": "ದಾಖಲೆ ಅಪ್‌ಲೋಡ್",
        "summarize_document": "ದಾಖಲೆಯನ್ನು ಸಾರಾಂಶಗೊಳಿಸಿ",
        "document_information": "ದಾಖಲೆ ಮಾಹಿತಿ", 
        "clear_all": "ಎಲ್ಲವನ್ನೂ ತೆರವುಗೊಳಿಸಿ",
        
        # Results display
        "summary_results": "ಸಾರಾಂಶ ಫಲಿತಾಂಶಗಳು",
        "simple_summary": "ಸರಳ ಸಾರಾಂಶ",
        "detailed_summary": "ವಿವರವಾದ ಸಾರಾಂಶ",
        "lawzio_capabilities": "ಲಾಜಿಯೋ ನಿಮಗೆ ಇದರಲ್ಲಿ ಸಹಾಯ ಮಾಡಬಹುದು:",
        
        # Footer
        "footer": "ಲಾಜಿಯೋ - ಕಾನೂನು ದಾಖಲೆಗಳನ್ನು ಎಲ್ಲರಿಗೂ ಲಭ್ಯವಾಗುವಂತೆ ಮಾಡುವುದು",
        "footer_tagline": "ಲಾಜಿಯೋ - ಕಾನೂನು ದಾಖಲೆಗಳನ್ನು ಎಲ್ಲರಿಗೂ ಲಭ್ಯವಾಗುವಂತೆ ಮಾಡುವುದು"
    },
    
    "malayalam": {
        # App title and description
        "app_title": "⚖️ ലാസിയോ - നിയമ രേഖ സംഗ്രഹകൻ",
        "app_description": "AI-പവർഡ് സംഗ്രഹവും വിവർത്തനവും ഉപയോഗിച്ച് സങ്കീർണ്ണമായ നിയമ രേഖകൾ ലളിതമാക്കുക",
        
        # Common labels
        "settings": "ക്രമീകരണങ്ങൾ",
        "summary_detail_level": "സംഗ്രഹ വിശദാംശ തലം:",
        "simple": "ലളിതമായ",
        "detailed": "വിശദമായ",
        "output_language": "ഔട്ട്പുട്ട് ഭാഷ:",
        
        # Document actions
        "upload_prompt": "നിയമ രേഖ അപ്‌ലോഡ് ചെയ്യുക",
        "document_upload": "രേഖ അപ്‌ലോഡ്",
        "summarize_document": "രേഖ സംഗ്രഹിക്കുക",
        "document_information": "രേഖാ വിവരങ്ങൾ", 
        "clear_all": "എല്ലാം മായ്‌ക്കുക",
        
        # Results display
        "summary_results": "സംഗ്രഹ ഫലങ്ങൾ",
        "simple_summary": "ലളിതമായ സംഗ്രഹം",
        "detailed_summary": "വിശദമായ സംഗ്രഹം",
        "lawzio_capabilities": "ലാസിയോയ്ക്ക് നിങ്ങളെ ഇതിൽ സഹായിക്കാൻ കഴിയും:",
        
        # Footer
        "footer": "ലാസിയോ - നിയമ രേഖകൾ എല്ലാവർക്കും ലഭ്യമാക്കുന്നു",
        "footer_tagline": "ലാസിയോ - നിയമ രേഖകൾ എല്ലാവർക്കും ലഭ്യമാക്കുന്നു"
    },
    
    "punjabi": {
        # App title and description
        "app_title": "⚖️ ਲਾਜ਼ੀਓ - ਕਾਨੂੰਨੀ ਦਸਤਾਵੇਜ਼ ਸੰਖੇਪਕਾਰ",
        "app_description": "AI-ਸ਼ਕਤੀਸ਼ਾਲੀ ਸੰਖੇਪ ਅਤੇ ਅਨੁਵਾਦ ਨਾਲ ਜਟਿਲ ਕਾਨੂੰਨੀ ਦਸਤਾਵੇਜ਼ਾਂ ਨੂੰ ਆਸਾਨ ਬਣਾਓ",
        
        # Common labels
        "settings": "ਸੈਟਿੰਗਾਂ",
        "summary_detail_level": "ਸੰਖੇਪ ਵੇਰਵਾ ਪੱਧਰ:",
        "simple": "ਸਧਾਰਨ",
        "detailed": "ਵਿਸਤਾਰਿਤ",
        "output_language": "ਆਉਟਪੁੱਟ ਭਾਸ਼ਾ:",
        
        # Document actions
        "upload_prompt": "ਕਾਨੂੰਨੀ ਦਸਤਾਵੇਜ਼ ਅਪਲੋਡ ਕਰੋ",
        "document_upload": "ਦਸਤਾਵੇਜ਼ ਅਪਲੋਡ",
        "summarize_document": "ਦਸਤਾਵੇਜ਼ ਨੂੰ ਸੰਖੇਪ ਕਰੋ",
        "document_information": "ਦਸਤਾਵੇਜ਼ ਜਾਣਕਾਰੀ", 
        "clear_all": "ਸਭ ਸਾਫ਼ ਕਰੋ",
        
        # Results display
        "summary_results": "ਸੰਖੇਪ ਨਤੀਜੇ",
        "simple_summary": "ਸਧਾਰਨ ਸੰਖੇਪ",
        "detailed_summary": "ਵਿਸਤਾਰਿਤ ਸੰਖੇਪ",
        "lawzio_capabilities": "ਲਾਜ਼ੀਓ ਤੁਹਾਡੀ ਇਸ ਵਿੱਚ ਮਦਦ ਕਰ ਸਕਦਾ ਹੈ:",
        
        # Footer
        "footer": "ਲਾਜ਼ੀਓ - ਕਾਨੂੰਨੀ ਦਸਤਾਵੇਜ਼ਾਂ ਨੂੰ ਹਰ ਕਿਸੇ ਲਈ ਪਹੁੰਚਯੋਗ ਬਣਾਉਣਾ",
        "footer_tagline": "ਲਾਜ਼ੀਓ - ਕਾਨੂੰਨੀ ਦਸਤਾਵੇਜ਼ਾਂ ਨੂੰ ਹਰ ਕਿਸੇ ਲਈ ਪਹੁੰਚਯੋਗ ਬਣਾਉਣਾ"
    },
    
    "urdu": {
        # App title and description
        "app_title": "⚖️ لازیو - قانونی دستاویز کا خلاصہ",
        "app_description": "AI پر مبنی خلاصہ اور ترجمہ کے ساتھ پیچیدہ قانونی دستاویزات کو آسان بنائیں",
        
        # Common labels
        "settings": "ترتیبات",
        "summary_detail_level": "خلاصہ تفصیل کی سطح:",
        "simple": "آسان",
        "detailed": "تفصیلی",
        "output_language": "آؤٹ پٹ زبان:",
        
        # Document actions
        "upload_prompt": "قانونی دستاویز اپلوڈ کریں",
        "document_upload": "دستاویز اپلوڈ",
        "summarize_document": "دستاویز کا خلاصہ کریں",
        "document_information": "دستاویز کی معلومات", 
        "clear_all": "سب صاف کریں",
        
        # Results display
        "summary_results": "خلاصہ نتائج",
        "simple_summary": "آسان خلاصہ",
        "detailed_summary": "تفصیلی خلاصہ",
        "lawzio_capabilities": "لازیو آپ کی ان میں مدد کر سکتا ہے:",
        
        # Footer
        "footer": "لازیو - قانونی دستاویزات کو سب کے لیے قابل رسائی بنانا",
        "footer_tagline": "لازیو - قانونی دستاویزات کو سب کے لیے قابل رسائی بنانا"
    },
    
    "odia": {
        # App title and description
        "app_title": "⚖️ ଲାଜିଓ - ଆଇନଗତ ଦଲିଲ ସାରାଂଶକାରୀ",
        "app_description": "AI-ଶକ୍ତି ସାରାଂଶ ଏବଂ ଅନୁବାଦ ସହିତ ଜଟିଳ ଆଇନଗତ ଦଲିଲଗୁଡିକୁ ସରଳ କରନ୍ତୁ",
        
        # Common labels
        "settings": "ସେଟିଂସ୍",
        "summary_detail_level": "ସାରାଂଶ ବିବରଣୀ ସ୍ତର:",
        "simple": "ସରଳ",
        "detailed": "ବିସ୍ତୃତ",
        "output_language": "ଆଉଟପୁଟ୍ ଭାଷା:",
        
        # Document actions
        "upload_prompt": "ଆଇନଗତ ଦଲିଲ ଅପଲୋଡ୍ କରନ୍ତୁ",
        "document_upload": "ଦଲିଲ ଅପଲୋଡ୍",
        "summarize_document": "ଦଲିଲର ସାରାଂଶ କରନ୍ତୁ",
        "document_information": "ଦଲିଲ ସୂଚନା", 
        "clear_all": "ସବୁ ସଫା କରନ୍ତୁ",
        
        # Results display
        "summary_results": "ସାରାଂଶ ଫଳାଫଳ",
        "simple_summary": "ସରଳ ସାରାଂଶ",
        "detailed_summary": "ବିସ୍ତୃତ ସାରାଂଶ",
        "lawzio_capabilities": "ଲାଜିଓ ଆପଣଙ୍କୁ ଏଥିରେ ସାହାଯ୍ୟ କରିପାରିବ:",
        
        # Footer
        "footer": "ଲାଜିଓ - ଆଇନଗତ ଦଲିଲଗୁଡିକୁ ସମସ୍ତଙ୍କ ପାଇଁ ସୁଲଭ କରିବା",
        "footer_tagline": "ଲାଜିଓ - ଆଇନଗତ ଦଲିଲଗୁଡିକୁ ସମସ୍ତଙ୍କ ପାଇଁ ସୁଲଭ କରିବା"
    }
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