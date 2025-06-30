import os
import json
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class JobTailor:
    """
    Main orchestrator for resume and cover letter tailoring
    """
    
    def __init__(self, output_base_path: str = None):
        self.output_base_path = output_base_path or os.getenv('OUTPUT_BASE_PATH', './output')
        self.resume_template_path = './resume_template.json'
        
        # Ensure output directory exists
        os.makedirs(self.output_base_path, exist_ok=True)
    
    def process_job_application(self, job_description: str, model_provider: str = 'openai') -> str:
        """
        Main workflow: analyze job, tailor resume, generate cover letter
        
        Args:
            job_description: Raw job description text
            model_provider: AI model to use ('openai', 'anthropic', 'local')
            
        Returns:
            Path to output folder containing all generated files
        """
        print("🔍 Analyzing job description...")
        job_analysis = self.analyze_job_description(job_description)
        
        print("📁 Creating output folder...")
        output_folder = self.create_output_folder(job_analysis)
        
        print("📄 Loading base resume...")
        base_resume = self.load_resume_template()
        
        print("✨ Tailoring resume...")
        tailored_resume = self.tailor_resume(base_resume, job_analysis, model_provider)
        
        print("✍️ Generating cover letter...")
        cover_letter = self.generate_cover_letter(base_resume, job_analysis, model_provider)
        
        print("💾 Saving outputs...")
        self.save_outputs(output_folder, {
            'job_description': job_description,
            'job_analysis': job_analysis,
            'tailored_resume': tailored_resume,
            'cover_letter': cover_letter
        })
        
        print(f"✅ Complete! Files saved to: {output_folder}")
        return output_folder
    
    def analyze_job_description(self, job_description: str) -> Dict[str, Any]:
        """
        Analyze job description to extract key requirements and details using Gemini API
        """
        print("🔍 Calling Gemini API for job extraction...")
        try:
            from gemini_extractor import GeminiJobExtractor
            extractor = GeminiJobExtractor()
            result = extractor.extract_job_details(job_description)
            print(f"✅ Gemini extraction result: {result}")
            return result
        except Exception as e:
            print(f"❌ Job extraction failed: {e}")
            # Fallback to basic structure
            return {
                "company_name": "Unknown Company",
                "job_title": "Unknown Position",
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
    
    def create_output_folder(self, job_analysis: Dict[str, Any]) -> str:
        """Create timestamped output folder based on company and role"""
        timestamp = datetime.now().strftime("%Y-%m-%dT%H%M")
        
        # Clean company and job title for folder name
        company = job_analysis.get('company_name', 'Unknown_Company')
        job_title = job_analysis.get('job_title', 'Unknown_Position')
        
        # Sanitize for folder names
        company = self._sanitize_filename(company)
        job_title = self._sanitize_filename(job_title)
        
        folder_name = f"{company}_{job_title}_{timestamp}"
        folder_path = os.path.join(self.output_base_path, folder_name)
        
        os.makedirs(folder_path, exist_ok=True)
        return folder_path
    
    def _sanitize_filename(self, filename: str) -> str:
        """Remove invalid characters from filename"""
        import re
        # Handle None or empty strings
        if not filename:
            return "Unknown"
        
        # Replace invalid chars with underscore
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', str(filename))
        # Replace spaces with underscores
        sanitized = sanitized.replace(' ', '_')
        # Remove multiple underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        # Trim underscores from ends
        return sanitized.strip('_')[:50]  # Limit length
    
    def load_resume_template(self) -> Dict[str, Any]:
        """Load the base resume JSON template"""
        try:
            with open(self.resume_template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Resume template not found at {self.resume_template_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in resume template: {e}")
    
    def tailor_resume(self, base_resume: Dict[str, Any], job_analysis: Dict[str, Any], model_provider: str) -> Dict[str, Any]:
        """
        Tailor resume content based on job requirements
        """
        # TODO: Implement actual AI model calling
        # For now, return the base resume with minimal modifications
        
        tailored = base_resume.copy()
        
        # Add job targeting info to summary if we have good extraction
        if not job_analysis.get('extraction_failed', False):
            company = job_analysis.get('company_name', '')
            role = job_analysis.get('job_title', '')
            if company and role:
                tailored['targeting'] = {
                    'company': company,
                    'role': role,
                    'tailored_date': datetime.now().isoformat()
                }
        
        print(f"Resume tailored using {model_provider} model")
        return tailored
    
    def generate_cover_letter(self, base_resume: Dict[str, Any], job_analysis: Dict[str, Any], model_provider: str) -> str:
        """
        Generate a tailored cover letter
        """
        # TODO: Implement actual AI model calling
        # For now, return a basic template
        
        name = base_resume.get('personal_info', {}).get('name', 'Steven Waters')
        company = job_analysis.get('company_name', 'the company')
        role = job_analysis.get('job_title', 'this position')
        
        cover_letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {role} position at {company}.

With over 20 years of experience in project management, solution delivery, and technology leadership, I am confident that my background aligns well with your requirements.

Key highlights of my experience:
• Chief Product Officer at Outstaffer, leading product strategy and team scaling
• General Manager Technology at Certane, managing strategic technology transitions
• Extensive experience in SaaS development, cloud technologies, and stakeholder management

I would welcome the opportunity to discuss how my experience can contribute to {company}'s continued success.

Thank you for your consideration.

Best regards,
{name}"""

        print(f"Cover letter generated using {model_provider} model")
        return cover_letter
    
    def save_outputs(self, output_folder: str, outputs: Dict[str, Any]) -> None:
        """Save all generated files to the output folder"""
        
        # Save original job description
        with open(os.path.join(output_folder, 'job_description.txt'), 'w', encoding='utf-8') as f:
            f.write(outputs['job_description'])
        
        # Save job analysis
        with open(os.path.join(output_folder, 'job_analysis.json'), 'w', encoding='utf-8') as f:
            json.dump(outputs['job_analysis'], f, indent=2, ensure_ascii=False)
        
        # Save tailored resume
        with open(os.path.join(output_folder, 'tailored_resume.json'), 'w', encoding='utf-8') as f:
            json.dump(outputs['tailored_resume'], f, indent=2, ensure_ascii=False)
        
        # Save cover letter
        with open(os.path.join(output_folder, 'cover_letter.txt'), 'w', encoding='utf-8') as f:
            f.write(outputs['cover_letter'])
        
        # Save metadata
        metadata = {
            'generated_at': datetime.now().isoformat(),
            'company': outputs['job_analysis'].get('company_name'),
            'role': outputs['job_analysis'].get('job_title'),
            'extraction_successful': not outputs['job_analysis'].get('extraction_failed', False)
        }
        with open(os.path.join(output_folder, 'metadata.json'), 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # Read job description from job.txt
    try:
        with open('job.txt', 'r', encoding='utf-8') as f:
            job_desc = f.read().strip()
        
        if not job_desc:
            print("❌ job.txt is empty. Please add a job description.")
            exit(1)
            
        print("📋 Processing job from job.txt...")
        tailor = JobTailor()
        output_path = tailor.process_job_application(job_desc, model_provider='openai')
        print(f"✅ Results saved to: {output_path}")
        
    except FileNotFoundError:
        print("❌ job.txt not found. Please create it with a job description.")
        exit(1)
