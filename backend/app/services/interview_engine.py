from backend.app.core.llm.gemini_client import generate_response

class InterviewEngine:

    def __init__(self, config):
        self.role = config.role
        self.level = config.level
        self.tech_stack = config.tech_stack
        self.question_count = config.question_count

        self.current_question = 0

        self.topics_covered = []

        self.phase = "technical"

    def generate_question(self):

        prompt = f"""
        You are a professional technical interviewer.

        Candidate Role:
        {self.role}

        Candidate Level:
        {self.level}

        Tech Stack:
        {", ".join(self.tech_stack)}

        Current Interview Phase:
        {self.phase}

        Questions Already Asked:
        {self.current_question}

        Topics Already Covered:
        {self.topics_covered}

        Ask ONE realistic interview question.

        Do not repeat previous topics.
        """

        response = generate_response(prompt)

        self.current_question += 1

        return response