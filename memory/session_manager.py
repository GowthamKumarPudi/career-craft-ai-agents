"""
Session Manager
Manages user sessions and stores session data
"""

import json
import os
from datetime import datetime


class SessionManager:
    """Manages user sessions and data persistence"""
    
    def __init__(self, session_file='sessions/sessions.json'):
        self.session_file = session_file
        self.sessions = {}
        self.load_sessions()
    
    def create_session(self, user_id):
        """Create a new session for a user"""
        session_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.sessions[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'data': {}
        }
        
        self.save_sessions()
        return session_id
    
    def store_session_data(self, session_id, key, value):
        """Store data in a session"""
        if session_id in self.sessions:
            self.sessions[session_id]['data'][key] = value
            self.sessions[session_id]['last_updated'] = datetime.now().isoformat()
            self.save_sessions()
            return True
        return False
    
    def retrieve_session_data(self, session_id, key):
        """Retrieve data from a session"""
        if session_id in self.sessions:
            return self.sessions[session_id]['data'].get(key)
        return None
    
    def get_session(self, session_id):
        """Get complete session data"""
        return self.sessions.get(session_id)
    
    def delete_session(self, session_id):
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            self.save_sessions()
            return True
        return False
    
    def save_sessions(self):
        """Save sessions to file"""
        try:
            os.makedirs('sessions', exist_ok=True)
            with open(self.session_file, 'w') as f:
                json.dump(self.sessions, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save sessions: {e}")
    
    def load_sessions(self):
        """Load sessions from file"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    self.sessions = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load sessions: {e}")
            self.sessions = {}
    
    def list_sessions(self, user_id):
        """List all sessions for a user"""
        user_sessions = []
        for session_id, session_data in self.sessions.items():
            if session_data['user_id'] == user_id:
                user_sessions.append({
                    'session_id': session_id,
                    'created_at': session_data['created_at'],
                    'last_updated': session_data['last_updated']
                })
        return user_sessions


def main():
    """Test session manager"""
    print("="*60)
    print("SESSION MANAGER - TEST")
    print("="*60)
    
    manager = SessionManager()
    
    # Create session
    session_id = manager.create_session("user123")
    print(f"\n✅ Session created: {session_id}")
    
    # Store data
    manager.store_session_data(session_id, "name", "Gowtham")
    manager.store_session_data(session_id, "skills", ["Python", "JavaScript"])
    print("✅ Data stored")
    
    # Retrieve data
    name = manager.retrieve_session_data(session_id, "name")
    skills = manager.retrieve_session_data(session_id, "skills")
    print(f"\n📋 Retrieved Data:")
    print(f"   Name: {name}")
    print(f"   Skills: {skills}")
    
    # Get full session
    session = manager.get_session(session_id)
    print(f"\n📋 Full Session:")
    print(json.dumps(session, indent=2))


if __name__ == "__main__":
    main()
