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
    goal = "Check if the given information contains any Private Data.",
    backstory = """This agent is specialized in Checking private data such as Personal Identification Numbers (e.g., Social Security Numbers),
                Medical Records, Biometric Data (e.g., fingerprints, retina scans), Personal Financial Information (e.g., bank account details, credit card numbers),
                Private Communications (e.g., emails, text messages), Home Addresses, Phone Numbers, Birth Dates, Private Photos and Videos
                Passwords and PINs. You are knowledgeable about the principles, laws, and practices related to the protection and management 
                of personal and sensitive data. This agent ensure that data is handled in compliance with regulations 
                such as GDPR, HIPAA, CCPA, and others """,
    verbose = True,
    allow_delegation = False,
    llm = llm
)

#creating Internal data detection agent
Internal_data_agent = Agent(
    role = "corporate data manager",
    goal = """Check if the given information contains the internal data of a company including """,
    backstory = """This agent is specialized in checking Internal data of a company such as internal memos, company policies and procedures, 
                internal project plans, employee work schedules, internal meeting notes, staff directory and contact information, 
                internal financial statements, non-public marketing strategies, internal training materials, 
                and employee performance reviews. you are responsible for managing, safeguarding, and ensuring the proper use of internal company information""",
    verbose = True,
    allow_delegation = False,
    llm = llm
)

#creating Confidential data detection agent
confidential_data_agent = Agent(
    role = "professional in handling Confidential Data",
    goal = "Check in the given information if any Confidential Data is present.",
    backstory = """
                This agent understands and manages confidential data such as trade secrets, proprietary algorithms, research and development data, 
                customer data, contractual agreements, strategic plans, legal documents, vendor information, M&A documents, and confidential business 
                reports. the agent is professional and responsible for ensuring that sensitive and confidential information is protected from unauthorized access 
                and disclosure, and is handled in compliance with legal and regulatory requirements
                """,
    verbose = True,
    allow_delegation = False,
    llm = llm
)

#creating  Restricted Data detection agent
restricted_data_agent = Agent(
    role = "professional in handling Restricted Data.",
    goal = "Check in the given information if any Restricted Data is passed.",
    backstory = """
                this agent is specialized in understanding and managing restricted data such as national security information, classified government documents, 
                security codes and access controls, critical infrastructure data, law enforcement investigation reports, sensitive intelligence reports, 
                military operations information, highly sensitive financial data, critical research data, and highly sensitive personal information. 
                This agent is responsible for safeguarding highly sensitive information, ensuring compliance with security protocols, 
                and preventing unauthorized access to critical data.
                """,
    verbose = True,
    allow_delegation = False,
    llm = llm
)

#creating Public Data detection agent
public_data_agent = Agent(
    role = "Public Relations Specialist ",
    goal = "Check in the given information if any Public Data is present.",
    backstory = """
                This agent is specialized in understanding and managing public data such as press releases, publicly available financial reports, published research papers, 
                company marketing materials, public blog posts, news articles, public government records, public social media posts, product catalogs,
                and user manuals of a company very well. This agent is responsible for handling and disseminating public information, ensuring that 
                the company's public data is accurate, consistent, and effectively communicates the intended message to the public.
                """,
    verbose = True,
    allow_delegation = False,
    llm = llm
)


#creating Tasks


