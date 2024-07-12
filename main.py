import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import AzureChatOpenAI
from langchain_groq import ChatGroq


load_dotenv()

groq_api_key = os.environ["GROQ_API_KEY"]

llm = ChatGroq(
    model = "llama3-70b-8192",
    temperature = 0.0,
    api_key = groq_api_key
)

##creating agents
#creating Private data detection agent
private_data_agent = Agent(
    role = "Data Protection specialist",
    goal = """Check if the given information contains any private data such as Personal Identification Numbers (e.g., Social Security Numbers),
                Medical Records, Biometric Data (e.g., fingerprints, retina scans), Personal Financial Information (e.g., bank account details, credit card numbers),
                Private Communications (e.g., emails, text messages), Home Addresses, Phone Numbers, Birth Dates, Private Photos and Videos
                Passwords and PINs. You are knowledgeable about the principles, laws, and practices related to the protection and management 
                of personal and sensitive data. You ensure that data is handled in compliance with regulations 
                such as GDPR, HIPAA, CCPA, and others.""",
    backstory = "",
    verbose = True,
    allow_delegation = False,
    llm = llm
)

#creating Internal data detection agent
Internal_data_agent = Agent(
    role = "corporate data manager",
    goal = """Check if the given information contains the internal data of a company, including internal memos, company policies and procedures, 
    internal project plans, employee work schedules, internal meeting notes, staff directory and contact information, 
    internal financial statements, non-public marketing strategies, internal training materials, 
    and employee performance reviews. you are responsible for managing, safeguarding, and ensuring the proper use of internal company information""",
    backstory = "",
    verbose = True,
    allow_delegation = False,
    llm = llm
)

#creating Private data detection agent
private_data_agent = Agent(
    role = "Data Protection specialist",
    goal = "",
    backstory = "",
    verbose = True,
    allow_delegation = False,
    llm = llm
)

#creating Private data detection agent
private_data_agent = Agent(
    role = "Data Protection specialist",
    goal = "",
    backstory = "",
    verbose = True,
    allow_delegation = False,
    llm = llm
)

#creating Private data detection agent
private_data_agent = Agent(
    role = "Data Protection specialist",
    goal = "",
    backstory = "",
    verbose = True,
    allow_delegation = False,
    llm = llm
)