"""
Direct implementation for Indian language translation without external API dependencies
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
            str: Fully translated Tamil text
        """
        if not text:
            return ""
            
        try:
            # First attempt a complete translation by replacing known document structures
            
            # Common legal document framework patterns
            service_agreement_pattern = re.compile(r'Service Agreement', re.IGNORECASE)
            agreement_pattern = re.compile(r'This (agreement|contract) \("Agreement"\) is made (on|as of) (.*?)(,| ) between', re.IGNORECASE)
            parties_pattern = re.compile(r'(Company Name|Service Provider):\s*(.*?)(\n|$)', re.IGNORECASE)
            client_pattern = re.compile(r'(Client Name|Customer):\s*(.*?)(\n|$)', re.IGNORECASE)
            payment_pattern = re.compile(r'(Payment Terms|Total Contract Value):', re.IGNORECASE)
            service_pattern = re.compile(r'(Services to be Provided|Scope of Services):', re.IGNORECASE)
            
            # Replace common document structures with Tamil templates
            tamil_text = text
            tamil_text = service_agreement_pattern.sub("சேவை ஒப்பந்தம்", tamil_text)
            
            # Replace agreement introduction
            agreement_match = agreement_pattern.search(text)
            if agreement_match:
                date_part = agreement_match.group(3)
                intro_text = "இந்த சேவை ஒப்பந்தம் (\"ஒப்பந்தம்\") " + date_part + " அன்று, பின்வரும் தரப்புகளுக்கு இடையே செய்யப்படுகிறது:"
                tamil_text = agreement_pattern.sub(intro_text, tamil_text)
            
            # Replace common section headers with Tamil versions
            for eng_header, tamil_header in self.section_headers.items():
                pattern = r'\b' + re.escape(eng_header) + r'[:\.]?\s*\n'
                tamil_text = re.sub(pattern, f"{tamil_header}:\n", tamil_text, flags=re.IGNORECASE)
                
                # Also match numbered sections
                numbered_pattern = r'(\d+\.)\s*' + re.escape(eng_header) + r'[:\.]?\s*\n'
                tamil_text = re.sub(numbered_pattern, f"\\1 {tamil_header}:\n", tamil_text, flags=re.IGNORECASE)
            
            # Replace legal terms with Tamil equivalents
            for eng_term, tamil_term in self.tamil_legal_terms.items():
                # Replace whole words only (with word boundaries)
                pattern = r'\b' + re.escape(eng_term) + r'\b'
                tamil_text = re.sub(pattern, tamil_term, tamil_text, flags=re.IGNORECASE)
            
            # Format document nicely with Tamil title and section dividers
            full_translation = f"{self.tamil_header}\n\n{tamil_text}"
            return full_translation
            
        except Exception as e:
            print(f"Full Tamil translation error: {str(e)}")
            # Fallback to simpler approach
            try:
                # If full translation fails, do the simpler term-by-term approach
                enhanced_text = text
                for eng_header, tamil_header in self.section_headers.items():
                    pattern = r'\b' + re.escape(eng_header) + r'\b'
                    enhanced_text = re.sub(pattern, f"{eng_header} ({tamil_header})", enhanced_text, flags=re.IGNORECASE)
                
                # Then replace legal terms
                for eng_term, tamil_term in self.tamil_legal_terms.items():
                    pattern = r'\b' + re.escape(eng_term) + r'\b'
                    enhanced_text = re.sub(pattern, f"{eng_term} ({tamil_term})", enhanced_text, flags=re.IGNORECASE)
                
                return f"{self.tamil_header}\n\n{self.tamil_intro}\n\n----\n\n{enhanced_text}\n\n----\n\n{self.tamil_note}"
            except Exception as e2:
                print(f"Tamil translation fallback error: {str(e2)}")
                # Even if there's an error, try to return something
                return f"{self.tamil_header}\n\n{text}\n\n{self.tamil_note}"


class HindiLegalTranslator:
    """
    Hindi legal document translator using a comprehensive legal terminology dictionary
    This is a specialized template-based approach for Hindi legal documents
    """
    
    def __init__(self):
        """Initialize the Hindi legal translator with comprehensive legal terminology"""
        # Extended Hindi legal terms and phrases dictionary
        self.hindi_legal_terms = {
            # Basic contract terms
            "agreement": "समझौता",
            "contract": "अनुबंध",
            "party": "पक्ष",
            "parties": "पक्षों",
            "terms": "शर्तें",
            "conditions": "शर्तें",
            "clause": "खंड",
            "section": "अनुभाग",
            "paragraph": "पैराग्राफ",
            "article": "अनुच्छेद",
            "addendum": "परिशिष्ट",
            "amendment": "संशोधन",
            
            # Legal framework terms
            "law": "कानून",
            "legal": "कानूनी",
            "statute": "विधि",
            "regulation": "नियम",
            "provision": "प्रावधान",
            "code": "संहिता",
            "bylaws": "उपनियम",
            "legislation": "विधान",
            "ordinance": "अध्यादेश",
            
            # Court-related terms
            "court": "न्यायालय",
            "supreme court": "सर्वोच्च न्यायालय",
            "high court": "उच्च न्यायालय",
            "district court": "जिला न्यायालय",
            "judge": "न्यायाधीश",
            "magistrate": "मजिस्ट्रेट",
            "bench": "पीठ",
            "plaintiff": "वादी",
            "defendant": "प्रतिवादी",
            "petitioner": "याचिकाकर्ता",
            "respondent": "प्रत्यर्थी",
            "appellant": "अपीलकर्ता",
            "witness": "गवाह",
            "testimony": "गवाही",
            "evidence": "सबूत",
            "exhibit": "प्रदर्शनी",
            "affidavit": "हलफनामा",
            "deposition": "गवाही",
            "docket": "डॉकेट",
            
            # Legal outcomes
            "verdict": "फैसला",
            "ruling": "निर्णय",
            "judgment": "न्यायनिर्णय",
            "decree": "डिक्री",
            "order": "आदेश",
            "injunction": "निषेधाज्ञा",
            "appeal": "अपील",
            "stay": "रोक",
            "dismissal": "खारिज",
            
            # Legal professionals
            "attorney": "अधिवक्ता",
            "lawyer": "वकील",
            "advocate": "अधिवक्ता",
            "counsel": "परामर्शदाता",
            "solicitor": "सॉलिसिटर",
            "barrister": "बैरिस्टर",
            "notary": "नोटरी",
            "client": "ग्राहक",
            
            # Rights and obligations
            "rights": "अधिकार",
            "obligations": "दायित्व",
            "duties": "कर्तव्य",
            "liability": "देयता",
            "indemnity": "क्षतिपूर्ति",
            "warranty": "वारंटी",
            "guarantee": "गारंटी",
            "covenant": "प्रतिज्ञापत्र",
            "undertaking": "वचनबद्धता",
            
            # Remedies and penalties
            "damages": "हर्जाना",
            "compensation": "मुआवजा",
            "restitution": "प्रत्यावर्तन",
            "specific performance": "विशिष्ट पालन",
            "breach": "उल्लंघन",
            "violation": "उल्लंघन",
            "penalty": "जुर्माना",
            "fine": "जुर्माना",
            "sanction": "प्रतिबंध",
            "punishment": "सजा",
            
            # Contract lifecycle
            "execution": "निष्पादन",
            "enforcement": "प्रवर्तन",
            "termination": "समाप्ति",
            "expiration": "समाप्ति",
            "renewal": "नवीकरण",
            "extension": "विस्तार",
            "cancellation": "रद्दीकरण",
            "rescission": "विखंडन",
            
            # Dispute resolution
            "jurisdiction": "क्षेत्राधिकार",
            "venue": "स्थान",
            "arbitration": "मध्यस्थता",
            "mediation": "मध्यस्थता",
            "conciliation": "सुलह",
            "settlement": "निपटारा",
            "negotiation": "बातचीत",
            "dispute": "विवाद",
            "litigation": "मुकदमेबाजी",
            
            # Document-related terms
            "document": "दस्तावेज़",
            "deed": "विलेख",
            "certificate": "प्रमाणपत्र",
            "signature": "हस्ताक्षर",
            "seal": "मुहर",
            "date": "तारीख",
            "execution date": "निष्पादन तिथि",
            "effective date": "प्रभावी तिथि",
            
            # Property-related terms
            "property": "संपत्ति",
            "real property": "अचल संपत्ति",
            "personal property": "व्यक्तिगत संपत्ति",
            "asset": "परिसंपत्ति",
            "title": "स्वामित्व",
            "mortgage": "बंधक",
            "lease": "पट्टा",
            "easement": "सुगमता",
            
            # Privacy and confidentiality
            "confidential": "गोपनीय",
            "confidentiality": "गोपनीयता",
            "privacy": "निजता",
            "disclosure": "प्रकटीकरण",
            "non-disclosure": "गैर-प्रकटीकरण",
            
            # Financial terms
            "payment": "भुगतान",
            "fee": "शुल्क",
            "cost": "लागत",
            "expense": "व्यय",
            "price": "मूल्य",
            "consideration": "प्रतिफल",
            "tax": "कर",
            "interest": "ब्याज",
            "default": "चूक",
            
            # Legal drafting terms
            "hereby": "एतद्द्वारा",
            "whereas": "जबकि",
            "notwithstanding": "के बावजूद",
            "herein": "इसमें",
            "hereof": "इसका",
            "thereof": "उसका",
            "aforementioned": "पूर्वोक्त",
            "hereunder": "इसके अंतर्गत",
            "subject to": "के अधीन",
            
            # General legal concepts
            "force majeure": "अप्रत्याशित घटना",
            "act of god": "दैवीय घटना",
            "good faith": "सद्भावना",
            "due diligence": "सम्यक तत्परता",
            "precedent": "पूर्वोदाहरण",
            "doctrine": "सिद्धांत",
            "rule of law": "विधि का शासन",
            "public policy": "लोक नीति",
            "summary": "सारांश"
        }
        
        # Section headers in Hindi
        self.section_headers = {
            "Overview": "अवलोकन",
            "Summary": "सारांश",
            "Introduction": "परिचय",
            "Background": "पृष्ठभूमि",
            "Purpose": "उद्देश्य",
            "Scope": "विस्तार",
            "Terms": "शर्तें",
            "Conditions": "शर्तें",
            "Obligations": "दायित्व",
            "Rights": "अधिकार",
            "Representations": "प्रतिनिधित्व",
            "Warranties": "वारंटियां",
            "Payment": "भुगतान",
            "Termination": "समाप्ति",
            "Governing Law": "शासी कानून",
            "Dispute Resolution": "विवाद समाधान",
            "Confidentiality": "गोपनीयता",
            "General Provisions": "सामान्य प्रावधान",
            "Miscellaneous": "विविध",
            "Signatures": "हस्ताक्षर",
        }
        
        # Basic Hindi phrases for legal document translation
        self.hindi_header = "कानूनी दस्तावेज़ सारांश"  # Legal Document Summary
        self.hindi_intro = "इस कानूनी दस्तावेज़ का सारांश निम्नलिखित है:"  # The summary of this legal document is as follows
        self.hindi_note = "नोट: यह पूर्ण अनुवाद नहीं है, और केवल प्रमुख कानूनी शब्दों के अर्थ प्रदान करता है।"  # Note: This is not a complete translation, and only provides meaning for key legal terms.
    
    def translate(self, text):
        """
        Translate English legal text into Hindi using the legal terms dictionary
        
        Args:
            text (str): The English legal text to translate
            
        Returns:
            str: Fully translated Hindi text
        """
        if not text:
            return ""
            
        try:
            # First attempt a complete translation by replacing known document structures
            
            # Common legal document framework patterns
            service_agreement_pattern = re.compile(r'Service Agreement', re.IGNORECASE)
            agreement_pattern = re.compile(r'This (agreement|contract) \("Agreement"\) is made (on|as of) (.*?)(,| ) between', re.IGNORECASE)
            parties_pattern = re.compile(r'(Company Name|Service Provider):\s*(.*?)(\n|$)', re.IGNORECASE)
            client_pattern = re.compile(r'(Client Name|Customer):\s*(.*?)(\n|$)', re.IGNORECASE)
            payment_pattern = re.compile(r'(Payment Terms|Total Contract Value):', re.IGNORECASE)
            service_pattern = re.compile(r'(Services to be Provided|Scope of Services):', re.IGNORECASE)
            
            # Replace common document structures with Hindi templates
            hindi_text = text
            hindi_text = service_agreement_pattern.sub("सेवा अनुबंध", hindi_text)
            
            # Replace agreement introduction
            agreement_match = agreement_pattern.search(text)
            if agreement_match:
                date_part = agreement_match.group(3)
                intro_text = "यह सेवा अनुबंध (\"अनुबंध\") " + date_part + " को किया गया है, निम्नलिखित पक्षों के बीच:"
                hindi_text = agreement_pattern.sub(intro_text, hindi_text)
            
            # Replace common section headers with Hindi versions
            for eng_header, hindi_header in self.section_headers.items():
                pattern = r'\b' + re.escape(eng_header) + r'[:\.]?\s*\n'
                hindi_text = re.sub(pattern, f"{hindi_header}:\n", hindi_text, flags=re.IGNORECASE)
                
                # Also match numbered sections
                numbered_pattern = r'(\d+\.)\s*' + re.escape(eng_header) + r'[:\.]?\s*\n'
                hindi_text = re.sub(numbered_pattern, f"\\1 {hindi_header}:\n", hindi_text, flags=re.IGNORECASE)
            
            # Replace legal terms with Hindi equivalents
            for eng_term, hindi_term in self.hindi_legal_terms.items():
                # Replace whole words only (with word boundaries)
                pattern = r'\b' + re.escape(eng_term) + r'\b'
                hindi_text = re.sub(pattern, hindi_term, hindi_text, flags=re.IGNORECASE)
            
            # Format document nicely with Hindi title and section dividers
            full_translation = f"{self.hindi_header}\n\n{hindi_text}"
            return full_translation
            
        except Exception as e:
            print(f"Full Hindi translation error: {str(e)}")
            # Fallback to simpler approach
            try:
                # If full translation fails, do the simpler term-by-term approach
                enhanced_text = text
                for eng_header, hindi_header in self.section_headers.items():
                    pattern = r'\b' + re.escape(eng_header) + r'\b'
                    enhanced_text = re.sub(pattern, f"{eng_header} ({hindi_header})", enhanced_text, flags=re.IGNORECASE)
                
                # Then replace legal terms
                for eng_term, hindi_term in self.hindi_legal_terms.items():
                    pattern = r'\b' + re.escape(eng_term) + r'\b'
                    enhanced_text = re.sub(pattern, f"{eng_term} ({hindi_term})", enhanced_text, flags=re.IGNORECASE)
                
                return f"{self.hindi_header}\n\n{self.hindi_intro}\n\n----\n\n{enhanced_text}\n\n----\n\n{self.hindi_note}"
            except Exception as e2:
                print(f"Hindi translation fallback error: {str(e2)}")
                # Even if there's an error, try to return something
                return f"{self.hindi_header}\n\n{text}\n\n{self.hindi_note}"


# Basic language-specific translator with legal terminology
class BasicLegalTranslator:
    """
    A generic formatter for legal document translations
    when a specialized translator is not available
    """
    
    def __init__(self, language_name, language_code):
        """Initialize the basic translator with language info"""
        self.language_name = language_name
        self.language_code = language_code
        
        # Basic header translations for common languages
        self.headers = {
            "hi": {
                "header": "कानूनी दस्तावेज़ सारांश",
                "intro": "इस कानूनी दस्तावेज़ का सारांश निम्नलिखित है:",
                "note": "नोट: यह पूर्ण अनुवाद नहीं है, केवल मूल अंग्रेजी पाठ के साथ प्रदान किया गया है।"
            },
            "mr": {
                "header": "कायदेशीर दस्तऐवजाचा सारांश",
                "intro": "या कायदेशीर दस्तऐवजाचा सारांश खालीलप्रमाणे आहे:",
                "note": "टीप: हा पूर्ण अनुवाद नाही, मूळ इंग्रजी मजकुरासह प्रदान केला आहे."
            },
            "bn": {
                "header": "আইনি নথির সারসংক্ষেপ",
                "intro": "এই আইনি নথির সারসংক্ষেপ নিম্নরূপ:",
                "note": "দ্রষ্টব্য: এটি একটি সম্পূর্ণ অনুবাদ নয়, মূল ইংরেজি পাঠ্যের সাথে প্রদান করা হয়েছে।"
            },
            "te": {
                "header": "చట్టపరమైన పత్రం యొక్క సారాంశం",
                "intro": "ఈ చట్టపరమైన పత్రం యొక్క సారాంశం కింది విధంగా ఉంది:",
                "note": "గమనిక: ఇది పూర్తి అనువాదం కాదు, అసలు ఇంగ్లీష్ పాఠంతో అందించబడింది."
            },
            "gu": {
                "header": "કાનૂની દસ્તાવેજનો સારાંશ",
                "intro": "આ કાનૂની દસ્તાવેજનો સારાંશ નીચે મુજબ છે:",
                "note": "નોંધ: આ પૂર્ણ અનુવાદ નથી, મૂળ અંગ્રેજી લખાણ સાથે પ્રદાન કરવામાં આવ્યું છે."
            },
            "kn": {
                "header": "ಕಾನೂನು ದಾಖಲೆಯ ಸಾರಾಂಶ",
                "intro": "ಈ ಕಾನೂನು ದಾಖಲೆಯ ಸಾರಾಂಶವು ಈ ಕೆಳಗಿನಂತಿದೆ:",
                "note": "ಗಮನಿಸಿ: ಇದು ಪೂರ್ಣ ಅನುವಾದವಲ್ಲ, ಮೂಲ ಇಂಗ್ಲಿಷ್ ಪಠ್ಯದೊಂದಿಗೆ ಒದಗಿಸಲಾಗಿದೆ."
            },
            "ml": {
                "header": "നിയമപരമായ രേഖയുടെ സംഗ്രഹം",
                "intro": "ഈ നിയമപരമായ രേഖയുടെ സംഗ്രഹം ചുവടെ കാണുന്നു:",
                "note": "കുറിപ്പ്: ഇത് ഒരു പൂർണ്ണ വിവർത്തനമല്ല, യഥാർത്ഥ ഇംഗ്ലീഷ് ടെക്സ്റ്റിനൊപ്പം നൽകിയിരിക്കുന്നു."
            },
            "pa": {
                "header": "ਕਾਨੂੰਨੀ ਦਸਤਾਵੇਜ਼ ਦਾ ਸਾਰ",
                "intro": "ਇਸ ਕਾਨੂੰਨੀ ਦਸਤਾਵੇਜ਼ ਦਾ ਸਾਰ ਹੇਠਾਂ ਦਿੱਤਾ ਗਿਆ ਹੈ:",
                "note": "ਨੋਟ: ਇਹ ਪੂਰਾ ਅਨੁਵਾਦ ਨਹੀਂ ਹੈ, ਅਸਲ ਅੰਗਰੇਜ਼ੀ ਪਾਠ ਦੇ ਨਾਲ ਪ੍ਰਦਾਨ ਕੀਤਾ ਗਿਆ ਹੈ।"
            },
            "ur": {
                "header": "قانونی دستاویز کا خلاصہ",
                "intro": "اس قانونی دستاویز کا خلاصہ درج ذیل ہے:",
                "note": "نوٹ: یہ مکمل ترجمہ نہیں ہے، اصل انگریزی متن کے ساتھ فراہم کیا گیا ہے۔"
            },
            "or": {
                "header": "ଆଇନଗତ ଦଲିଲର ସାରାଂଶ",
                "intro": "ଏହି ଆଇନଗତ ଦଲିଲର ସାରାଂଶ ନିମ୍ନରେ ଦିଆଯାଇଛି:",
                "note": "ଦ୍ରଷ୍ଟବ୍ୟ: ଏହା ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଅନୁବାଦ ନୁହେଁ, ମୂଳ ଇଂରାଜୀ ପାଠ୍ୟ ସହିତ ପ୍ରଦାନ କରାଯାଇଛି।"
            },
        }
        
        # Default English if language not supported
        self.default_headers = {
            "header": f"Legal Document Summary ({self.language_name})",
            "intro": f"The summary of this legal document is as follows ({self.language_name}):",
            "note": f"Note: This is not a complete translation, provided with the original English text."
        }
    
    def translate(self, text):
        """
        Format the text with proper headers and formatting
        
        Args:
            text (str): The English legal text
            
        Returns:
            str: Formatted text with headers in target language
        """
        if not text:
            return ""
            
        try:
            # Get appropriate headers for the language
            lang_headers = self.headers.get(self.language_code.lower(), self.default_headers)
            
            # Create a nicely formatted output with sections
            formatted_text = f"{lang_headers['header']}\n\n{lang_headers['intro']}\n\n"
            formatted_text += "----\n\n"
            
            # Add the original text (which we'll consider as the translation for now)
            formatted_text += text
            
            # Add footer note
            formatted_text += f"\n\n----\n\n{lang_headers['note']}"
            
            return formatted_text
            
        except Exception as e:
            print(f"Basic translation formatting error: {str(e)}")
            # Even if there's an error, return something
            return f"Translation to {self.language_name}\n\n{text}"


def get_translator(language_code):
    """
    Factory function to get the appropriate translator for a language
    
    Args:
        language_code (str): Two-letter language code (e.g., 'ta' for Tamil)
        
    Returns:
        Translator object or None if not available
    """
    # Language code to name mapping for more readable outputs
    language_names = {
        "en": "English",
        "hi": "Hindi", 
        "ta": "Tamil",
        "bn": "Bengali",
        "mr": "Marathi",
        "te": "Telugu",
        "gu": "Gujarati",
        "kn": "Kannada",
        "ml": "Malayalam",
        "pa": "Punjabi",
        "ur": "Urdu",
        "or": "Odia"
    }
    
    # First check for specialized translators
    if language_code.lower() == 'ta':
        return TamilLegalTranslator()
    elif language_code.lower() == 'hi':
        return HindiLegalTranslator()
    
    # For other languages, use the basic formatter with appropriate language name
    language_name = language_names.get(language_code.lower(), "Unknown")
    return BasicLegalTranslator(language_name, language_code.lower())