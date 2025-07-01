import google.generativeai as genai
import json
import os
from pathlib import Path

class GeminiExtractor:
    def __init__(self, api_key=None):
        """Initialize Gemini extractor with API key"""
        if api_key:
            genai.configure(api_key=api_key)
        elif os.getenv('GEMINI_API_KEY'):
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        else:
            raise ValueError("Gemini API key required")

        self.model = genai.GenerativeModel('gemini-pro')
        self.prompt_template = self._load_prompt_template()

    def _load_prompt_template(self):
        """Load the extraction prompt from file"""
        prompt_file = Path(__file__).parent.parent / "prompts" / "extraction_prompt.txt"

        if not prompt_file.exists():
            raise FileNotFoundError(f"Extraction prompt file not found: {prompt_file}")

        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read().strip()

    def extract_job_info(self, job_description):
        """
        Extract structured information from job description

        Args:
            job_description (str): Raw job description text

        Returns:
            dict: Extracted job information with basic_info and personality_signals
        """
        try:
            # Combine prompt template with job description
            full_prompt = f"{self.prompt_template}\n\nJOB DESCRIPTION TO ANALYZE:\n{job_description}"

            # Generate response
            response = self.model.generate_content(full_prompt)

            # Parse JSON response
            result = self._parse_response(response.text)

            # Validate structure
            self._validate_response(result)

            return result

        except Exception as e:
            print(f"Error extracting job info: {str(e)}")
            return self._get_fallback_structure()

    def _parse_response(self, response_text):
        """Parse the AI response and extract JSON"""
        try:
            # Clean up response - remove any markdown formatting
            cleaned = response_text.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned[7:]
            if cleaned.startswith('```'):
                cleaned = cleaned[3:]
            if cleaned.endswith('```'):
                cleaned = cleaned[:-3]

            # Parse JSON
            return json.loads(cleaned)

        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(f"Raw response: {response_text}")
            raise

    def _validate_response(self, result):
        """Validate the response has required structure"""
        required_keys = ['basic_info', 'personality_signals']

        for key in required_keys:
            if key not in result:
                raise ValueError(f"Missing required key: {key}")

        # Validate basic_info structure
        basic_info_keys = ['company', 'job_title', 'key_requirements']
        for key in basic_info_keys:
            if key not in result['basic_info']:
                print(f"Warning: Missing basic_info key: {key}")

        # Validate personality_signals structure
        if not isinstance(result['personality_signals'], list):
            raise ValueError("personality_signals must be a list")

        for signal in result['personality_signals']:
            if not isinstance(signal, dict):
                continue
            required_signal_keys = ['signal', 'context', 'category']
            for key in required_signal_keys:
                if key not in signal:
                    print(f"Warning: Missing signal key: {key}")

    def _get_fallback_structure(self):
        """Return basic structure if extraction fails"""
        return {
            "basic_info": {
                "company": "Unknown",
                "job_title": "Unknown",
                "location": "Unknown",
                "experience_level": "Unknown",
                "industry": "Unknown",
                "key_requirements": [],
                "main_responsibilities": [],
                "technical_skills": []
            },
            "personality_signals": []
        }

# Convenience function for direct usage
def extract_job_description(job_description, api_key=None):
    """
    Extract job information using Gemini

    Args:
        job_description (str): Raw job description text
        api_key (str, optional): Gemini API key

    Returns:
        dict: Extracted job information
    """
    extractor = GeminiExtractor(api_key)
    return extractor.extract_job_info(job_description)