import io
import re
import easyocr
import fitz  # PyMuPDF
import numpy as np
from PIL import Image
from typing import Dict, Any, List


class OCREngine:
    """
    OCR Engine for extracting text and structured data from documents
    """
    
    def __init__(self):
        """
        Initialize EasyOCR Reader with English language support
        Falls back to CPU if CUDA is not available
        """
        try:
            # Try to initialize with GPU support
            self.reader = easyocr.Reader(['en'], gpu=True)
            print("OCR Engine initialized with GPU support")
        except Exception as e:
            # Fall back to CPU if GPU is not available
            print(f"GPU not available, using CPU: {e}")
            self.reader = easyocr.Reader(['en'], gpu=False)
            print("OCR Engine initialized with CPU")
    
    def process_file(self, file_bytes: bytes, filename: str) -> List[str]:
        """
        Process uploaded file (PDF or Image) and extract text
        
        Args:
            file_bytes: Raw bytes of the uploaded file
            filename: Name of the file to determine type
            
        Returns:
            List of extracted text strings
        """
        # Determine file type from extension
        file_extension = filename.lower().split('.')[-1]
        
        try:
            if file_extension == 'pdf':
                # Handle PDF files
                image_array = self._pdf_to_image(file_bytes)
            elif file_extension in ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp']:
                # Handle image files
                image_array = self._image_to_array(file_bytes)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
            
            # Extract text using EasyOCR
            # detail=0 returns only text without bounding boxes
            extracted_text = self.reader.readtext(image_array, detail=0)
            
            return extracted_text
            
        except Exception as e:
            print(f"Error processing file: {e}")
            raise
    
    def _pdf_to_image(self, pdf_bytes: bytes) -> np.ndarray:
        """
        Convert first page of PDF to numpy array for OCR
        
        Args:
            pdf_bytes: Raw PDF file bytes
            
        Returns:
            Numpy array representation of the PDF page
        """
        # Open PDF from bytes
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        # Get the first page
        first_page = pdf_document[0]
        
        # Render page to pixmap (image) at 300 DPI for better OCR
        mat = fitz.Matrix(300/72, 300/72)  # 300 DPI scaling
        pixmap = first_page.get_pixmap(matrix=mat)
        
        # Convert pixmap to PIL Image
        img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        
        # Convert PIL Image to numpy array
        image_array = np.array(img)
        
        pdf_document.close()
        
        return image_array
    
    def _image_to_array(self, image_bytes: bytes) -> np.ndarray:
        """
        Convert image bytes to numpy array for OCR
        
        Args:
            image_bytes: Raw image file bytes
            
        Returns:
            Numpy array representation of the image
        """
        # Open image from bytes
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary (handles PNG with alpha, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array
        image_array = np.array(image)
        
        return image_array
    
    def extract_data(self, text_list: List[str]) -> Dict[str, Any]:
        """
        Extract structured data from raw OCR text using regex patterns
        
        Args:
            text_list: List of text strings from OCR
            
        Returns:
            Dictionary containing extracted data and confidence score
        """
        # Combine all text - preserve structure with newlines
        raw_text = " ".join(text_list)
        
        # Also create a version with newlines for better pattern matching
        raw_text_multiline = "\n".join(text_list)
        
        # Initialize extracted data
        extracted_data = {
            "raw_text": raw_text,
            "extracted_gpa": None,
            "extracted_name": None,
            "extracted_balance": None,
            "confidence_score": 0.0
        }
        
        # Track successful extractions for confidence calculation
        successful_extractions = 0
        total_attempts = 3  # GPA, Name, Balance
        
        # ===== 1. EXTRACT GPA/PERCENTAGE =====
        # Multiple comprehensive patterns to catch various formats
        gpa_patterns = [
            # CGPA variations
            r'CGPA[:\s\-]*(\d+\.?\d*)',
            r'\(CGPA\)[:\s\-]*(\d+\.?\d*)',
            r'C\.?G\.?P\.?A\.?[:\s\-]*(\d+\.?\d*)',
            
            # GPA variations
            r'GPA[:\s\-]*(\d+\.?\d*)',
            r'G\.?P\.?A\.?[:\s\-]*(\d+\.?\d*)',
            
            # Grade variations
            r'Grade[:\s\-]*(\d+\.?\d*)',
            r'Final\s+Grade[:\s\-]*(\d+\.?\d*)',
            
            # Percentage variations
            r'Percentage[:\s\-]*(\d+\.?\d*)',
            r'(\d{1,3}\.?\d*)\s*%',
            r'Percent[:\s\-]*(\d+\.?\d*)',
            
            # Score variations
            r'Score[:\s\-]*(\d+\.?\d*)',
            r'Total[:\s\-]*(\d+\.?\d*)'
        ]
        
        for pattern in gpa_patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                gpa_value = match.group(1)
                # Validate it's a reasonable GPA/percentage value
                try:
                    float_val = float(gpa_value)
                    if 0 <= float_val <= 100:  # Valid range
                        extracted_data["extracted_gpa"] = gpa_value
                        successful_extractions += 1
                        break
                except ValueError:
                    continue
        
        # ===== 2. EXTRACT STUDENT NAME =====
        # Multiple name extraction strategies
        name_patterns = [
            # Direct "Name:" pattern
            r'(?:Student\s+)?Name[:\s]+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){1,3})',
            # "Name of Student:" pattern
            r'Name\s+of\s+(?:the\s+)?Student[:\s]+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){1,3})',
            # Candidate name
            r'Candidate[:\s]+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){1,3})'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, raw_text_multiline, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                
                # Clean the name - remove common OCR artifacts and institutional words
                stop_words = ['University', 'College', 'Institute', 'School', 'Department', 
                             'Faculty', 'Of', 'The', 'And', 'CGPA', 'GPA', 'Grade']
                
                # Split name into words and filter
                name_words = name.split()
                cleaned_words = []
                
                for word in name_words:
                    # Stop if we hit a stop word
                    if word in stop_words:
                        break
                    # Only keep words that look like names (capitalized, letters only)
                    if word[0].isupper() and word.isalpha():
                        cleaned_words.append(word)
                
                # Only accept names with 2-4 words
                if 2 <= len(cleaned_words) <= 4:
                    extracted_data["extracted_name"] = " ".join(cleaned_words)
                    successful_extractions += 1
                    break
        
        # ===== 3. EXTRACT FINANCIAL INFORMATION =====
        financial_patterns = [
            # Balance patterns
            r'Balance[:\s]*(?:Rs\.?|INR|₹|\$)\s*([0-9,]+\.?[0-9]*)',
            r'Available\s+Balance[:\s]*(?:Rs\.?|INR|₹|\$)\s*([0-9,]+\.?[0-9]*)',
            r'Current\s+Balance[:\s]*(?:Rs\.?|INR|₹|\$)\s*([0-9,]+\.?[0-9]*)',
            
            # Amount patterns
            r'Amount[:\s]*(?:Rs\.?|INR|₹|\$)\s*([0-9,]+\.?[0-9]*)',
            r'Total[:\s]*(?:Rs\.?|INR|₹|\$)\s*([0-9,]+\.?[0-9]*)',
            
            # Fee patterns
            r'Fee[s]?[:\s]*(?:Rs\.?|INR|₹|\$)\s*([0-9,]+\.?[0-9]*)',
            r'Tuition[:\s]*(?:Rs\.?|INR|₹|\$)\s*([0-9,]+\.?[0-9]*)'
        ]
        
        for pattern in financial_patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                balance = match.group(1).replace(',', '')
                # Validate it's a reasonable amount
                try:
                    float_val = float(balance)
                    if float_val > 0:  # Valid amount
                        extracted_data["extracted_balance"] = balance
                        successful_extractions += 1
                        break
                except ValueError:
                    continue
        
        # ===== CALCULATE CONFIDENCE SCORE =====
        # Base confidence on multiple factors
        
        # Factor 1: Extraction success rate (60% weight)
        extraction_confidence = (successful_extractions / total_attempts) * 0.6
        
        # Factor 2: Text length/quality (20% weight)
        # More text generally means better OCR quality
        text_length_confidence = min(len(raw_text) / 500, 1.0) * 0.2
        
        # Factor 3: Text contains expected keywords (20% weight)
        keywords = ['Name', 'GPA', 'CGPA', 'Grade', 'Student', 'University']
        keyword_count = sum(1 for keyword in keywords if keyword.lower() in raw_text.lower())
        keyword_confidence = min(keyword_count / len(keywords), 1.0) * 0.2
        
        # Total confidence
        total_confidence = extraction_confidence + text_length_confidence + keyword_confidence
        
        extracted_data["confidence_score"] = round(total_confidence, 2)
        
        return extracted_data