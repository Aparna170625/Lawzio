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
                
        return text
    except Exception as e:
        raise Exception(f"OCR processing error: {str(e)}")

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

def process_image(image_file):
    """
    Extract text from an image file using OCR
    
    Args:
        image_file: uploaded image file object
    
    Returns:
        str: Extracted text content
    """
    try:
        # Open the image using PIL
        image = Image.open(image_file)
        
        # Use pytesseract for OCR
        text = pytesseract.image_to_string(image)
        
        return text
    except Exception as e:
        raise Exception(f"Error processing image with OCR: {str(e)}")

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
