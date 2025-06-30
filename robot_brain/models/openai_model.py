import openai
from models.model_interface import ResumeTailorModel

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
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']

    def generate_cover_letter(self, resume_json, job_description_text):
        prompt = f"""
        Write a compelling, personalized cover letter for this job application.
        Use the resume and job description to highlight fit and enthusiasm.

        RESUME: {resume_json}
        JOB DESCRIPTION: {job_description_text}
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
