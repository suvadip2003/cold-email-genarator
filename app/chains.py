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

    # --- NEW METHOD with a powerful prompt for job applications ---
    def write_application_mail(self, job_description, your_name, your_status, your_passion, your_projects, your_skills, your_phone, your_links):
        
        prompt_template = PromptTemplate.from_template(
            """
            ### PERSONA:
            You are a professional career coach who excels at writing concise and impactful cold emails for job applications.

            ### CONTEXT:
            - Applicant's Name: {your_name}
            - Applicant's Background: {your_status}
            - Applicant's Passion: {your_passion}
            - Applicant's Key Projects/Achievements: {your_projects}
            - Applicant's Relevant Skills: {your_skills}
            - Applicant's Contact Info: Phone - {your_phone}, Links - {your_links}
            - The full text of the job description they are applying for is below:
            ---
            {job_description}
            ---

            ### TASK:
            Analyze the job description to identify the company's name and the specific job role. Then, write a short, professional, and confident cold email from the applicant to the hiring manager. Follow the structure below exactly.

            ### EMAIL STRUCTURE:
            1.  **Subject Line:** Format as "[Role] Application – [Your Name]".
            2.  **Greeting:** Use a professional but generic greeting like "Dear Hiring Manager,".
            3.  **Paragraph 1 (Introduction):** In one or two sentences, introduce the applicant, their background, their passion, and mention their key projects/achievements.
            4.  **Paragraph 2 (Connection & Value):** In one or two sentences, state admiration for the company's work (infer this from the job description) and explicitly state the desire to contribute their specific skills to the team.
            5.  **Paragraph 3 (Call to Action):** Mention that the resume and portfolio are attached/linked and ask for a quick call to explore opportunities.
            6.  **Signature:** Format the signature exactly as shown below, with each part on a new line.

            ### RULES:
            - Keep the email body concise and professional.
            - Do not add any preamble or text before the "Subject:" line.
            
            ### SIGNATURE FORMAT:
            Best regards,

            {your_name}

            {your_phone} | {your_links}

            ### EMAIL:
            """
        )

        application_chain = prompt_template | self.llm
        
        response = application_chain.invoke({
            "job_description": job_description,
            "your_name": your_name,
            "your_status": your_status,
            "your_passion": your_passion,
            "your_projects": your_projects,
            "your_skills": your_skills,
            "your_phone": your_phone,
            "your_links": your_links
        })
        
        return response.content