import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL_NAME = "gpt-4o"

class OpenAIHelper:
    def __init__(self):
        """
        Initialize OpenAI helper with API key from environment
        """
        api_key = os.getenv("OPENAI_API_KEY")
        self.is_api_available = False
        self.client = None
        
        # We noticed the project API key format (sk-proj-) doesn't work well
        # Let's check for that and provide a better error message
        if api_key:
            if api_key.startswith("sk-proj-"):
                print("Project API keys (sk-proj-*) are not fully supported. Using local summarization only.")
            else:
                try:
                    # Initialize client 
                    self.client = OpenAI(api_key=api_key)
                    
                    # Validate the API key with a simple request
                    try:
                        # Just check if models endpoint works
                        self.client.models.list(limit=1)
                        self.is_api_available = True
                        print("OpenAI client initialized and verified successfully.")
                    except Exception as validate_error:
                        print(f"OpenAI API key validation failed: {str(validate_error)}")
                        self.client = None
                except Exception as e:
                    print(f"OpenAI client initialization error: {str(e)}")
                    self.client = None
        else:
            print("OPENAI_API_KEY environment variable not set")
            self.client = None
    
    def summarize_legal_document(self, text, detail_level="detailed"):
        """
        Summarize a legal document using OpenAI
        
        Args:
            text (str): The legal document text to summarize
            detail_level (str): 'simple' or 'detailed' summary
        
        Returns:
            str: Summarized text
        """
        if not text:
            return "No text to summarize."
            
        # Check if OpenAI API is available
        if not self.is_api_available or self.client is None:
            return self._generate_fallback_summary(text, detail_level)
        
        # Truncate if text is too long
        max_tokens = 15000  # Reasonable limit for GPT-4o context
        if len(text) > max_tokens*4:  # Rough character to token ratio
            text = text[:max_tokens*4] + "\n\n[Document truncated due to length]"
        
        if detail_level == "simple":
            system_prompt = (
                "You are a legal assistant that simplifies complex legal documents. "
                "Create a concise, easy-to-understand summary in plain language. "
                "Avoid legal jargon when possible, and explain any necessary legal terms. "
                "Focus on the key points, obligations, rights, and conclusions only."
            )
        else:  # detailed
            system_prompt = (
                "You are a legal assistant that summarizes legal documents. "
                "Create a comprehensive summary with the following sections:\n"
                "1. Overview: Brief description of the document type and purpose\n"
                "2. Key Facts: Important dates, parties, case numbers, etc.\n"
                "3. Main Arguments/Points: Primary legal arguments or clauses\n"
                "4. Conclusions/Rulings: Final decisions, judgments, obligations\n"
                "5. Important Legal Principles: Notable precedents or legal concepts\n\n"
                "Use proper legal terminology while still being clear."
            )
        
        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Summarize this legal document:\n\n{text}"}
                ],
                temperature=0.3,  # Lower temperature for more consistent output
            )
            return response.choices[0].message.content
        except Exception as e:
            # Check for quota exceeded error
            error_str = str(e)
            if "quota" in error_str.lower() or "insufficient_quota" in error_str:
                self.is_api_available = False  # Mark API as unavailable
                return self._generate_fallback_summary(text, detail_level, 
                    error_message="OpenAI API quota exceeded. Using basic summary instead.")
            # For other tesseract errors
            elif "tesseract" in error_str.lower():
                raise Exception(
                    "OCR processing error. There was an issue with the document recognition. "
                    "Please try a clearer document or a different file format."
                )
            else:
                self.is_api_available = False  # Mark API as unavailable for other errors
                return self._generate_fallback_summary(text, detail_level,
                    error_message=f"OpenAI API error: {error_str}")
                
    def _generate_fallback_summary(self, text, detail_level, error_message=None):
        """
        Generate a basic summary when OpenAI API is not available
        
        Args:
            text (str): The legal document text
            detail_level (str): 'simple' or 'detailed' summary level
            error_message (str, optional): Error message to include
            
        Returns:
            str: Basic summary of the document
        """
        # Create a header with the error message if provided
        header = f"⚠️ **API Unavailable**: {error_message}\n\n" if error_message else ""
        
        # Calculate some basic statistics about the document
        word_count = len(text.split())
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        
        # Extract the first few sentences as a simple summary
        sentences = text.replace('\n', ' ').replace('  ', ' ').split('.')
        intro_sentences = sentences[:3] if len(sentences) > 3 else sentences
        intro_text = '. '.join(intro_sentences)
        if len(intro_text) > 0 and not intro_text.endswith('.'):
            intro_text += '.'
            
        # Find potential key terms (simple frequency-based approach)
        words = [word.lower() for word in text.split() if len(word) > 4]
        word_freq = {}
        for word in words:
            if word not in word_freq:
                word_freq[word] = 0
            word_freq[word] += 1
            
        # Get top words by frequency
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        key_terms = ", ".join([word for word, _ in top_words])
        
        # Format the basic summary
        if detail_level == "simple":
            summary = f"{header}**Basic Document Analysis**\n\n"
            summary += f"This document contains approximately {word_count} words and {sentence_count} sentences.\n\n"
            summary += f"**Document Preview**: {intro_text}\n\n"
            summary += f"**Frequent Terms**: {key_terms}\n\n"
            summary += "To get a proper AI-powered summary, please update the OpenAI API key."
        else:  # detailed
            summary = f"{header}**Basic Document Analysis**\n\n"
            summary += f"**Document Statistics**:\n- Word Count: {word_count}\n- Sentence Count: {sentence_count}\n\n"
            summary += f"**Document Introduction**:\n{intro_text}\n\n"
            summary += f"**Key Terms** (by frequency):\n{key_terms}\n\n"
            
            # Try to extract some specific legal sections based on common headings
            legal_sections = ["PURPOSE", "SCOPE", "DEFINITIONS", "AGREEMENT", "TERMS", "CONDITIONS", 
                              "OBLIGATIONS", "RIGHTS", "GOVERNING LAW", "JURISDICTION"]
            
            found_sections = []
            for section in legal_sections:
                if section in text.upper():
                    # Find the position of the section
                    pos = text.upper().find(section)
                    # Extract a snippet (200 chars) from that position
                    snippet = text[pos:pos+200].replace('\n', ' ').strip()
                    found_sections.append(f"**{section.title()}**: {snippet}...")
            
            if found_sections:
                summary += "**Detected Sections**:\n" + "\n\n".join(found_sections) + "\n\n"
                
            summary += "Note: This is a basic analysis produced without AI. For full AI-powered summarization, please provide a valid OpenAI API key."
        
        return summary
