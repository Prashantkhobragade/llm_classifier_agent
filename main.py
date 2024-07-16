import os
import base64
#from openai import OpenAI
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
#from langchain_openai import AzureChatOpenAI
from langchain_groq import ChatGroq
#from crewai_tools import SerperDevTool



load_dotenv()

groq_api_key = os.environ["GROQ_API_KEY"]
SERPER_API_KEY = os.environ['SERPER_API_KEY']

llm = ChatGroq(
    model = "llama3-70b-8192",
    temperature = 0.0,
    api_key = groq_api_key
)

# Instantiate tools
#search_tool = SerperDevTool()


##creating agents
#creating Private data detection agent
private_data_agent = Agent(
    role = "Private Data Detection",
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
#for company specific
internal_data_agent = Agent(
    role = "Internal Data Detection",
    goal = "Check if the given {information} contains the internal data of a {company} .",
    backstory = """This agent is specialized in checking Internal data of a {company} such as internal memos, company policies and procedures, 
                internal project plans, employee work schedules, internal meeting notes, staff directory and contact information, 
                internal financial statements, non-public marketing strategies, internal training materials, 
                and employee performance reviews. you are responsible for managing, safeguarding, and ensuring the proper use of internal company information""",
    #tools = [search_tool],
    verbose = True,
    allow_delegation = False,
    llm = llm
)


#creating Confidential data detection agent
confidential_data_agent = Agent(
    role = "Confidential Data Detection",
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
    role = "Restricted Data Detection.",
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
    role = "Public Data Detection",
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



summary_agent = Agent(
    role = "Create brife summary",
    goal = "Create a brife summary about what all above Agents has returns",
    backstory = """This agent is a specialized AI agent designed to integrate and summarize the outputs of five distinct data-handling agents. 
                    Each of these agents focuses on a specific category of data, ensuring comprehensive and secure processing. 
                    summary_agent's primary mission is to provide a clear, cohesive summary of the work done by all five agents, 
                    delivering valuable insights and actionable information.""",
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
    description = "Analyze the given information and determine if any Internal data of the {company} is available within it.",
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

summary_task = Task(
    description = "provide a clear, cohesive summary of the work done by all five agent",
    agent = summary_agent,
    expected_output = "Summaries all the output from the Agents (Only True and False with Agent Name) in Json format"
)




    #Crew
crew = Crew(
            agents = [private_data_agent, internal_data_agent, 
                    confidential_data_agent, restricted_data_agent, public_data_agent, summary_agent],
            tasks = [private_data_task, internal_data_task,
                    confidential_data_task, restricted_data_task, public_data_task, summary_task],
            #process = Process.sequential,
            #manager_agent=manager_agent,
            verbose = 2
            )


result = crew.kickoff(inputs = {"information": """ Acme Inc. Internal Memo

To: All Acme Inc. Employees
From: John Doe, CEO
Date: July 15, 2024
Subject: Strategic Initiative and Upcoming Changes

Dear Team,

As we continue to strive for excellence and growth at Acme Inc., it is crucial that we keep everyone informed about our strategic initiatives and upcoming changes. This memo contains sensitive information that should not be shared outside of the company. Your cooperation in maintaining the confidentiality of this information is greatly appreciated.

1. Internal Project Plans:

We are embarking on Project Phoenix, which aims to overhaul our current supply chain management system. The goal is to improve efficiency, reduce costs, and enhance our ability to meet customer demands. This project will be executed in three phases over the next 18 months. Details about the project timeline, key milestones, and team assignments will be shared during the upcoming department meetings.

2. Company Policies and Procedures:

Starting next month, we will be implementing new remote work policies. Employees will be required to work from the office at least three days a week, with the option to work remotely on the remaining two days. This change aims to balance flexibility with the need for in-person collaboration.

3. Employee Work Schedules:

To support the new remote work policy, we are introducing a flexible scheduling system. Employees can choose their in-office days based on team needs and personal preferences, subject to manager approval. Detailed guidelines will be distributed next week.

4. Internal Financial Statements:

Our Q2 financial results indicate a 12% increase in revenue compared to last year, largely driven by the successful launch of our new product line. However, operating expenses have also risen by 8% due to increased investment in research and development. The finance team is working on a detailed report that will be shared with senior management.

5. Non-public Marketing Strategies:

We are planning a major marketing campaign for Q4, focused on our new eco-friendly product range. The campaign will include targeted digital advertising, influencer partnerships, and a series of sustainability-themed events. Details about the campaign strategy and execution plan will be shared in the next marketing department meeting.

6. Internal Training Materials:

To support our strategic initiatives, we are rolling out new training programs for employees. These programs will cover advanced data analytics, supply chain optimization, and customer relationship management. Training schedules and materials will be available on the internal portal starting next month.

7. Employee Performance Reviews:

The annual performance review process will begin in August. Managers will receive detailed guidelines and templates for conducting reviews. Employees are encouraged to complete their self-assessments by the end of July.

Please remember that all the information contained in this memo is confidential and should not be disclosed to anyone outside of Acme Inc. If you have any questions or need further clarification, feel free to reach out to your department head.

Thank you for your continued dedication and hard work.

Best regards,

John Doe
CEO, Acme Inc""",
"company": "Acme Inc."}
                            )


#print(result.usage_metrics())


#langchain_visualizer.visualize(crew_agent)


#langchain visulizer ---->> some dependency issues with crewai and langchain
