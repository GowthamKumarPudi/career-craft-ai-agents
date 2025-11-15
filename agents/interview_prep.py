"""
Interview Prep Agent
Generates interview questions and provides preparation guidance
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


class InterviewPrepAgent:
    """Prepares users for job interviews"""
    
    def __init__(self):
        self.model = 'gemini-2.0-flash'
        self.name = "Interview Prep"
        self.instruction = """
You are an Interview Preparation Specialist. Your expertise includes:
- Interview strategy and preparation
- Technical question generation
- Behavioral question coaching
- Answer framework training (STAR method)
- Mock interview conducting

When preparing for interviews:
1. Assess the interview type and level
2. Generate relevant practice questions
3. Provide answer frameworks
4. Give interview tips and best practices
5. Build confidence and readiness
"""

    def generate_questions(self, role_title, experience_level="Junior"):
        """Generate practice interview questions"""
        
        prompt = f"""
Generate interview questions for this position:

ROLE: {role_title}
EXPERIENCE LEVEL: {experience_level}

Create:
1. **Technical Questions**: 5 role-specific technical questions
2. **Behavioral Questions**: 5 behavioral questions (STAR format)
3. **Situational Questions**: 3 scenario-based questions
4. **Company Questions**: 3 questions to ask the company
5. **Difficulty Rating**: Easy/Medium/Hard for each

Format with clear numbering and expectations.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def provide_answer_framework(self, question):
        """Provide framework for answering interview questions"""
        
        prompt = f"""
Provide a framework to answer this interview question well:

QUESTION: {question}

Give:
1. **Analysis**: What are they really asking?
2. **STAR Method**: Situation, Task, Action, Result (if applicable)
3. **Sample Answer**: Example answer structure
4. **Key Points**: Critical points to mention
5. **Do's and Don'ts**: What to do and avoid
6. **Follow-ups**: Possible follow-up questions

Make it practical and actionable.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def create_prep_guide(self, company_name, role_title):
        """Create interview preparation guide for specific company"""
        
        prompt = f"""
Create a comprehensive interview prep guide:

COMPANY: {company_name}
ROLE: {role_title}

Include:
1. **Company Overview**: What you should know
2. **Role Requirements**: Key skills and experience
3. **Common Questions**: Questions typically asked
4. **Technical Topics**: Topics to review
5. **Preparation Checklist**: Week-by-week prep plan
6. **Day-Before Tips**: Final preparation
7. **Day-Of Tips**: Interview day strategy

Make it comprehensive and actionable.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def provide_tips(self, interview_type="Technical"):
        """Provide interview tips and best practices"""
        
        prompt = f"""
Provide comprehensive interview tips for {interview_type} interviews:

INTERVIEW TYPE: {interview_type}

Provide:
1. **Before Interview**: Preparation steps
2. **During Interview**: Tips and techniques
3. **Communication**: How to respond effectively
4. **Technical Specific**: For technical interviews
5. **Common Mistakes**: What to avoid
6. **Red Flags**: What not to do
7. **Closing Strong**: How to end the interview

Be specific and actionable.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def conduct_mock_interview(self, role_title):
        """Conduct a mock interview session"""
        
        prompt = f"""
You are conducting a mock interview for: {role_title}

1. Ask ONE interview question appropriate for this role
2. Wait for the candidate's answer
3. Provide constructive feedback on their response
4. Give suggestions for improvement
5. Ask if they want to continue (be interactive)

Make it realistic and helpful. Start with a warm greeting and then ask the first question.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text

    def process_prep(self, query_type, **kwargs):
        """Process interview preparation requests"""
        
        print(f"\n{'='*70}")
        print(f"{self.name}: Interview Preparation")
        print(f"{'='*70}\n")
        
        if query_type == "questions":
            role = kwargs.get('role', 'Software Engineer')
            level = kwargs.get('level', 'Junior')
            result = self.generate_questions(role, level)
        elif query_type == "framework":
            question = kwargs.get('question', '')
            result = self.provide_answer_framework(question)
        elif query_type == "guide":
            company = kwargs.get('company', '')
            role = kwargs.get('role', '')
            result = self.create_prep_guide(company, role)
        elif query_type == "tips":
            int_type = kwargs.get('type', 'Technical')
            result = self.provide_tips(int_type)
        elif query_type == "mock":
            role = kwargs.get('role', 'Software Engineer')
            result = self.conduct_mock_interview(role)
        else:
            result = "Query type not recognized"
        
        print(result)
        print(f"\n{'='*70}\n")
        
        return result


def main():
    """Test the Interview Prep Agent"""
    
    print("="*70)
    print("INTERVIEW PREP AGENT - TEST")
    print("="*70)
    
    prep = InterviewPrepAgent()
    
    print("\n--- GENERATE QUESTIONS ---")
    prep.process_prep("questions", 
                     role="Python Developer", 
                     level="Junior")
    
    print("\n--- ANSWER FRAMEWORK ---")
    prep.process_prep("framework",
                     question="Tell me about a challenging project you worked on")
    
    print("\n--- PREPARATION GUIDE ---")
    prep.process_prep("guide",
                     company="TCS",
                     role="Software Engineer")
    
    print("\n--- INTERVIEW TIPS ---")
    prep.process_prep("tips", type="Technical Interview")


if __name__ == "__main__":
    main()
