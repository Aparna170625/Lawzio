"""
Direct implementation for Tamil translation without external API dependencies
This focuses on robust, reliable translation for legal documents
"""
import re
import os
import json

class TamilLegalTranslator:
    """
    Tamil legal document translator using a comprehensive legal terminology dictionary
    This is a specialized template-based approach for legal documents
    """
    
    def __init__(self):
        """Initialize the Tamil legal translator with comprehensive legal terminology"""
        # Extended Tamil legal terms and phrases dictionary
        self.tamil_legal_terms = {
            # Basic contract terms
            "agreement": "ஒப்பந்தம்",
            "contract": "ஒப்பந்தம்",
            "party": "கட்சி",
            "parties": "கட்சிகள்",
            "terms": "விதிமுறைகள்",
            "conditions": "நிபந்தனைகள்",
            "clause": "பிரிவு",
            "section": "பிரிவு",
            "paragraph": "பத்தி",
            "article": "கட்டுரை",
            "addendum": "இணைப்பு",
            "amendment": "திருத்தம்",
            
            # Legal framework terms
            "law": "சட்டம்",
            "legal": "சட்டபூர்வமான",
            "statute": "சட்டவிதி",
            "regulation": "விதிமுறை",
            "provision": "ஏற்பாடு",
            "code": "நெறிமுறை",
            "bylaws": "துணைச்சட்டங்கள்",
            "legislation": "சட்டமியற்றுதல்",
            "ordinance": "அரசாணை",
            
            # Court-related terms
            "court": "நீதிமன்றம்",
            "supreme court": "உச்ச நீதிமன்றம்",
            "high court": "உயர் நீதிமன்றம்",
            "district court": "மாவட்ட நீதிமன்றம்",
            "judge": "நீதிபதி",
            "magistrate": "நீதித்துறை அதிகாரி",
            "bench": "நீதிபீடம்",
            "plaintiff": "வாதி",
            "defendant": "பிரதிவாதி",
            "petitioner": "மனுதாரர்",
            "respondent": "பதிலளிப்பவர்",
            "appellant": "மேல்முறையீட்டாளர்",
            "witness": "சாட்சி",
            "testimony": "சாட்சியம்",
            "evidence": "ஆதாரம்",
            "exhibit": "காட்சிப்பொருள்",
            "affidavit": "சத்தியக்கடதாசி",
            "deposition": "வாக்குமூலம்",
            "docket": "வழக்குப்பட்டியல்",
            
            # Legal outcomes
            "verdict": "தீர்ப்பு",
            "ruling": "தீர்ப்பு",
            "judgment": "தீர்ப்பு",
            "decree": "ஆணை",
            "order": "உத்தரவு",
            "injunction": "தடையாணை",
            "appeal": "மேல்முறையீடு",
            "stay": "இடைக்காலத் தடை",
            "dismissal": "நிராகரிப்பு",
            
            # Legal professionals
            "attorney": "வழக்கறிஞர்",
            "lawyer": "வழக்கறிஞர்",
            "advocate": "வழக்கறிஞர்",
            "counsel": "ஆலோசகர்",
            "solicitor": "வழக்கறிஞர்",
            "barrister": "வழக்காடும் வழக்கறிஞர்",
            "notary": "நோட்டரி",
            "client": "வாடிக்கையாளர்",
            
            # Rights and obligations
            "rights": "உரிமைகள்",
            "obligations": "கடமைகள்",
            "duties": "கடமைகள்",
            "liability": "பொறுப்பு",
            "indemnity": "இழப்பீட்டுப் பாதுகாப்பு",
            "warranty": "உத்தரவாதம்",
            "guarantee": "உறுதிமொழி",
            "covenant": "உடன்படிக்கை",
            "undertaking": "மேற்கொள்ளல்",
            
            # Remedies and penalties
            "damages": "இழப்பீடுகள்",
            "compensation": "இழப்பீடு",
            "restitution": "மீட்டளிப்பு",
            "specific performance": "குறிப்பிட்ட செயலாக்கம்",
            "breach": "மீறல்",
            "violation": "மீறல்",
            "penalty": "அபராதம்",
            "fine": "அபராதம்",
            "sanction": "தண்டனை",
            "punishment": "தண்டனை",
            
            # Contract lifecycle
            "execution": "செயல்படுத்துதல்",
            "enforcement": "அமலாக்கம்",
            "termination": "முடிவுறுத்தல்",
            "expiration": "காலாவதியாதல்",
            "renewal": "புதுப்பித்தல்",
            "extension": "நீட்டிப்பு",
            "cancellation": "ரத்து",
            "rescission": "விலக்கல்",
            
            # Dispute resolution
            "jurisdiction": "அதிகார வரம்பு",
            "venue": "நீதிமன்ற இடம்",
            "arbitration": "நடுவர் தீர்ப்பு",
            "mediation": "மத்தியஸ்தம்",
            "conciliation": "சமரசம்",
            "settlement": "தீர்வு",
            "negotiation": "பேச்சுவார்த்தை",
            "dispute": "சர்ச்சை",
            "litigation": "வழக்காடுதல்",
            
            # Document-related terms
            "document": "ஆவணம்",
            "deed": "பத்திரம்",
            "certificate": "சான்றிதழ்",
            "signature": "கையொப்பம்",
            "seal": "முத்திரை",
            "date": "தேதி",
            "execution date": "செயல்படுத்தும் தேதி",
            "effective date": "நடைமுறைக்கு வரும் தேதி",
            
            # Property-related terms
            "property": "சொத்து",
            "real property": "அசையா சொத்து",
            "personal property": "அசையும் சொத்து",
            "asset": "சொத்து",
            "title": "உரிமை",
            "deed": "பத்திரம்",
            "mortgage": "அடமானம்",
            "lease": "குத்தகை",
            "easement": "உரிமைப்பாதை",
            
            # Privacy and confidentiality
            "confidential": "இரகசியமான",
            "confidentiality": "இரகசியத்தன்மை",
            "privacy": "தனியுரிமை",
            "disclosure": "வெளிப்படுத்துதல்",
            "non-disclosure": "வெளியிடாமை",
            
            # Financial terms
            "payment": "கட்டணம்",
            "fee": "கட்டணம்",
            "cost": "செலவு",
            "expense": "செலவு",
            "price": "விலை",
            "consideration": "பரிசீலனை",
            "tax": "வரி",
            "interest": "வட்டி",
            "penalty": "அபராதம்",
            "default": "தவறுகை",
            
            # Legal drafting terms
            "hereby": "இதன்மூலம்",
            "whereas": "அதேபோல்",
            "notwithstanding": "எனினும்",
            "herein": "இதில்",
            "hereof": "இதைப் பற்றி",
            "thereof": "அதைப் பற்றி",
            "aforementioned": "மேலே குறிப்பிடப்பட்ட",
            "hereunder": "இதன் கீழ்",
            "subject to": "இதற்கு உட்பட்டு",
            
            # General legal concepts
            "force majeure": "இயற்கை சீற்றம்",
            "act of god": "இயற்கை சீற்றம்",
            "good faith": "நல்லெண்ணம்",
            "due diligence": "உரிய கவனம்",
            "precedent": "முன்னுதாரணம்",
            "doctrine": "கோட்பாடு",
            "rule of law": "சட்டத்தின் ஆட்சி",
            "public policy": "பொது கொள்கை",
            "summary": "சுருக்கம்"
        }
        
        # Section headers in Tamil
        self.section_headers = {
            "Overview": "கண்ணோட்டம்",
            "Summary": "சுருக்கம்",
            "Introduction": "அறிமுகம்",
            "Background": "பின்னணி",
            "Purpose": "நோக்கம்",
            "Scope": "நோக்கம்",
            "Terms": "விதிமுறைகள்",
            "Conditions": "நிபந்தனைகள்",
            "Obligations": "கடமைகள்",
            "Rights": "உரிமைகள்",
            "Representations": "பிரதிநிதித்துவங்கள்",
            "Warranties": "உத்தரவாதங்கள்",
            "Payment": "கட்டணம்",
            "Termination": "முடிவுறுத்தல்",
            "Governing Law": "ஆளும் சட்டம்",
            "Dispute Resolution": "சர்ச்சை தீர்வு",
            "Confidentiality": "இரகசியத்தன்மை",
            "General Provisions": "பொது விதிகள்",
            "Miscellaneous": "இதர",
            "Signatures": "கையொப்பங்கள்",
        }
        
        # Basic Tamil phrases for legal document translation
        self.tamil_header = "சட்ட ஆவண சுருக்கம்"  # Legal Document Summary
        self.tamil_intro = "இந்த சட்ட ஆவணத்தின் சுருக்கம் பின்வருமாறு:"  # The summary of this legal document is as follows
        self.tamil_note = "குறிப்பு: இது முழுமையான மொழிபெயர்ப்பு அல்ல, மேலும் முக்கிய சட்ட சொற்களுக்கான பொருள் மட்டுமே வழங்கப்படுகிறது."  # Note: This is not a complete translation, and only provides meaning for key legal terms.
    
    def translate(self, text):
        """
        Translate English legal text into Tamil using the legal terms dictionary
        
        Args:
            text (str): The English legal text to translate
            
        Returns:
            str: Text with Tamil translations for legal terms
        """
        if not text:
            return ""
            
        try:
            # First, replace section headers
            enhanced_text = text
            for eng_header, tamil_header in self.section_headers.items():
                pattern = r'\b' + re.escape(eng_header) + r'\b'
                enhanced_text = re.sub(pattern, f"{eng_header} ({tamil_header})", enhanced_text, flags=re.IGNORECASE)
            
            # Then replace legal terms
            for eng_term, tamil_term in self.tamil_legal_terms.items():
                # Replace whole words only (with word boundaries)
                pattern = r'\b' + re.escape(eng_term) + r'\b'
                enhanced_text = re.sub(pattern, f"{eng_term} ({tamil_term})", enhanced_text, flags=re.IGNORECASE)
            
            # Create a formatted Tamil summary with translated key terms
            full_translation = f"{self.tamil_header}\n\n{self.tamil_intro}\n\n----\n\n{enhanced_text}\n\n----\n\n{self.tamil_note}"
            return full_translation
            
        except Exception as e:
            print(f"Tamil translation error: {str(e)}")
            # Even if there's an error, try to return something
            return f"{self.tamil_header}\n\n{text}\n\n{self.tamil_note}"


# More translators can be added here in the future

def get_translator(language_code):
    """
    Factory function to get the appropriate translator for a language
    
    Args:
        language_code (str): Two-letter language code (e.g., 'ta' for Tamil)
        
    Returns:
        Translator object or None if not available
    """
    if language_code.lower() == 'ta':
        return TamilLegalTranslator()
    # Add more translators here as needed
    return None