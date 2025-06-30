# JobTailor - Resume & Cover Letter Automation

Local-first AI-powered tool that tailors resumes and cover letters for job applications.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   - Copy `.env.template` to `.env`
   - Add your `GEMINI_API_KEY` to `.env`

3. **Run:**
   ```python
   from main import JobTailor
   
   tailor = JobTailor()
   output_path = tailor.process_job_application(job_description_text)
   ```

## Features

- **Gemini AI extraction** - Parses job descriptions into structured data
- **Smart folder naming** - `Company_Role_YYYY-MM-DDTHHMM` format
- **Complete outputs** - Tailored resume, cover letter, job analysis, metadata
- **Modular design** - Easy to extend with different AI models

## Output Structure

Each run creates a timestamped folder containing:
- `job_description.txt` - Original job posting
- `job_analysis.json` - Extracted company, role, skills data
- `tailored_resume.json` - Customized resume
- `cover_letter.txt` - Generated cover letter
- `metadata.json` - Run information and success metrics

## Next Steps

- Implement actual AI model integration for resume tailoring
- Add CLI interface
- Support URL job description fetching
- Add more AI model providers
