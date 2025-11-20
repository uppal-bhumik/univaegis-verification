from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from typing import Union, Dict, Any
from pydantic import BaseModel

from .ocr_engine import OCREngine
from .eligibility import EligibilityEngine


# Initialize Router
router = APIRouter(
    prefix="/api/v1",
    tags=["verification"]
)

# Initialize OCR and Eligibility Engines
ocr_engine = OCREngine()
eligibility_engine = EligibilityEngine()


# Pydantic model for eligibility check request
class EligibilityRequest(BaseModel):
    extracted_gpa: Union[str, float, None]
    ielts_score: Union[float, None]


@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload and process a document (PDF or Image) using OCR
    
    Args:
        file: Uploaded document file
        
    Returns:
        Dictionary containing OCR extracted data
    """
    try:
        # Validate file type
        allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp']
        file_extension = file.filename.lower().split('.')[-1]
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Read file bytes
        file_bytes = await file.read()
        
        # Check if file is empty
        if len(file_bytes) == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty"
            )
        
        # Process file with OCR
        text_list = ocr_engine.process_file(file_bytes, file.filename)
        
        # Extract structured data
        extracted_data = ocr_engine.extract_data(text_list)
        
        return {
            "status": "success",
            "filename": file.filename,
            "data": extracted_data
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle any other errors
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )


@router.post("/check-eligibility")
async def check_eligibility(request: EligibilityRequest = Body(...)) -> Dict[str, Any]:
    """
    Check student eligibility based on GPA and IELTS score
    
    Args:
        request: EligibilityRequest containing extracted_gpa and ielts_score
        
    Returns:
        Dictionary containing eligibility status and reasons
    """
    try:
        # Check eligibility using the eligibility engine
        result = eligibility_engine.check_eligibility(
            extracted_gpa=request.extracted_gpa,
            ielts_score=request.ielts_score
        )
        
        return result
        
    except Exception as e:
        # Handle any errors
        raise HTTPException(
            status_code=500,
            detail=f"Error checking eligibility: {str(e)}"
        )