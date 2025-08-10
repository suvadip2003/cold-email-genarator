import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-70b-8192")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    # --- UPDATED METHOD ---
    def write_mail(self, job, links, user_name, user_role, user_company, company_description):
        """
        Generates a cold email using a flexible and powerful prompt template.
        """
        prompt_email = PromptTemplate.from_template(
            """
            ### PERSONA:
            You are a world-class business development executive and an expert cold email writer. Your tone is confident, professional, and helpful.

            ### CONTEXT:
            - Your Identity: You are {user_name}, a {user_role} at {user_company}.
            - Your Company's Pitch: {company_description}
            - Your Proof Points: Here is a list of relevant portfolio links you can use as social proof: {link_list}
            - The Target: You are writing to a hiring manager about the following job posting.
            - Job Posting Text: {job_description}

            ### TASK:
            Write a concise, professional, and highly personalized cold email to the hiring manager for this role. The email must be under 150 words and follow the structure below exactly.

            ### EMAIL STRUCTURE:
            1.  **Subject Line:** Create a short, specific subject line that references the job role.
            2.  **Personalized Opening (1 sentence):** Start by directly referencing the specific job title to prove you've done research.
            3.  **Value Proposition (2-3 sentences):** Connect your company's value directly to the key needs and responsibilities mentioned in the job description. Focus on the benefits you provide (e.g., "increase efficiency," "reduce costs," "solve X problem").
            4.  **Social Proof (1 sentence):** Naturally include one of the most relevant portfolio links from the context to build credibility.
            5.  **Call to Action (1 sentence):** End with a single, clear, low-friction question suggesting a brief call (e.g., "Would you be open to a 15-minute call next week?").

            ### RULES:
            - Do NOT include a preamble like "Here is the cold email:" or "Subject:".
            - Sign off with the exact signature below, ensuring each part is on a new line.

            ### SIGNATURE:
            Best regards,
            {user_name}
            {user_role}
            {user_company}

            ### COLD EMAIL:
            """
        )
        
        chain_email = prompt_email | self.llm
        
        res = chain_email.invoke({
            "job_description": str(job), 
            "link_list": links,
            "user_name": user_name,
            "user_role": user_role,
            "user_company": user_company,
            "company_description": company_description
        })
        
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))