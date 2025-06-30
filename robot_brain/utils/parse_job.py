import re
from typing import Tuple


def extract_company_and_role(job_description: str) -> Tuple[str, str]:
    """Extract company and job role from the job description text.

    The function looks for patterns like "<role> at <company>" on the first line
    of the job description. Fallbacks default to "UnknownCompany" and
    "UnknownRole" if nothing can be parsed.
    """
    if not job_description:
        return "UnknownCompany", "UnknownRole"

    first_line = job_description.strip().splitlines()[0]

    # Pattern: "Job Title at Company"
    match = re.search(r"^(?P<role>.+?)\s+at\s+(?P<company>.+)$", first_line, re.I)
    if match:
        role = match.group("role").strip()
        company = match.group("company").strip()
        return company, role

    # Pattern: "Company - Job Title" or "Job Title - Company"
    if " - " in first_line:
        left, right = first_line.split(" - ", 1)
        # heuristic: company names often contain keywords or are a single word
        company_keywords = [
            "inc",
            "llc",
            "corp",
            "company",
            "corporation",
            "technologies",
            "systems",
            "solutions",
            "group",
        ]
        left_lower = left.lower()
        right_lower = right.lower()
        if any(word in left_lower for word in company_keywords) or left.istitle():
            company, role = left.strip(), right.strip()
        else:
            company, role = right.strip(), left.strip()
        return company, role

    # Fallback: use first two words as role and company
    parts = first_line.split()
    if len(parts) >= 2:
        role = parts[0]
        company = parts[1]
        return company, role

    return "UnknownCompany", "UnknownRole"
