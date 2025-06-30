"""Entry point for running the resume tailoring pipeline."""

from pathlib import Path

from utils.output_writer import save_outputs
from utils.parse_job import extract_company_and_role


def main() -> None:
    """Tailor the resume and save outputs."""
    resume_json = Path("robot_brain/resume_template.json").read_text()
    job_path = Path("robot_brain/input/job.txt")
    job_description = job_path.read_text() if job_path.exists() else ""

    company, role = extract_company_and_role(job_description)

    # Placeholder generation logic; replace with model integration.
    tailored_resume = f"Tailored resume for {role} at {company}."
    cover_letter = f"Cover letter expressing interest in the {role} role at {company}."

    save_outputs(tailored_resume, cover_letter, job_description, company, role)


if __name__ == "__main__":
    main()
