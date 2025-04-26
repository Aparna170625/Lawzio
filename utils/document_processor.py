import os
import io
import PyPDF2
import docx
import tempfile

def read_pdf(pdf_file):
    """
    Extract text from PDF file
    
    Args:
        pdf_file: uploaded PDF file object
    
    Returns:
        str: Extracted text content
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")

def read_docx(docx_file):
    """
    Extract text from DOCX file
    
    Args:
        docx_file: uploaded DOCX file object
    
    Returns:
        str: Extracted text content
    """
    try:
        # Create a temporary file to save the uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
            tmp_file.write(docx_file.getvalue())
            tmp_path = tmp_file.name
        
        # Open the temporary file with python-docx
        doc = docx.Document(tmp_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        # Clean up the temporary file
        os.unlink(tmp_path)
        return text
    except Exception as e:
        # Clean up temp file in case of exception
        if 'tmp_path' in locals():
            os.unlink(tmp_path)
        raise Exception(f"Error processing DOCX: {str(e)}")

def read_txt(txt_file):
    """
    Extract text from TXT file
    
    Args:
        txt_file: uploaded TXT file object
    
    Returns:
        str: Extracted text content
    """
    try:
        content = txt_file.getvalue().decode("utf-8")
        return content
    except Exception as e:
        raise Exception(f"Error processing TXT: {str(e)}")

def process_document(uploaded_file):
    """
    Process document based on file type
    
    Args:
        uploaded_file: The uploaded file object
    
    Returns:
        str: Extracted text content
    """
    if uploaded_file is None:
        return None
    
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    if file_type == 'pdf':
        return read_pdf(uploaded_file)
    elif file_type == 'docx':
        return read_docx(uploaded_file)
    elif file_type == 'txt':
        return read_txt(uploaded_file)
    else:
        raise ValueError(f"Unsupported file format: {file_type}. Please upload PDF, DOCX, or TXT files.")
