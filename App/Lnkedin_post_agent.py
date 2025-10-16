import os
import asyncio
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # ✅ Correct import
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema.output_parser import StrOutputParser


# Load environment variables
load_dotenv()

BASE_URL = os.getenv("BASE_URL") 
API_KEY = os.getenv("API_KEY") 
MODEL_NAME = os.getenv("MODEL_NAME") 

if not BASE_URL or not MODEL_NAME:
    raise ValueError("Please set BASE_URL and MODEL_NAME in your .env file")

# --- Pydantic Models for Structured Output ---

class LinkedInPost(BaseModel):
    """Model for LinkedIn post structure"""
    title: str = Field(description="Catchy title/headline for the post")
    content: str = Field(description="Main content of the LinkedIn post (2-4 paragraphs)")
    hashtags: List[str] = Field(description="Relevant hashtags for the post")
    call_to_action: str = Field(description="Engaging call-to-action to encourage interaction")
    
    def format_post(self) -> str:
        """Format the post for LinkedIn display"""
        formatted_post = f"{self.title}\n\n{self.content}\n\n"
        if self.call_to_action:
            formatted_post += f"{self.call_to_action}\n\n"
        formatted_post += " ".join([f"#{tag}" for tag in self.hashtags])
        return formatted_post

# --- LangChain Setup ---

# Initialize the LLM for local models
# --- LangChain Setup ---

from langchain_openai import ChatOpenAI  # ✅ new import

# Initialize the LLM for GitHub Models API
llm = ChatOpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    model=MODEL_NAME,
    temperature=0.7,
)


# Create the LinkedIn post generation prompt template
linkedin_post_prompt = PromptTemplate(
    input_variables=["topic", "language"],
    template="""
You are a professional LinkedIn content creator and social media expert. Create an engaging LinkedIn post about the given topic in the specified language.

Topic: {topic}
Language: {language}

Requirements:
1. Create a professional, engaging LinkedIn post (2-4 paragraphs)
2. Include a compelling title/headline
3. Make the content informative and valuable to the professional audience
4. Include relevant hashtags (3-5 hashtags)
5. Add a call-to-action to encourage engagement
6. Ensure the post is written in {language}
7. Keep it professional but conversational
8. Make it shareable and likely to generate discussion

Structure your response as follows:
TITLE: [Your catchy title here]
CONTENT: [Your 2-4 paragraph post content here]
HASHTAGS: [List 3-5 relevant hashtags separated by commas]
CALL_TO_ACTION: [Your call-to-action here]

Remember to:
- Start with a hook to grab attention
- Provide valuable insights or information
- Use professional language appropriate for LinkedIn
- Encourage meaningful engagement
- Keep paragraphs concise and readable
"""
)

# Create the LLM chain
linkedin_chain = LLMChain(
    llm=llm,
    prompt=linkedin_post_prompt,
    output_parser=StrOutputParser()
)

# --- LinkedIn Post Generator Agent ---

class LinkedInPostAgent:
    """AI Agent for generating LinkedIn posts using LangChain"""
    
    def __init__(self):
        self.chain = linkedin_chain
        
    async def generate_post(self, topic: str, language: str = "English") -> LinkedInPost:
        """
        Generate a LinkedIn post for the given topic and language
        
        Args:
            topic (str): The topic of the post (e.g., "AI in Healthcare", "Remote Work Productivity")
            language (str): The language of the post (e.g., "English", "Bengali", "Spanish")
            
        Returns:
            LinkedInPost: Structured LinkedIn post object
        """
        try:
            # Generate the post using the LangChain
            result = await self.chain.ainvoke({
                "topic": topic,
                "language": language
            })
            
            # Parse the generated content
            return self._parse_generated_content(result, topic, language)
            
        except Exception as e:
            print(f"Error generating post: {str(e)}")
            return self._create_fallback_post(topic, language)
    
    def _parse_generated_content(self, content: str, topic: str, language: str) -> LinkedInPost:
        """Parse the generated content into structured format"""
        try:
            lines = content.strip().split('\n')
            title = ""
            post_content = ""
            hashtags = []
            call_to_action = ""
            
            current_section = None
            content_lines = []
            
            for line in lines:
                line = line.strip()
                if line.startswith("TITLE:"):
                    title = line.replace("TITLE:", "").strip()
                    current_section = "title"
                elif line.startswith("CONTENT:"):
                    current_section = "content"
                    content_text = line.replace("CONTENT:", "").strip()
                    if content_text:
                        content_lines.append(content_text)
                elif line.startswith("HASHTAGS:"):
                    hashtags_text = line.replace("HASHTAGS:", "").strip()
                    hashtags = [tag.strip() for tag in hashtags_text.split(",") if tag.strip()]
                    current_section = "hashtags"
                elif line.startswith("CALL_TO_ACTION:"):
                    call_to_action = line.replace("CALL_TO_ACTION:", "").strip()
                    current_section = "cta"
                elif current_section == "content" and line:
                    content_lines.append(line)
            
            # Join content lines
            if not post_content:
                post_content = "\n\n".join(content_lines) if content_lines else ""
            
            # Clean up hashtags (remove # if present)
            hashtags = [tag.replace("#", "") for tag in hashtags]
            
            return LinkedInPost(
                title=title or f"Professional Insights on {topic}",
                content=post_content or f"Here's what I think about {topic} and its impact on our industry...",
                hashtags=hashtags or ["professional", "insights", "networking"],
                call_to_action=call_to_action or "What are your thoughts on this topic? Share your experience in the comments!"
            )
            
        except Exception as e:
            print(f"Error parsing content: {str(e)}")
            return self._create_fallback_post(topic, language)
    
    def _create_fallback_post(self, topic: str, language: str) -> LinkedInPost:
        """Create a fallback post if generation fails"""
        return LinkedInPost(
            title=f"Professional Insights on {topic}",
            content=f"As professionals, we're constantly navigating the evolving landscape of {topic}. "
                   f"This topic presents both challenges and opportunities that require our attention and strategic thinking. "
                   f"I'd love to hear your perspectives and experiences in this area.",
            hashtags=["professional", "insights", "networking", "industry"],
            call_to_action="What's your take on this? Let's discuss in the comments below!"
        )

# --- Main Function ---

async def main():
    """Main function to demonstrate the LinkedIn Post Agent"""
    
    # Initialize the agent
    linkedin_agent = LinkedInPostAgent()
    
    # Demo topics and languages
    demo_requests = [
        {"topic": "AI in Healthcare", "language": "English"},
        {"topic": "Remote Work Productivity", "language": "English"},
        {"topic": "Sustainable Business Practices", "language": "Spanish"},
        {"topic": "Digital Transformation", "language": "Bengali"},
    ]
    
    print("🚀 LinkedIn Post Generator Agent")
    print("=" * 50)
    
    for i, request in enumerate(demo_requests, 1):
        print(f"\n📝 Demo {i}: Generating post about '{request['topic']}' in {request['language']}")
        print("-" * 40)
        
        try:
            # Generate the post
            post = await linkedin_agent.generate_post(
                topic=request["topic"],
                language=request["language"]
            )
            
            # Display the formatted post
            print("\n" + "="*20 + " GENERATED POST " + "="*20)
            print(post.format_post())
            print("="*60)
            
        except Exception as e:
            print(f"❌ Error generating post: {str(e)}")
    
    # Interactive mode
    print("\n" + "="*50)
    print("🎯 Interactive Mode - Create your own LinkedIn post!")
    print("="*50)
    
    while True:
        try:
            print("\nEnter your request (or 'quit' to exit):")
            print("Format: Topic, Language (e.g., 'Machine Learning, English')")
            
            user_input = input("> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Thank you for using the LinkedIn Post Generator!")
                break
            
            if not user_input:
                continue
                
            # Parse input
            parts = user_input.split(',')
            if len(parts) >= 2:
                topic = parts[0].strip()
                language = parts[1].strip()
            else:
                topic = user_input.strip()
                language = "English"
            
            print(f"\n🔄 Generating LinkedIn post about '{topic}' in {language}...")
            
            # Generate post
            post = await linkedin_agent.generate_post(topic, language)
            
            # Display result
            print("\n" + "="*20 + " YOUR LINKEDIN POST " + "="*20)
            print(post.format_post())
            print("="*60)
            
        except KeyboardInterrupt:
            print("\n👋 Thank you for using the LinkedIn Post Generator!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())