from abc import ABC, abstractmethod

class ResumeTailorModel(ABC):
    @abstractmethod
    def tailor_resume(self, resume_json, job_description_text):
        pass

    @abstractmethod
    def generate_cover_letter(self, resume_json, job_description_text):
        pass
