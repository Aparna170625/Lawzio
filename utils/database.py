"""
Database module for storing document history and analysis results
with encryption support for enhanced privacy
"""
import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import logging
from utils.encryption import DocumentEncryption, anonymize_text, generate_document_token

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize encryption
encryption = DocumentEncryption()

# Database connection parameters from environment variables
DB_PARAMS = {
    "dbname": os.environ.get("PGDATABASE"),
    "user": os.environ.get("PGUSER"),
    "password": os.environ.get("PGPASSWORD"),
    "host": os.environ.get("PGHOST"),
    "port": os.environ.get("PGPORT")
}

def get_connection():
    """
    Get a connection to the database
    
    Returns:
        connection: psycopg2 connection object
    """
    try:
        connection = psycopg2.connect(**DB_PARAMS)
        return connection
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

def save_document_history(filename, file_size_kb, document_language, risk_level, content_length, 
                         risk_factors=None, document_text=None, privacy_level='standard'):
    """
    Save document history to the database with encryption support
    
    Args:
        filename (str): Name of the uploaded file
        file_size_kb (float): Size of the file in KB
        document_language (str): Detected language of the document
        risk_level (str): Assessed risk level (Low, Medium, High)
        content_length (int): Number of characters in the document
        risk_factors (list, optional): List of identified risk factors
        document_text (str, optional): The full document text (will be encrypted if privacy_level requires)
        privacy_level (str): Privacy level ('standard', 'enhanced', 'maximum')
        
    Returns:
        int: ID of the created record or None if failed
    """
    if risk_factors is None:
        risk_factors = []
        
    connection = get_connection()
    if not connection:
        return None
        
    try:
        with connection:
            with connection.cursor() as cursor:
                # Generate access token for document retrieval
                access_token = generate_document_token()
                is_encrypted = False
            
                # Encrypt document text if provided and privacy level requires it
                encrypted_document_text = None
                if document_text and privacy_level in ['enhanced', 'maximum']:
                    encrypted_document_text = encryption.encrypt(document_text)
                    is_encrypted = True
                elif document_text:
                    encrypted_document_text = document_text  # Store unencrypted
                
                # Apply text anonymization for maximum privacy level
                anonymized_factors = risk_factors.copy()
                if privacy_level == 'maximum' and risk_factors:
                    anonymized_factors = []
                    for factor in risk_factors:
                        anonymized_factors.append(anonymize_text(factor))
                
                # Insert document history with encryption fields
                cursor.execute(
                    """
                    INSERT INTO document_history 
                    (filename, file_size_kb, document_language, risk_level, content_length, 
                     document_text, is_encrypted, access_token, privacy_level)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                    """,
                    (filename, file_size_kb, document_language, risk_level, content_length,
                     encrypted_document_text, is_encrypted, access_token, privacy_level)
                )
                document_id = cursor.fetchone()[0]
                
                # Insert risk factors if any
                if anonymized_factors:
                    for factor in anonymized_factors:
                        cursor.execute(
                            """
                            INSERT INTO risk_factors (document_id, risk_factor)
                            VALUES (%s, %s)
                            """,
                            (document_id, factor)
                        )
                
                # Save privacy settings
                retention_days = 7 if privacy_level == 'maximum' else 30
                anonymize = True if privacy_level == 'maximum' else False
                encrypt_storage = True if privacy_level in ['enhanced', 'maximum'] else False
                
                cursor.execute(
                    """
                    INSERT INTO privacy_settings
                    (document_id, privacy_level, retention_days, anonymize_text, encrypt_storage, access_token)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """, 
                    (document_id, privacy_level, retention_days, anonymize, encrypt_storage, access_token)
                )
                
                return document_id
    except Exception as e:
        logger.error(f"Error saving document history: {e}")
        return None
    finally:
        connection.close()

def save_document_summary(document_id, summary_text, detail_level, language="english"):
    """
    Save document summary to the database with encryption if needed
    
    Args:
        document_id (int): ID of the document in document_history
        summary_text (str): The generated summary text
        detail_level (str): Level of detail (simple or detailed)
        language (str): Language of the summary
        
    Returns:
        int: ID of the created summary or None if failed
    """
    connection = get_connection()
    if not connection:
        return None
        
    try:
        with connection:
            with connection.cursor() as cursor:
                # Check document's privacy level
                cursor.execute(
                    """
                    SELECT privacy_level FROM document_history
                    WHERE id = %s
                    """,
                    (document_id,)
                )
                
                result = cursor.fetchone()
                if not result:
                    return None
                
                privacy_level = result[0] if result[0] else 'standard'
                is_encrypted = False
                encrypted_summary = summary_text
                
                # Encrypt summary if privacy level requires it
                if privacy_level in ['enhanced', 'maximum']:
                    encrypted_summary = encryption.encrypt(summary_text)
                    is_encrypted = True
                
                cursor.execute(
                    """
                    INSERT INTO document_summaries 
                    (document_id, summary_text, detail_level, language, is_encrypted)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                    """,
                    (document_id, encrypted_summary, detail_level, language, is_encrypted)
                )
                return cursor.fetchone()[0]
    except Exception as e:
        logger.error(f"Error saving document summary: {e}")
        return None
    finally:
        connection.close()

def get_recent_documents(limit=10):
    """
    Get recent document history
    
    Args:
        limit (int): Maximum number of records to return
        
    Returns:
        list: List of recent document history records
    """
    connection = get_connection()
    if not connection:
        return []
        
    try:
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM document_history
                    ORDER BY upload_date DESC
                    LIMIT %s
                    """,
                    (limit,)
                )
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error getting recent documents: {e}")
        return []
    finally:
        connection.close()

def get_document_with_risk_factors(document_id):
    """
    Get document history with its risk factors
    
    Args:
        document_id (int): ID of the document
        
    Returns:
        dict: Document record with risk factors list
    """
    connection = get_connection()
    if not connection:
        return None
        
    try:
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Get document
                cursor.execute(
                    """
                    SELECT * FROM document_history
                    WHERE id = %s
                    """,
                    (document_id,)
                )
                document = cursor.fetchone()
                
                if not document:
                    return None
                    
                # Get risk factors
                cursor.execute(
                    """
                    SELECT risk_factor FROM risk_factors
                    WHERE document_id = %s
                    """,
                    (document_id,)
                )
                risk_factors = [row['risk_factor'] for row in cursor.fetchall()]
                
                document['risk_factors'] = risk_factors
                
                # Decrypt document_text if it exists and is encrypted
                if document.get('document_text') and document.get('is_encrypted'):
                    try:
                        document['document_text'] = encryption.decrypt(document['document_text'])
                    except Exception as e:
                        logger.error(f"Error decrypting document text: {e}")
                        document['document_text'] = "[Encrypted content - decryption failed]"
                
                return document
    except Exception as e:
        logger.error(f"Error getting document with risk factors: {e}")
        return None
    finally:
        connection.close()
        
def get_document_text(document_id):
    """
    Get the full document text, decrypting if necessary
    
    Args:
        document_id (int): ID of the document
        
    Returns:
        str: Decrypted document text or None
    """
    connection = get_connection()
    if not connection:
        return None
        
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT document_text, is_encrypted 
                    FROM document_history
                    WHERE id = %s
                    """,
                    (document_id,)
                )
                
                result = cursor.fetchone()
                if not result or not result[0]:
                    return None
                    
                document_text, is_encrypted = result
                
                # Decrypt if encrypted
                if is_encrypted:
                    try:
                        return encryption.decrypt(document_text)
                    except Exception as e:
                        logger.error(f"Error decrypting document text: {e}")
                        return "[Encrypted content - decryption failed]"
                else:
                    return document_text
                
    except Exception as e:
        logger.error(f"Error getting document text: {e}")
        return None
    finally:
        connection.close()

def get_document_summaries(document_id):
    """
    Get all summaries for a document, decrypting if necessary
    
    Args:
        document_id (int): ID of the document
        
    Returns:
        list: List of summary records with decrypted content
    """
    connection = get_connection()
    if not connection:
        return []
        
    try:
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM document_summaries
                    WHERE document_id = %s
                    ORDER BY generation_date DESC
                    """,
                    (document_id,)
                )
                summaries = cursor.fetchall()
                
                # Check for encryption and decrypt if needed
                for summary in summaries:
                    if summary.get('is_encrypted') and summary.get('summary_text'):
                        try:
                            summary['summary_text'] = encryption.decrypt(summary['summary_text'])
                        except Exception as e:
                            logger.error(f"Error decrypting summary: {e}")
                            summary['summary_text'] = "[Encrypted content - decryption failed]"
                
                return summaries
    except Exception as e:
        logger.error(f"Error getting document summaries: {e}")
        return []
    finally:
        connection.close()

def get_privacy_settings(document_id):
    """
    Get privacy settings for a document
    
    Args:
        document_id (int): ID of the document
        
    Returns:
        dict: Privacy settings or None if not found
    """
    connection = get_connection()
    if not connection:
        return None
        
    try:
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM privacy_settings
                    WHERE document_id = %s
                    """,
                    (document_id,)
                )
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error getting privacy settings: {e}")
        return None
    finally:
        connection.close()

def update_privacy_settings(document_id, privacy_level=None, retention_days=None, 
                          anonymize_text=None, encrypt_storage=None):
    """
    Update privacy settings for a document
    
    Args:
        document_id (int): ID of the document
        privacy_level (str, optional): Privacy level
        retention_days (int, optional): Data retention period in days
        anonymize_text (bool, optional): Whether to anonymize text
        encrypt_storage (bool, optional): Whether to encrypt storage
        
    Returns:
        bool: Success or failure
    """
    connection = get_connection()
    if not connection:
        return False
        
    try:
        with connection:
            with connection.cursor() as cursor:
                # Only update provided fields
                update_fields = []
                params = []
                
                if privacy_level is not None:
                    update_fields.append("privacy_level = %s")
                    params.append(privacy_level)
                    
                if retention_days is not None:
                    update_fields.append("retention_days = %s")
                    params.append(retention_days)
                    
                if anonymize_text is not None:
                    update_fields.append("anonymize_text = %s")
                    params.append(anonymize_text)
                    
                if encrypt_storage is not None:
                    update_fields.append("encrypt_storage = %s")
                    params.append(encrypt_storage)
                    
                if not update_fields:
                    return False
                    
                # Add document_id to params
                params.append(document_id)
                
                cursor.execute(f"""
                    UPDATE privacy_settings 
                    SET {', '.join(update_fields)}
                    WHERE document_id = %s
                """, tuple(params))
                
                # Also update document_history privacy_level if provided
                if privacy_level is not None:
                    cursor.execute("""
                        UPDATE document_history
                        SET privacy_level = %s
                        WHERE id = %s
                    """, (privacy_level, document_id))
                
                return True
    except Exception as e:
        logger.error(f"Error updating privacy settings: {e}")
        return False
    finally:
        connection.close()

def delete_document_by_token(access_token):
    """
    Delete a document and all related data using its access token
    
    Args:
        access_token (str): Document access token
        
    Returns:
        bool: Success or failure
    """
    connection = get_connection()
    if not connection:
        return False
        
    try:
        with connection:
            with connection.cursor() as cursor:
                # Find document_id by token
                cursor.execute("""
                    SELECT id FROM document_history
                    WHERE access_token = %s
                """, (access_token,))
                
                result = cursor.fetchone()
                if not result:
                    return False
                    
                document_id = result[0]
                
                # Delete risk factors
                cursor.execute("""
                    DELETE FROM risk_factors
                    WHERE document_id = %s
                """, (document_id,))
                
                # Delete summaries
                cursor.execute("""
                    DELETE FROM document_summaries
                    WHERE document_id = %s
                """, (document_id,))
                
                # Delete privacy settings
                cursor.execute("""
                    DELETE FROM privacy_settings
                    WHERE document_id = %s
                """, (document_id,))
                
                # Delete document
                cursor.execute("""
                    DELETE FROM document_history
                    WHERE id = %s
                """, (document_id,))
                
                return True
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        return False
    finally:
        connection.close()