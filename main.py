"""
Career-Craft AI - Interactive CLI Application
Main entry point that uses all agents together
"""

import os
import sys
import json
from dotenv import load_dotenv
from google import genai

# Import all agents
from agents.coordinator import CoordinatorAgent
from agents.profile_analyzer import ProfileAnalyzerAgent
from agents.job_matcher import JobMatcherAgent
from agents.skill_analyzer import SkillAnalyzerAgent
from agents.interview_prep import InterviewPrepAgent
from memory.session_manager import SessionManager

load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


class CareerCraftCLI:
    """Interactive CLI for Career-Craft AI System"""
    
    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.profile_analyzer = ProfileAnalyzerAgent()
        self.job_matcher = JobMatcherAgent()
        self.skill_analyzer = SkillAnalyzerAgent()
        self.interview_prep = InterviewPrepAgent()
        self.session_manager = SessionManager()
        
        self.current_session = None
        self.current_user_profile = None
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_banner(self):
        """Display welcome banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║          CAREER-CRAFT AI - Career Guidance System           ║
║                                                              ║
║  Your intelligent multi-agent system for career success     ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def display_menu(self):
        """Display main menu"""
        menu = """
┌─ MAIN MENU ─────────────────────────────────────────────────┐
│                                                              │
│  1. Profile Analysis     - Analyze your resume/profile      │
│  2. Job Matching         - Find suitable job opportunities  │
│  3. Skill Analysis       - Identify skill gaps              │
│  4. Interview Prep       - Prepare for interviews           │
│  5. General Query        - Ask anything (Coordinator)       │
│  6. View Session         - View current session data        │
│  7. Clear Session        - Start fresh session              │
│  8. Exit                 - Close application                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
"""
        print(menu)
    
    def get_user_input(self, prompt="Your input: "):
        """Get user input safely"""
        try:
            return input(f"\n{prompt}").strip()
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
            return None
    
    def profile_analysis_menu(self):
        """Profile analysis submenu"""
        print("\n┌─ PROFILE ANALYSIS ──────────────────────────────────┐")
        print("│ 1. Full Profile Analysis                           │")
        print("│ 2. Extract Skills                                  │")
        print("│ 3. Assess Experience Level                         │")
        print("│ 4. Generate Professional Summary                   │")
        print("│ 5. Back to Main Menu                               │")
        print("└────────────────────────────────────────────────────┘")
        
        choice = self.get_user_input("Select option (1-5): ")
        
        if choice == "1":
            resume = self.get_user_input("\nPaste your resume/profile text:\n")
            if resume:
                result = self.profile_analyzer.process_profile(resume, "full")
                self.current_user_profile = result
                self.session_manager.store_session_data(self.current_session, 
                                                       "user_profile", result)
        elif choice == "2":
            resume = self.get_user_input("\nPaste your resume text:\n")
            if resume:
                self.profile_analyzer.process_profile(resume, "skills")
        elif choice == "3":
            resume = self.get_user_input("\nPaste your resume text:\n")
            if resume:
                self.profile_analyzer.process_profile(resume, "experience")
        elif choice == "4":
            resume = self.get_user_input("\nPaste your resume text:\n")
            if resume:
                self.profile_analyzer.process_profile(resume, "summary")
        elif choice != "5":
            print("\n❌ Invalid choice. Please try again.")
    
    def job_matching_menu(self):
        """Job matching submenu"""
        print("\n┌─ JOB MATCHING ──────────────────────────────────────┐")
        print("│ 1. Match Jobs (based on profile)                   │")
        print("│ 2. Find Specific Opportunities                     │")
        print("│ 3. Analyze Job Fit                                 │")
        print("│ 4. Explore Career Paths                            │")
        print("│ 5. Back to Main Menu                               │")
        print("└────────────────────────────────────────────────────┘")
        
        choice = self.get_user_input("Select option (1-5): ")
        
        if choice == "1":
            if not self.current_user_profile:
                profile = self.get_user_input("\nProvide your profile/skills:\n")
            else:
                profile = self.current_user_profile
            preferences = self.get_user_input("Any specific preferences? (leave blank if none): ")
            self.job_matcher.process_matching(profile, "match", preferences=preferences or None)
        elif choice == "2":
            role = self.get_user_input("What role are you interested in? (e.g., Python Developer): ")
            location = self.get_user_input("Preferred location (default: Remote): ") or "Remote"
            self.job_matcher.process_matching("", "find", role=role, location=location)
        elif choice == "3":
            profile = self.get_user_input("\nProvide your profile:\n")
            job_desc = self.get_user_input("Paste the job description:\n")
            self.job_matcher.process_matching(profile, "fit", job_description=job_desc)
        elif choice == "4":
            current_role = self.get_user_input("What is your current role? ")
            self.job_matcher.process_matching("", "paths", current_role=current_role)
        elif choice != "5":
            print("\n❌ Invalid choice. Please try again.")
    
    def skill_analysis_menu(self):
        """Skill analysis submenu"""
        print("\n┌─ SKILL ANALYSIS ────────────────────────────────────┐")
        print("│ 1. Identify Skill Gaps                             │")
        print("│ 2. Create Learning Path                            │")
        print("│ 3. Recommend Certifications                        │")
        print("│ 4. Industry Trends Analysis                        │")
        print("│ 5. Back to Main Menu                               │")
        print("└────────────────────────────────────────────────────┘")
        
        choice = self.get_user_input("Select option (1-5): ")
        
        if choice == "1":
            current = self.get_user_input("List your current skills: ")
            target = self.get_user_input("What role do you target? ")
            self.skill_analyzer.process_analysis("gaps", 
                                               current_skills=current, 
                                               target_role=target)
        elif choice == "2":
            skill = self.get_user_input("Which skill do you want to learn? ")
            level = self.get_user_input("Current level (Beginner/Intermediate/Advanced): ") or "Beginner"
            self.skill_analyzer.process_analysis("learning", skill=skill, level=level)
        elif choice == "3":
            profile = self.get_user_input("Provide your profile: ")
            target = self.get_user_input("Target role: ")
            self.skill_analyzer.process_analysis("certifications", 
                                               profile=profile, 
                                               target_role=target)
        elif choice == "4":
            industry = self.get_user_input("Which industry? (e.g., AI/ML, Web Development): ")
            self.skill_analyzer.process_analysis("trends", industry=industry)
        elif choice != "5":
            print("\n❌ Invalid choice. Please try again.")
    
    def interview_prep_menu(self):
        """Interview preparation submenu"""
        print("\n┌─ INTERVIEW PREPARATION ─────────────────────────────┐")
        print("│ 1. Generate Practice Questions                     │")
        print("│ 2. Get Answer Framework                            │")
        print("│ 3. Create Interview Guide                          │")
        print("│ 4. Interview Tips & Best Practices                 │")
        print("│ 5. Mock Interview Session                          │")
        print("│ 6. Back to Main Menu                               │")
        print("└────────────────────────────────────────────────────┘")
        
        choice = self.get_user_input("Select option (1-6): ")
        
        if choice == "1":
            role = self.get_user_input("What role are you interviewing for? ")
            level = self.get_user_input("Experience level (Entry/Junior/Mid/Senior): ") or "Junior"
            self.interview_prep.process_prep("questions", role=role, level=level)
        elif choice == "2":
            question = self.get_user_input("\nPaste the interview question:\n")
            self.interview_prep.process_prep("framework", question=question)
        elif choice == "3":
            company = self.get_user_input("Company name: ")
            role = self.get_user_input("Role: ")
            self.interview_prep.process_prep("guide", company=company, role=role)
        elif choice == "4":
            int_type = self.get_user_input("Interview type (Technical/Behavioral/HR): ") or "Technical"
            self.interview_prep.process_prep("tips", type=int_type)
        elif choice == "5":
            role = self.get_user_input("What role would you like to practice? ")
            print("\n📝 Mock Interview Session Starting...")
            self.interview_prep.process_prep("mock", role=role)
        elif choice != "6":
            print("\n❌ Invalid choice. Please try again.")
    
    def general_query(self):
        """Handle general queries through coordinator"""
        print("\n┌─ GENERAL QUERY ─────────────────────────────────────┐")
        print("│ Ask the Coordinator anything about your career     │")
        print("└────────────────────────────────────────────────────┘")
        
        query = self.get_user_input("\nYour question: ")
        if query:
            self.coordinator.process_query(query)
    
    def view_session(self):
        """View current session data"""
        if self.current_session:
            print("\n┌─ SESSION DATA ──────────────────────────────────────┐")
            print(f"Session ID: {self.current_session}")
            if self.current_user_profile:
                print(f"\nStored Profile:\n{self.current_user_profile[:500]}...")
            else:
                print("No profile data stored yet")
            print("└────────────────────────────────────────────────────┘")
        else:
            print("\n❌ No active session")
    
    def clear_session(self):
        """Clear current session"""
        self.current_session = self.session_manager.create_session("user")
        self.current_user_profile = None
        print(f"\n✅ Session cleared. New session ID: {self.current_session}")
    
    def run(self):
        """Main application loop"""
        self.clear_screen()
        self.display_banner()
        
        # Create initial session
        self.current_session = self.session_manager.create_session("user")
        print(f"✅ Session started. ID: {self.current_session}\n")
        
        print("Type 'help' at any time for assistance")
        print("Type 'exit' or select option 8 to quit\n")
        
        while True:
            try:
                self.display_menu()
                choice = self.get_user_input("Select option (1-8): ")
                
                if choice == "1":
                    self.profile_analysis_menu()
                elif choice == "2":
                    self.job_matching_menu()
                elif choice == "3":
                    self.skill_analysis_menu()
                elif choice == "4":
                    self.interview_prep_menu()
                elif choice == "5":
                    self.general_query()
                elif choice == "6":
                    self.view_session()
                elif choice == "7":
                    self.clear_session()
                elif choice == "8" or choice.lower() == "exit":
                    print("\n" + "="*60)
                    print("Thank you for using Career-Craft AI!")
                    print("Good luck with your career journey! 🚀")
                    print("="*60 + "\n")
                    break
                elif choice.lower() == "help":
                    self.display_banner()
                    print("Commands available:")
                    print("- Select any option from 1-8")
                    print("- Type 'exit' to quit")
                    print("- Type 'help' to see this message")
                else:
                    print("\n❌ Invalid choice. Please select 1-8 or type 'exit'.")
                
                input("\n📌 Press Enter to continue...")
                self.clear_screen()
                self.display_banner()
                
            except KeyboardInterrupt:
                print("\n\n❌ Application interrupted.")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again.")
                input("\nPress Enter to continue...")


def main():
    """Entry point"""
    try:
        app = CareerCraftCLI()
        app.run()
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
