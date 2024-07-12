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
    goal = "Check if the given {information} contains any Private Data.",
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
internal_data_agent = Agent(
    role = "corporate data manager",
    goal = """Check if the given {information} contains the internal data of a company including """,
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
    goal = "Check in the given {information} if any Confidential Data is present.",
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
    goal = "Check in the given {information} if any Restricted Data is passed.",
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
    goal = "Check in the given {information} if any Public Data is present.",
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
private_data_task = Task(
    description = "Analyze the given information and determine if any private data is available within it.",
    agent = private_data_agent,
    expected_output = "Private Data True or False"
)

internal_data_task = Task(
    description = "Analyze the given information and determine if any Internal data is available within it.",
    agent = internal_data_agent,
    expected_output = "Internal data True or False"
)

confidential_data_task = Task(
    description = "Analyze the given information and determine if any Confidential data is available within it.",
    agent = confidential_data_agent,
    expected_output = "Confidential data True or False."
)

restricted_data_task = Task(
    description = "Analyze the given information and determine if any restricted data is available within it.",
    agent = restricted_data_agent,
    expected_output = "restricted data True or False."
)

public_data_task = Task(
    description = "Analyze the given information and determine if any Public data is available within it.",
    agent = public_data_agent,
    expected_output = "Public data True or False."
)




    #Crew
crew = Crew(
            agents = [private_data_agent, internal_data_agent, 
                    confidential_data_agent, restricted_data_agent, public_data_agent],
            tasks = [private_data_task, internal_data_task,
                    confidential_data_task, restricted_data_task, public_data_task],
            #process = Process.sequential,
            verbose = 2
            )


result = crew.kickoff(inputs = {"information": """

                                Jane Doe, residing at 123 Elm Street, Springfield, has been using her bank account number 9876543210 and 
                                credit card number 4111 1111 1111 1111 
                                for recent transactions. Her Social Security Number is 555-55-5555, and she has biometric data, 
                                including fingerprints and retina scans, stored for security purposes. Jane recently received a 
                                text message from her doctor’s office, reminding her of an appointment on July 15, 2024, 
                                for a medical checkup, which included details of her recent lab results. 
                                Her phone number is (555) 123-4567, and her birth date is January 1, 1980. 
                                Jane’s private photos and videos are stored in a secured digital vault with a password, 
                                which is “J@neD0e2024,” and her PIN is 1234.

                                            """})
