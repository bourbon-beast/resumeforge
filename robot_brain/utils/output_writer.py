import json
from datetime import datetime
from pathlib import Path


def save_outputs(
    tailored_resume: str,
    cover_letter: str,
    job_description: str,
    company: str,
    role: str,
    output_root: Path = Path("robot_brain/output"),
) -> Path:
    """Save generated files to a timestamped folder and return its path."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H%M")
    folder_name = f"{company}_{role}_{timestamp}"
    output_dir = output_root / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "tailored_resume.txt").write_text(tailored_resume)
    (output_dir / "cover_letter.txt").write_text(cover_letter)
    (output_dir / "job_description.txt").write_text(job_description)

    summary = {
        "company": company,
        "role": role,
        "timestamp": timestamp,
        "files": [
            "tailored_resume.txt",
            "cover_letter.txt",
            "job_description.txt",
        ],
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    return output_dir
