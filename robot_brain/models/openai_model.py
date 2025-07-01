import openai
from model_interface import ResumeTailorModel


class OpenAIModel(ResumeTailorModel):
    def __init__(self, api_key):
        openai.api_key = api_key

    def tailor_resume(self, resume_json, job_description_text):
        prompt = f"""
        You are an expert resume coach.
        Given the following resume (in JSON) and a job description,
        output a tailored resume that emphasizes the most relevant experience
        and uses strong, outcome-focused language.

        RESUME: {resume_json}
        JOB DESCRIPTION: {job_description_text}
        """
        response = openai.ChatCompletion.create(
            model="gpt-4", messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"]

    def generate_cover_letter(
        self, resume_json, job_extraction_json, brand_statement_json
    ):
        prompt = self.render_prompt(
            "cover_letter_prompt.txt",
            {
                "resume_json": resume_json,
                "job_extraction_json": job_extraction_json,
                "brand_statement_json": brand_statement_json,
            },
        )
        response = openai.ChatCompletion.create(
            model="gpt-4", messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"]
