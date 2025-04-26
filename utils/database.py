"""
Database module for storing document history and analysis results
"""
import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def save_document_history(filename, file_size_kb, document_language, risk_level, content_length, risk_factors=None):
    """
    Save document history to the database
    
    Args:
        filename (str): Name of the uploaded file
        file_size_kb (float): Size of the file in KB
        document_language (str): Detected language of the document
        risk_level (str): Assessed risk level (Low, Medium, High)
        content_length (int): Number of characters in the document
        risk_factors (list, optional): List of identified risk factors
        
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
                # Insert document history
                cursor.execute(
                    """
                    INSERT INTO document_history 
                    (filename, file_size_kb, document_language, risk_level, content_length)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                    """,
                    (filename, file_size_kb, document_language, risk_level, content_length)
                )
                document_id = cursor.fetchone()[0]
                
                # Insert risk factors if any
                if risk_factors:
                    for factor in risk_factors:
                        cursor.execute(
                            """
                            INSERT INTO risk_factors (document_id, risk_factor)
                            VALUES (%s, %s)
                            """,
                            (document_id, factor)
                        )
                
                return document_id
    except Exception as e:
        logger.error(f"Error saving document history: {e}")
        return None
    finally:
        connection.close()

def save_document_summary(document_id, summary_text, detail_level, language="english"):
    """
    Save document summary to the database
    
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
                cursor.execute(
                    """
                    INSERT INTO document_summaries 
                    (document_id, summary_text, detail_level, language)
                    VALUES (%s, %s, %s, %s) RETURNING id
                    """,
                    (document_id, summary_text, detail_level, language)
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
                return document
    except Exception as e:
        logger.error(f"Error getting document with risk factors: {e}")
        return None
    finally:
        connection.close()

def get_document_summaries(document_id):
    """
    Get all summaries for a document
    
    Args:
        document_id (int): ID of the document
        
    Returns:
        list: List of summary records
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
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error getting document summaries: {e}")
        return []
    finally:
        connection.close()