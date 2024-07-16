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
                of personal and sensitive data. """,
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
    goal = "Check in the given {information} if any Restricted Data is available.",
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
    goal = "Summarise the output of the Agents.",
    backstory = """This agent is a specialized AI agent designed to integrate and summarize the outputs of five distinct data-handling agents 
                    (i.e private_data_agent, internal_data_agent, confidential_data_agent, restricted_data_agent, public_data_agent). 
                    Each of these agents focuses on a specific category of data, ensuring comprehensive and secure processing. 
                    summary_agent's primary mission is to provide a clear, cohesive summary of the work done by all five agents, convert the output
                    into JSON format and delivering valuable insights and actionable information.""",
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
    description = "provide a clear, cohesive summary of the work done by all five agents",
    agent = summary_agent,
    expected_output = "output from above created agents, only True and False in json format"
)




    #Crew
crew = Crew(
            agents = [private_data_agent, internal_data_agent, 
                    confidential_data_agent, restricted_data_agent, public_data_agent, summary_agent],
            tasks = [private_data_task, internal_data_task,
                    confidential_data_task, restricted_data_task, public_data_task, summary_task],
            #process = Process.sequential,
            #manager_llm=llm,
            #manager_agent=manager_agent,
            verbose = False
            )


result = crew.kickoff(inputs = {"information": """ABC Pvt Ltd Expands Market Reach with $200 Million Acquisition of XYZ Company

– ABC Pvt Ltd, a renowned AI company, has announced its acquisition of XYZ Company for $200 million USD, solidifying its position as a leader in AI. This strategic acquisition is set to bolster ABC Pvt Ltd's portfolio and strengthen its competitive edge in the global market.

The acquisition of XYZ Company, known for its Data Driven Solutions, is expected to bring synergies that will benefit both companies. ABC Pvt Ltd aims to integrate XYZ Company's expertise and resources to enhance its product offerings and broaden its market footprint.

"We are pleased to complete the acquisition of XYZ Company," commented MR. KAALA, CEO of ABC Pvt Ltd. "This transaction aligns with our strategic growth objectives, allowing us to diversify our capabilities and better serve our customers."

The acquisition is part of ABC Pvt Ltd's broader strategy to expand into new markets and reinforce its commitment to innovation and customer satisfaction. ABC Pvt Ltd plans to maintain XYZ Company's operations and employees, ensuring a smooth transition and continuity of service for existing customers.

For more information on ABC Pvt Ltd's latest acquisition and its impact on the industry, please visit www.abcai.com.


                                    """,
"company": "XYZ Corporation."}
                            )


#print(result.usage_metrics())


#langchain_visualizer.visualize(crew_agent)


#langchain visulizer ---->> some dependency issues with crewai and langchain
