import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from fastapi.middleware.cors import CORSMiddleware
import traceback # Used for logging exceptions

# --- Load environment variables and initial setup ---
load_dotenv()
BASE_URL = os.getenv("BASE_URL", "https://models.github.ai/inference")
API_KEY = os.getenv("API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

if not API_KEY:
    raise ValueError("❌ Please set your API_KEY in the .env file")

# --- FastAPI Initialization and CORS Configuration ---
app = FastAPI(
    title="LinkedIn Post Generator API",
    description="Generate professional LinkedIn posts using LangChain and OpenAI (GPT-4o-mini).",
    version="1.0.0"
)

# CORS FIX: Allow all origins so the local HTML file can connect
origins = ["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows POST, GET, and the preflight OPTIONS request
    allow_headers=["*"],
)


# --- LinkedIn Post Model (Pydantic) ---
class LinkedInPost(BaseModel):
    title: str = Field(description="Catchy headline for the post")
    content: str = Field(description="Main post body (2–4 paragraphs)")
    hashtags: List[str] = Field(description="Relevant hashtags")
    call_to_action: str = Field(description="Encouraging call to action")

    def format_post(self) -> str:
        """Formats the structured data into a ready-to-use LinkedIn post string."""
        formatted = f"{self.title}\n\n{self.content}\n\n"
        if self.call_to_action:
            formatted += f"{self.call_to_action}\n\n"
        # Format hashtags by adding the '#' symbol
        formatted += " ".join([f"#{tag}" for tag in self.hashtags])
        return formatted


# --- LangChain Setup ---
llm = ChatOpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    model=MODEL_NAME,
    temperature=0.7,
)

prompt_template = """
You are a professional LinkedIn content creator.
Create an engaging LinkedIn post about the topic below.

Topic: {topic}
Language: {language}

Rules:
1. 2–4 engaging paragraphs for the content section.
2. Include a catchy title.
3. Add relevant hashtags (3–5).
4. Add a specific call-to-action.
5. Write everything in {language}.

Format the output strictly using the following labels, one per line:
TITLE: <Your catchy headline>
CONTENT: <Your 2-4 paragraph post body>
HASHTAGS: <comma-separated list of tags, e.g., tag1, tag2, tag3>
CALL_TO_ACTION: <Your specific call-to-action>
"""

prompt = PromptTemplate(
    input_variables=["topic", "language"],
    template=prompt_template
)

# Use LCEL (LangChain Expression Language) for the chain: prompt | model | output_parser
# This replaces the deprecated LLMChain and automatically returns the string output.
post_chain = (
    RunnablePassthrough.assign(
        topic=lambda x: x["topic"], 
        language=lambda x: x["language"]
    )
    | prompt
    | llm
    | StrOutputParser()
)


# --- LinkedIn Post Agent ---
class LinkedInPostAgent:
    def __init__(self):
        # Use the LCEL chain
        self.chain = post_chain

    async def generate_post(self, topic: str, language: str = "English") -> LinkedInPost:
        # LCEL chain returns the raw string directly when using ainvoke()
        llm_output_string = await self.chain.ainvoke({"topic": topic, "language": language})
        
        # The dictionary extraction logic is now REMOVED because LCEL + StrOutputParser 
        # ensures we get a string.
        
        return self._parse_output(llm_output_string, topic)


    def _parse_output(self, text: str, topic: str) -> LinkedInPost:
        """Parses the raw text output from the LLM into the structured LinkedInPost model."""
        lines = text.strip().split("\n")
        title, hashtags, call_to_action = "", [], ""
        content_lines = []
        parsing_content = False

        for line in lines:
            line = line.strip()
            if line.upper().startswith("TITLE:"):
                title = line.replace("TITLE:", "").strip()
                parsing_content = False
            elif line.upper().startswith("CONTENT:"):
                parsing_content = True
                part = line.replace("CONTENT:", "").strip()
                if part:
                    content_lines.append(part)
            elif line.upper().startswith("HASHTAGS:"):
                # Clean and split hashtags
                tag_string = line.replace("HASHTAGS:", "").strip()
                hashtags = [t.strip().replace("#", "") for t in tag_string.split(",") if t.strip()]
                parsing_content = False
            elif line.upper().startswith("CALL_TO_ACTION:"):
                call_to_action = line.replace("CALL_TO_ACTION:", "").strip()
                parsing_content = False
            elif parsing_content and line:
                # Accumulate content lines until the next section marker
                content_lines.append(line)
        
        # Join content lines with double newlines for paragraph spacing
        content = "\n\n".join(content_lines)

        # Return structured post, providing sensible defaults if parsing failed
        return LinkedInPost(
            title=title or f"Insights on {topic}",
            content=content or f"Sharing thoughts on {topic}.",
            hashtags=hashtags or ["business", "growth", "leadership"],
            call_to_action=call_to_action or "What do you think? Let’s discuss!"
        )


# --- API Routes ---
agent = LinkedInPostAgent()

class PostRequest(BaseModel):
    topic: str
    language: str = "English"

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Welcome to the LinkedIn Post Generator API! Status: OK"}


@app.post("/generate", response_model=LinkedInPost)
async def generate_post_structured(request: PostRequest):
    """Generates a LinkedIn post and returns the structured data model."""
    try:
        post = await agent.generate_post(request.topic, request.language)
        return post
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/generate_formatted")
async def generate_formatted(request: PostRequest):
    """Generates a LinkedIn post and returns the final formatted string for easy copying."""
    try:
        post = await agent.generate_post(request.topic, request.language)
        return {"formatted_post": post.format_post()}
    except Exception as e:
        print(traceback.format_exc())
        # Return a simple error dictionary for the frontend to handle
        return {"error": f"Failed to generate post: {str(e)}"}
