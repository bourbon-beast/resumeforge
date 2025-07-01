#!/usr/bin/env python3
"""
JobTailor - AI-powered resume and cover letter customization tool
"""

import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from gemini_extractor import GeminiExtractor
from models.openai_model import OpenAIModel

load_dotenv()
print(f"Debug: GEMINI_API_KEY = {os.getenv('GEMINI_API_KEY')}")


def load_job_description():
    """Load job description from input file"""
    job_file = Path("input/job.txt")

    if not job_file.exists():
        raise FileNotFoundError(f"Job description file not found: {job_file}")

    with open(job_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        raise ValueError("Job description file is empty")

    return content


def load_resume_data():
    """Load resume JSON data"""
    resume_file = Path("input/resume_template.json")

    if not resume_file.exists():
        raise FileNotFoundError(f"Resume file not found: {resume_file}")

    with open(resume_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_brand_data():
    """Load brand statement JSON data"""
    brand_file = Path("input/brand_statement_json.json")

    if not brand_file.exists():
        raise FileNotFoundError(f"Brand statement file not found: {brand_file}")

    with open(brand_file, "r", encoding="utf-8") as f:
        return json.load(f)


def create_output_folder(job_extraction):
    """Create uniquely named output folder"""
    company = job_extraction.get("basic_info", {}).get("company", "Unknown_Company")
    job_title = job_extraction.get("basic_info", {}).get("job_title", "Unknown_Role")

    # Clean company and job title for folder name
    clean_company = "".join(
        c for c in company if c.isalnum() or c in (" ", "-", "_")
    ).strip()
    clean_title = "".join(
        c for c in job_title if c.isalnum() or c in (" ", "-", "_")
    ).strip()

    # Replace spaces with underscores
    clean_company = clean_company.replace(" ", "_")
    clean_title = clean_title.replace(" ", "_")

    # Create timestamp
    timestamp = datetime.now().strftime("%Y-%m-%dT%H%M")

    # Create folder name
    folder_name = f"{clean_company}_{clean_title}_{timestamp}"
    output_path = Path("output") / folder_name

    # Create directory
    output_path.mkdir(parents=True, exist_ok=True)

    return output_path


def save_extraction_results(output_path, job_description, job_extraction):
    """Save job description and extraction results"""

    # Save original job description
    with open(output_path / "job_description.txt", "w", encoding="utf-8") as f:
        f.write(job_description)

    # Save extraction results
    with open(output_path / "job_extraction.json", "w", encoding="utf-8") as f:
        json.dump(job_extraction, f, indent=2, ensure_ascii=False)

    print(f"Saved job analysis to: {output_path}")


def main():
    """Main JobTailor workflow"""
    try:
        print("🚀 JobTailor - Starting job analysis...")

        # Load input data
        print("📄 Loading job description...")
        job_description = load_job_description()
        print(f"✅ Loaded job description ({len(job_description)} characters)")

        print("📋 Loading resume data...")
        resume_data = load_resume_data()
        print(f"✅ Loaded resume for {resume_data['personal_info']['name']}")

        print("🎯 Loading brand statement...")
        brand_data = load_brand_data()
        print(
            f"✅ Loaded brand profile with {len(brand_data['brand_statement']['core_traits'])} core traits"
        )

        # Extract job information
        print("🤖 Analyzing job description with AI...")
        extractor = GeminiExtractor()
        job_extraction = extractor.extract_job_info(job_description)

        # Print extraction summary
        basic_info = job_extraction.get("basic_info", {})
        signals = job_extraction.get("personality_signals", [])

        print(f"✅ Job Analysis Complete!")
        print(f"   Company: {basic_info.get('company', 'Unknown')}")
        print(f"   Role: {basic_info.get('job_title', 'Unknown')}")
        print(f"   Requirements: {len(basic_info.get('key_requirements', []))} found")
        print(f"   Personality Signals: {len(signals)} found")

        if signals:
            print("   Key signals detected:")
            for signal in signals[:3]:  # Show first 3
                print(
                    f"     • {signal.get('signal', 'Unknown')} ({signal.get('category', 'unknown')})"
                )
            if len(signals) > 3:
                print(f"     ... and {len(signals) - 3} more")

        # Create output folder and save results
        print("💾 Saving results...")
        output_path = create_output_folder(job_extraction)
        save_extraction_results(output_path, job_description, job_extraction)

        print("🎉 Job analysis complete!")
        print(f"📁 Results saved to: {output_path}")

        # === Continue pipeline ===
        print("🧠 Initializing OpenAI model...")
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")

        model = OpenAIModel(api_key=openai_key)

        # Use raw job description text
        print("📄 Generating tailored resume...")
        tailored_resume = model.tailor_resume(resume_data, job_description)

        print("✉️ Generating cover letter...")
        cover_letter = model.generate_cover_letter(
            resume_json=resume_data,
            job_extraction_json=job_extraction,
            brand_statement_json=brand_data,
        )

        # Save outputs
        with open(output_path / "tailored_resume.txt", "w", encoding="utf-8") as f:
            f.write(tailored_resume)

        with open(output_path / "cover_letter.txt", "w", encoding="utf-8") as f:
            f.write(cover_letter)

        print("✅ Tailored resume and cover letter saved.")

        # TODO: Next steps
        print("\n🔄 Next steps:")
        print("   • Brand trait matching")
        print("   • Cover letter generation")
        print("   • Resume tailoring")

    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        print("💡 Make sure you have:")
        print("   • input/job.txt")
        print("   • input/resume.json")
        print("   • input/brand_statement.json")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
