"""
Encryption and privacy module for the Lawzio application
Provides secure encryption/decryption for document storage and processing
"""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets
import hashlib
import uuid

# This is used as a fallback if no encryption key is provided
DEFAULT_SALT = b'lawzio_default_salt_value'

class DocumentEncryption:
    """
    Handles document encryption and decryption using Fernet symmetric encryption
    """
    def __init__(self, master_key=None):
        """
        Initialize the encryption system with a master key
        
        Args:
            master_key (str, optional): Master encryption key. If not provided, 
                                       a default key will be generated.
        """
        # Generate or use provided master key
        if master_key:
            self.master_key = master_key
        else:
            # Use environment variable if available, otherwise generate a random key
            self.master_key = os.environ.get('ENCRYPTION_KEY')
            if not self.master_key:
                self.master_key = secrets.token_hex(16)
        
        # Convert the master key to bytes
        master_key_bytes = self.master_key.encode('utf-8')
        
        # Generate a key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=DEFAULT_SALT,
            iterations=100000,
        )
        
        # Derive the key
        key = base64.urlsafe_b64encode(kdf.derive(master_key_bytes))
        self.cipher = Fernet(key)
    
    def encrypt(self, data):
        """
        Encrypt string data
        
        Args:
            data (str): Data to encrypt
            
        Returns:
            str: Base64 encoded encrypted data
        """
        if not data:
            return None
            
        # Convert string to bytes
        data_bytes = data.encode('utf-8')
        
        # Encrypt the data
        encrypted_data = self.cipher.encrypt(data_bytes)
        
        # Return base64 encoded string
        return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
    
    def decrypt(self, encrypted_data):
        """
        Decrypt encrypted data
        
        Args:
            encrypted_data (str): Base64 encoded encrypted data
            
        Returns:
            str: Decrypted data as string
        """
        if not encrypted_data:
            return None
            
        try:
            # Convert from base64 to bytes
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            
            # Decrypt the data
            decrypted_bytes = self.cipher.decrypt(encrypted_bytes)
            
            # Return as string
            return decrypted_bytes.decode('utf-8')
        except Exception as e:
            # If decryption fails, return error message
            return f"[Decryption failed: {str(e)}]"

def anonymize_text(text, patterns=None):
    """
    Anonymize sensitive information in text using pattern matching
    
    Args:
        text (str): Text to anonymize
        patterns (dict, optional): Dictionary of regex patterns and replacement text
        
    Returns:
        str: Anonymized text
    """
    import re
    
    if not text:
        return text
        
    # Default patterns to anonymize
    default_patterns = {
        # Phone numbers (various formats)
        r'\b(?:\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b': '[PHONE]',
        
        # Email addresses
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b': '[EMAIL]',
        
        # Social Security Numbers (US format)
        r'\b\d{3}[-]?\d{2}[-]?\d{4}\b': '[SSN]',
        
        # Credit card numbers (basic pattern)
        r'\b(?:\d{4}[- ]?){4}|\d{16}\b': '[CREDIT_CARD]',
        
        # URLs
        r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(/[-\w%.~!$&\'()*+,;=:@/]*)?' : '[URL]',
        
        # IP addresses
        r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b': '[IP_ADDRESS]',
        
        # Dates (various formats)
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b': '[DATE]',
    }
    
    # Use provided patterns if any, otherwise use defaults
    patterns_to_use = patterns if patterns else default_patterns
    
    # Apply each pattern to the text
    for pattern, replacement in patterns_to_use.items():
        text = re.sub(pattern, replacement, text)
    
    return text

def generate_encryption_key():
    """
    Generate a new encryption key
    
    Returns:
        str: Hex encoded encryption key
    """
    return secrets.token_hex(16)

def hash_document_id(document_id):
    """
    Create a hash of the document ID for secure reference
    
    Args:
        document_id: Original document ID
        
    Returns:
        str: Hashed document ID
    """
    if not document_id:
        return None
        
    # Convert to string if not already
    doc_id_str = str(document_id)
    
    # Create hash using SHA-256
    hash_obj = hashlib.sha256(doc_id_str.encode('utf-8'))
    return hash_obj.hexdigest()

def generate_document_token():
    """
    Generate a unique token for document access control
    
    Returns:
        str: Unique document access token
    """
    return str(uuid.uuid4())