# 📧 AI-Powered Cold Email Generator
An intelligent application that automates the creation of personalized cold emails for job applications. Simply provide a job description, and the app leverages the power of Large Language Models via the Groq API to craft a compelling email tailored to the role.

## ✨ Live Demo
**[🚀 View the live application here!](https://cold-email-genarator-b8swfy3w739wbvug3aelhz.streamlit.app/)** *(Note: Replace this with your actual deployment link)*

---

## 📸 Application Interface
Here's a look at the clean and intuitive user interface built with Streamlit. The user provides their personal information in the sidebar, pastes a job description, and receives a professionally crafted email in seconds.


![App Screenshot](https://drive.google.com/file/d/1vuPXtI3EC5yIpBQqZA-UzQ0bnhAoHaG-/view?usp=sharing) 
*(To make this image work, you can upload your screenshot to a site like [Imgur](https://imgur.com/upload) and paste the direct link here)*

---

## 📋 Features
- **Dynamic Email Generation:** Creates unique, context-aware emails for any job description.
- **Personalized User Input:** A full sidebar allows any user to input their name, skills, and projects for truly custom emails.
- **Fast & Powerful LLM:** Integrated with the high-speed Groq API to use the Llama 3 model for generation.
- **Simple UI:** Built with Streamlit for a clean, interactive, and user-friendly experience.

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Backend & AI Orchestration:** LangChain
- **Language Model:** Llama 3 via Groq API
- **Core Libraries:** Pandas, python-dotenv
- **Deployment:** Streamlit Community Cloud

---

## ⚙️ How to Run This Project Locally
Follow these steps to set up and run the project on your own machine.

### Prerequisites
- Python 3.11 or later
- Git

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
```

### 2. Create and Activate a Virtual Environment
A virtual environment is essential for managing project dependencies.
```bash
# Create the virtual environment
python -m venv .venv

# Activate it (on Windows)
.venv\Scripts\activate
```

### 3. Install Dependencies
All required packages are listed in the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
You'll need an API key from [Groq](https://console.groq.com/keys) to run the application.

1.  Create a file named `.env` in the root of your project folder.
2.  Add your API key to this file in the following format:
    ```
    GROQ_API_KEY="gsk_YourSecretKeyGoesHere"
    ```

### 5. Run the Streamlit App
You're all set! Run the following command in your terminal:
```bash
streamlit run app/main.py
```
The application should now be running on your `localhost`.

---

## 🚀 How It Works
The application follows a simple but powerful workflow:
1.  **User Input:** The user provides their personal information in the sidebar and a job description in the main text area.
2.  **LLM Processing:** When the "Generate Email" button is clicked, the job description and user info are sent to the Groq API via a structured LangChain prompt.
3.  **Content Generation:** The Llama 3 model analyzes the context and generates a personalized cold email based on the engineered prompt.
4.  **Display:** The final, formatted email is displayed in the Streamlit interface.

