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
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=api_key)
    
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
            raise Exception(f"OpenAI API error: {str(e)}")
