import os
import json
import requests
from typing import Dict, Any, Optional

class GeminiJobExtractor:
    """Extract structured job information using Google Gemini API"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    def extract_job_details(self, job_description: str) -> Dict[str, Any]:
        """
        Extract structured job information from job description text
        
        Args:
            job_description: Raw job description text
            
        Returns:
            Dictionary with extracted job details
        """
        prompt = self._build_extraction_prompt(job_description)
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.1,  # Low temperature for consistent extraction
                "maxOutputTokens": 1000
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers={'Content-Type': 'application/json'},
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            content = result['candidates'][0]['content']['parts'][0]['text']
            
            # Parse the JSON response
            extracted_data = json.loads(content.strip())
            return extracted_data
            
        except requests.RequestException as e:
            print(f"API request failed: {e}")
            return self._get_fallback_structure()
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Failed to parse API response: {e}")
            return self._get_fallback_structure()
    
    def _build_extraction_prompt(self, job_description: str) -> str:
        """Build the prompt for job information extraction"""
        return f"""
Extract the following information from this job description and return ONLY valid JSON:

{{
  "company_name": "string or null",
  "job_title": "string or null", 
  "location": "string or null",
  "work_type": "remote/hybrid/onsite or null",
  "employment_type": "full-time/part-time/contract/freelance or null",
  "salary_range": "string or null",
  "experience_level": "entry/mid/senior/lead/executive or null",
  "required_skills": ["array of key required skills"],
  "nice_to_have_skills": ["array of preferred skills"],
  "key_responsibilities": ["array of main responsibilities"],
  "education_requirements": "string or null",
  "industry": "string or null",
  "team_size": "string or null",
  "reporting_to": "string or null"
}}

Rules:
- Return ONLY the JSON object, no other text
- Use null for missing information, don't guess
- Keep skill lists focused on the most important items
- Extract exact salary ranges when mentioned
- Identify the most likely job title if multiple are mentioned

Job Description:
{job_description}
"""
    
    def _get_fallback_structure(self) -> Dict[str, Any]:
        """Return empty structure if extraction fails"""
        return {
            "company_name": None,
            "job_title": None,
            "location": None,
            "work_type": None,
            "employment_type": None,
            "salary_range": None,
            "experience_level": None,
            "required_skills": [],
            "nice_to_have_skills": [],
            "key_responsibilities": [],
            "education_requirements": None,
            "industry": None,
            "team_size": None,
            "reporting_to": None,
            "extraction_failed": True
        }

# Usage example:
if __name__ == "__main__":
    # Test with sample job description
    sample_job = """
    Senior Software Engineer - Backend
    TechCorp Inc.
    
    We're looking for a Senior Software Engineer to join our backend team in Sydney, Australia.
    This is a full-time remote position with occasional office visits.
    
    Requirements:
    - 5+ years Python experience
    - Experience with AWS and microservices
    - Strong SQL skills
    
    Nice to have:
    - Docker experience
    - Previous startup experience
    
    Salary: $120,000 - $150,000 AUD
    """
    
    extractor = GeminiJobExtractor()
    result = extractor.extract_job_details(sample_job)
    print(json.dumps(result, indent=2))
