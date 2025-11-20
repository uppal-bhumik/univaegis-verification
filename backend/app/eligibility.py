from typing import Dict, List, Union, Any


class EligibilityEngine:
    """
    Eligibility Engine for checking student admission requirements
    """
    
    # Eligibility thresholds
    GPA_THRESHOLD = 8.0
    PERCENTAGE_THRESHOLD = 80.0
    IELTS_THRESHOLD = 8.0
    
    def __init__(self):
        """
        Initialize Eligibility Engine
        """
        pass
    
    def check_eligibility(
        self, 
        extracted_gpa: Union[str, float, None], 
        ielts_score: Union[float, None]
    ) -> Dict[str, Any]:
        """
        Check if student meets eligibility criteria based on GPA and IELTS score
        
        Args:
            extracted_gpa: GPA or percentage from OCR (can be string or float)
            ielts_score: IELTS score provided by user
            
        Returns:
            Dictionary with eligibility status and reasons
        """
        reasons = []
        gpa_pass = False
        ielts_pass = False
        
        # Check GPA/Percentage
        if extracted_gpa is None or extracted_gpa == "":
            reasons.append("GPA/Percentage not found in document")
        else:
            gpa_value = self._clean_gpa(extracted_gpa)
            
            if gpa_value is None:
                reasons.append("Unable to parse GPA/Percentage value")
            else:
                # Determine if it's a percentage or GPA
                if gpa_value > 10:
                    # Treat as percentage
                    if gpa_value >= self.PERCENTAGE_THRESHOLD:
                        gpa_pass = True
                        reasons.append(f"Percentage {gpa_value}% meets requirement (>= {self.PERCENTAGE_THRESHOLD}%)")
                    else:
                        reasons.append(f"Percentage {gpa_value}% is below required {self.PERCENTAGE_THRESHOLD}%")
                else:
                    # Treat as GPA
                    if gpa_value >= self.GPA_THRESHOLD:
                        gpa_pass = True
                        reasons.append(f"GPA {gpa_value} meets requirement (>= {self.GPA_THRESHOLD})")
                    else:
                        reasons.append(f"GPA {gpa_value} is below required {self.GPA_THRESHOLD}")
        
        # Check IELTS Score
        if ielts_score is None:
            reasons.append("IELTS score not provided")
        else:
            try:
                ielts_value = float(ielts_score)
                
                if ielts_value >= self.IELTS_THRESHOLD:
                    ielts_pass = True
                    reasons.append(f"IELTS score {ielts_value} meets requirement (>= {self.IELTS_THRESHOLD})")
                else:
                    reasons.append(f"IELTS score {ielts_value} is below required {self.IELTS_THRESHOLD}")
            except (ValueError, TypeError):
                reasons.append("Invalid IELTS score format")
        
        # Student must pass BOTH checks to be eligible
        eligible = gpa_pass and ielts_pass
        
        return {
            "eligible": eligible,
            "reasons": reasons
        }
    
    def _clean_gpa(self, gpa_input: Union[str, float]) -> Union[float, None]:
        """
        Clean and parse GPA value from various formats
        
        Args:
            gpa_input: GPA value as string or float
            
        Returns:
            Cleaned GPA as float, or None if parsing fails
        """
        try:
            # If already a float, return it
            if isinstance(gpa_input, (int, float)):
                return float(gpa_input)
            
            # If string, clean it
            if isinstance(gpa_input, str):
                # Remove common non-numeric characters
                cleaned = gpa_input.strip()
                cleaned = cleaned.replace('%', '')
                cleaned = cleaned.replace(',', '')
                cleaned = cleaned.strip()
                
                # Try to convert to float
                return float(cleaned)
            
            return None
            
        except (ValueError, AttributeError, TypeError):
            return None