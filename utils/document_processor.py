import os
import io
import PyPDF2
import docx
import tempfile
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import numpy as np

def read_pdf(pdf_file):
    """
    Extract text from PDF file, uses OCR if needed
    
    Args:
        pdf_file: uploaded PDF file object
    
    Returns:
        str: Extracted text content
    """
    try:
        # First try regular text extraction
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            text += page_text if page_text else ""

        # If meaningful text was extracted, return it
        if len(text.strip()) > 100:  # Assume if we have decent amount of text, extraction worked
            return text
            
        # If very little text was extracted, it might be a scanned document
        # Try OCR on the first few pages
        pdf_file.seek(0)  # Reset file pointer
        return extract_text_with_ocr(pdf_file)
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")

def extract_text_with_ocr(pdf_file):
    """
    Extract text from scanned PDF using OCR
    
    Args:
        pdf_file: PDF file object
    
    Returns:
        str: Extracted text using OCR
    """
    try:
        # Check if tesseract is available
        try:
            pytesseract.get_tesseract_version()
        except Exception:
            return """OCR processing requires Tesseract to be installed.
            This demo environment may not have Tesseract OCR fully configured.
            Please try uploading a document with embedded text."""
        
        # Convert PDF to images
        images = convert_from_bytes(pdf_file.getvalue(), dpi=300, first_page=1, last_page=5)
        
        text = ""
        for i, image in enumerate(images):
            # Use pytesseract to extract text
            page_text = pytesseract.image_to_string(image)
            text += f"\n--- Page {i+1} ---\n{page_text}\n"
            
            # Only process a few pages to avoid overloading
            if i >= 4:  # Process up to 5 pages
                text += "\n[Document truncated for processing efficiency]"
                break
        
        # Check if OCR produced meaningful text
        if len(text.strip()) < 50:
            text += "\n\n[Warning: OCR may not have extracted text properly. Please try a clearer document or a different format.]"
                
        return text
    except Exception as e:
        error_msg = str(e)
        if "poppler" in error_msg.lower():
            return """PDF to image conversion requires poppler to be installed.
            This demo environment may not have all required components configured.
            Please try uploading a document in another format like DOCX or TXT."""
        else:
            raise Exception(f"OCR processing error: {error_msg}")

def read_docx(docx_file):
    """
    Extract text from DOCX file
    
    Args:
        docx_file: uploaded DOCX file object
    
    Returns:
        str: Extracted text content
    """
    tmp_path = None
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
        if tmp_path:
            os.unlink(tmp_path)
        return text
    except Exception as e:
        # Clean up temp file in case of exception
        if tmp_path and os.path.exists(tmp_path):
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

def process_image(image_file):
    """
    Extract text from an image file using OCR
    
    Args:
        image_file: uploaded image file object
    
    Returns:
        str: Extracted text content
    """
    try:
        # Check if tesseract is available first
        try:
            pytesseract.get_tesseract_version()
        except Exception:
            return """OCR processing requires Tesseract to be installed.
            This demo environment may not have Tesseract OCR fully configured.
            Please try uploading a document with embedded text (like PDF or DOCX)."""
            
        # Open the image using PIL
        image = Image.open(image_file)
        
        # Use pytesseract for OCR
        text = pytesseract.image_to_string(image)
        
        # Check if OCR produced meaningful text
        if len(text.strip()) < 20:
            text += "\n\n[Warning: OCR may not have extracted text properly. Please try a clearer image or a different format.]"
        
        return text
    except Exception as e:
        error_msg = str(e)
        if "tesseract" in error_msg.lower():
            return """OCR processing requires Tesseract to be installed.
            This demo environment may not have Tesseract OCR fully configured.
            Please try uploading a document with embedded text (like PDF or DOCX)."""
        else:
            raise Exception(f"Error processing image with OCR: {error_msg}")

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
    elif file_type in ['jpg', 'jpeg', 'png', 'tiff', 'tif', 'bmp']:
        return process_image(uploaded_file)
    else:
        raise ValueError(f"Unsupported file format: {file_type}. Please upload PDF, DOCX, TXT, or image files.")
