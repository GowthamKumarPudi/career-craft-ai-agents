"""
Setup Verification Script - Windows Edition
Run this to verify your environment is correctly configured
"""

import os
import sys
from dotenv import load_dotenv

# Windows color support
try:
    from colorama import init, Fore, Style
    init()
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    RESET = Style.RESET_ALL
except:
    GREEN = RED = YELLOW = RESET = ""


def test_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"{GREEN}✓{RESET} Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 10:
        print(f"  {GREEN}✓{RESET} Version is compatible")
        return True
    else:
        print(f"  {RED}✗{RESET} Need Python 3.10 or higher")
        return False


def test_windows():
    """Check if running on Windows"""
    if sys.platform.startswith('win'):
        print(f"{GREEN}✓{RESET} Running on Windows")
        print(f"  Windows version: {sys.getwindowsversion().major}.{sys.getwindowsversion().minor}")
        return True
    else:
        print(f"{YELLOW}!{RESET} Not running on Windows")
        return True


def test_env_file():
    """Check .env file"""
    if os.path.exists('.env'):
        print(f"{GREEN}✓{RESET} .env file exists")
        return True
    else:
        print(f"{RED}✗{RESET} .env file not found")
        print("  Create a .env file with your GEMINI_API_KEY")
        return False


def test_api_key():
    """Check API key"""
    load_dotenv()
    key = os.getenv('GEMINI_API_KEY')
    
    if key and len(key) > 20 and not key.startswith('PASTE'):
        masked_key = f"{key[:10]}...{key[-4:]}"
        print(f"{GREEN}✓{RESET} API key configured ({masked_key})")
        return True
    else:
        print(f"{RED}✗{RESET} API key not configured properly")
        return False


def test_imports():
    """Test importing required packages"""
    packages = {
        'google.genai': 'Google Generative AI',
        'dotenv': 'Python Dotenv',
        'requests': 'Requests',
        'pandas': 'Pandas',
        'colorama': 'Colorama (Windows colors)'
    }
    
    all_good = True
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"{GREEN}✓{RESET} {name}")
        except ImportError:
            print(f"{RED}✗{RESET} {name} - Failed to import")
            all_good = False
    
    return all_good


def test_gemini_connection():
    """Test actual API connection"""
    try:
        from google import genai
        
        load_dotenv()
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        
        print(f"{YELLOW}⟳{RESET} Testing API connection...")
        
        response = client.models.generate_content(
    model='gemini-2.0-flash',
            contents='Reply with just: SUCCESS'
        )
        
        if 'SUCCESS' in response.text.upper():
            print(f"{GREEN}✓{RESET} Gemini API connection successful!")
            print(f"  Response: {response.text}")
            return True
        else:
            print(f"{RED}✗{RESET} Unexpected response")
            return False
            
    except Exception as e:
        print(f"{RED}✗{RESET} Connection failed: {str(e)}")
        return False


def main():
    print("=" * 70)
    print("AI AGENTS CAPSTONE - WINDOWS SETUP VERIFICATION")
    print("=" * 70)
    print()
    
    tests = [
        ("Python Version", test_python_version),
        ("Windows Check", test_windows),
        ("Environment File", test_env_file),
        ("API Key Configuration", test_api_key),
        ("Package Imports", test_imports),
        ("Gemini API Connection", test_gemini_connection)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{name}:")
        print("-" * 70)
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 70)
    if all(results):
        print(f"{GREEN}✓✓✓ ALL TESTS PASSED! ✓✓✓{RESET}")
        print("Your Windows environment is ready for development!")
    else:
        print(f"{RED}✗✗✗ SOME TESTS FAILED ✗✗✗{RESET}")
        print("Please fix the issues above before continuing.")
    print("=" * 70)
    
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()

