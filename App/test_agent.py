"""
Simple test script for the LinkedIn Post Generator Agent
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_linkedin_agent():
    """Test the LinkedIn Post Agent with sample inputs"""
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key in the .env file.")
        return
    
    try:
        # Import the agent (only after checking API key)
        from Lnkedin_post_agent import LinkedInPostAgent
        
        print("🚀 Testing LinkedIn Post Generator Agent")
        print("=" * 50)
        
        # Initialize the agent
        agent = LinkedInPostAgent()
        
        # Test cases
        test_cases = [
            {"topic": "Machine Learning in Finance", "language": "English"},
            {"topic": "Sustainable Technology", "language": "Spanish"},
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}: {test_case['topic']} in {test_case['language']}")
            print("-" * 40)
            
            try:
                # Generate post
                post = await agent.generate_post(
                    topic=test_case["topic"],
                    language=test_case["language"]
                )
                
                # Display result
                print("✅ Generated Successfully!")
                print("\n" + "="*20 + " POST " + "="*20)
                print(post.format_post())
                print("="*50)
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        print("\n🎉 All tests completed!")
        
    except ImportError as e:
        print(f"❌ Import Error: {str(e)}")
        print("Please install required dependencies: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_linkedin_agent())
