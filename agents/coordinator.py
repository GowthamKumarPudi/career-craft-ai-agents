"""
Coordinator Agent - Main Orchestrator
Manages the workflow and routes queries to specialized agents
"""

import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


class CoordinatorAgent:
    """Main coordinator that manages all agent workflows"""
    
    def __init__(self):
        self.model = 'gemini-2.0-flash'
        self.name = "Career-Craft Coordinator"
        self.instruction = """
You are the Career-Craft AI Coordinator Agent. You are the main orchestrator 
of a career guidance system. Your role is to:

1. Analyze user queries to understand what they need
2. Route queries to the appropriate specialized agent:
   - Profile Analysis: For resume/profile analysis
   - Job Matching: For job search and recommendations
   - Skill Analysis: For skill gap identification
   - Interview Prep: For interview preparation

3. Maintain context across the conversation
4. Provide comprehensive guidance

When responding:
- Be helpful and encouraging
- Provide actionable advice
- Ask clarifying questions if needed
- Maintain a professional but friendly tone

Available specializations:
- Profile Analyzer: Analyzes resumes and extracts key information
- Job Matcher: Finds relevant job opportunities
- Skill Gap Analyzer: Identifies skills needed for roles
- Interview Prep: Generates practice questions and tips
"""

    def analyze_intent(self, user_query):
        """Analyze user query to determine which agent to route to"""
        
        intent_analyzer_prompt = f"""
Analyze this user query and determine which type of help they need:

Query: "{user_query}"

Respond with ONLY a JSON object (no other text):
{{
    "intent": "one of: profile_analysis, job_matching, skill_analysis, interview_prep, general_guidance",
    "confidence": "high, medium, or low",
    "reasoning": "brief explanation"
}}
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=intent_analyzer_prompt
        )
        
        try:
            result = json.loads(response.text)
            return result
        except json.JSONDecodeError:
            return {
                "intent": "general_guidance",
                "confidence": "low",
                "reasoning": "Could not parse intent, defaulting to general guidance"
            }

    def route_to_specialist(self, user_query, intent):
        """Route query to the appropriate specialist agent"""
        
        if intent == "profile_analysis":
            return self._profile_analysis_agent(user_query)
        elif intent == "job_matching":
            return self._job_matching_agent(user_query)
        elif intent == "skill_analysis":
            return self._skill_analysis_agent(user_query)
        elif intent == "interview_prep":
            return self._interview_prep_agent(user_query)
        else:
            return self._general_guidance_agent(user_query)

    def _profile_analysis_agent(self, user_query):
        """Profile Analysis Specialist"""
        
        prompt = f"""
You are a Profile Analysis Specialist. Help the user analyze their professional profile.

User Query: {user_query}

Provide:
1. Key information to include in a profile
2. Skills assessment framework
3. Experience level evaluation
4. Recommendations for profile improvement

Be specific and actionable.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return {
            "agent": "Profile Analyzer",
            "response": response.text
        }

    def _job_matching_agent(self, user_query):
        """Job Matching Specialist"""
        
        prompt = f"""
You are a Job Matching Specialist. Help the user find suitable job opportunities.

User Query: {user_query}

Provide:
1. Types of roles that match their profile/interests
2. Industries to explore
3. Job search strategies
4. Resources for finding opportunities

Be realistic and encouraging.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return {
            "agent": "Job Matcher",
            "response": response.text
        }

    def _skill_analysis_agent(self, user_query):
        """Skill Gap Analysis Specialist"""
        
        prompt = f"""
You are a Skill Gap Analysis Specialist. Help users identify skill gaps and learning paths.

User Query: {user_query}

Provide:
1. Current skills assessment framework
2. Skills needed for their goal role
3. Skill gaps identified
4. Learning resources and timeline
5. Priority skills to learn first

Be detailed and structured.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return {
            "agent": "Skill Analyzer",
            "response": response.text
        }

    def _interview_prep_agent(self, user_query):
        """Interview Preparation Specialist"""
        
        prompt = f"""
You are an Interview Preparation Specialist. Help users prepare for job interviews.

User Query: {user_query}

Provide:
1. Interview preparation checklist
2. Practice questions relevant to their target role
3. Answer frameworks (STAR method)
4. Common mistakes to avoid
5. Final tips for success

Be comprehensive and encouraging.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return {
            "agent": "Interview Prep",
            "response": response.text
        }

    def _general_guidance_agent(self, user_query):
        """General Guidance for unclassified queries"""
        
        prompt = f"""
You are a Career Guidance AI Agent. Provide helpful career advice.

User Query: {user_query}

Respond with:
1. Direct answer to their question
2. Relevant career insights
3. Actionable next steps
4. Resources if applicable

Be helpful and encouraging.
"""
        
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return {
            "agent": "General Guidance",
            "response": response.text
        }

    def process_query(self, user_query):
        """Main method to process user queries"""
        
        print(f"\n{'='*70}")
        print(f"Coordinator: Processing your query...")
        print(f"{'='*70}\n")
        
        # Step 1: Analyze intent
        print(f"Analyzing intent...")
        intent_result = self.analyze_intent(user_query)
        print(f"Intent: {intent_result['intent']} (Confidence: {intent_result['confidence']})")
        print(f"Reason: {intent_result['reasoning']}\n")
        
        # Step 2: Route to specialist
        print(f"Routing to specialist agent...")
        specialist_result = self.route_to_specialist(user_query, intent_result['intent'])
        
        # Step 3: Return response
        print(f"{'='*70}")
        print(f"Agent: {specialist_result['agent']}")
        print(f"{'='*70}\n")
        print(specialist_result['response'])
        print(f"\n{'='*70}\n")
        
        return specialist_result


def main():
    """Main function to test the coordinator"""
    
    print("="*70)
    print("CAREER-CRAFT AI - COORDINATOR AGENT")
    print("="*70)
    
    # Create coordinator instance
    coordinator = CoordinatorAgent()
    
    # Test queries
    test_queries = [
        "I'm a final year student. Help me prepare for software engineering interviews.",
        "What skills do I need to become a data scientist?",
        "I have 2 years of Python experience. What jobs should I target?",
        "How do I improve my professional profile?"
    ]
    
    print("\nTesting with sample queries...\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Query {i} ---")
        print(f"User: {query}\n")
        
        coordinator.process_query(query)
        
        if i < len(test_queries):
            input("\nPress Enter to continue to next query...")


if __name__ == "__main__":
    main()
