from abc import ABC, abstractmethod


class ResumeTailorModel(ABC):
    @abstractmethod
    def tailor_resume(self, resume_json, job_description_text):
        pass

    @abstractmethod
    def generate_cover_letter(self, resume_json, job_description_text):
        pass

    def render_prompt(self, template_name: str, context: dict) -> str:
        import json
        from pathlib import Path

        prompt_path = Path(__file__).parent.parent / "prompts" / template_name
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

        template = prompt_path.read_text(encoding="utf-8")

        for key, value in context.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value, indent=2)
            template = template.replace(f"{{{{{key}}}}}", str(value))

        return template
