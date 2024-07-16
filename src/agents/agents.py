from crewai import Agent
from langchain_groq import ChatGroq

import os
import logging
from dotenv import load_dotenv

#load env variable
load_dotenv

try:
    Groq_API_KEY = os.getenv("Groq_API_KEY")
    if not Groq_API_KEY:
        raise ValueError("Groq api key is not found")
except:
    print("Error: Groq API key is not found")

class LLMClasifierAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model = "llama3-70b-8192",
            temperature = 0.0,
            api_key = Groq_API_KEY
            )
        
    def private_data_agent(self):
        return Agent(
            role = "Private Data Detection",
            goal = "Check if the given {information} contains any Private Data.",
            backstory = """This agent is specialized in Checking private data such as Personal Identification Numbers (e.g., Social Security Numbers),
                        Medical Records, Biometric Data (e.g., fingerprints, retina scans), Personal Financial Information (e.g., bank account details, credit card numbers),
                        Private Communications (e.g., emails, text messages), Home Addresses, Phone Numbers, Birth Dates, Private Photos and Videos
                        Passwords and PINs. You are knowledgeable about the principles, laws, and practices related to the protection and management 
                        of personal and sensitive data. """,
            verbose = True,
            #max_rpm = 2,
            allow_delegation = False,
            llm = self.llm
            )
    

    def internal_data_agent(self):
        return  Agent(
            role = "Internal Data Detection",
            goal = "Check if the given {information} contains the internal data of a {company} .",
            backstory = """This agent is specialized in checking Internal data of a {company} such as internal memos, company policies and procedures, 
                        internal project plans, employee work schedules, internal meeting notes, staff directory and contact information, 
                        internal financial statements, non-public marketing strategies, internal training materials, 
                        and employee performance reviews. you are responsible for managing, safeguarding, and ensuring the proper use of internal company information""",
            #tools = [search_tool],
            verbose = True,
            #max_rpm = 2,
            allow_delegation = False,
            llm = self.llm
            )
    
    def confidential_data_agent(self):
        return Agent(
            role = "Confidential Data Detection",
            goal = "Check in the given {information} if any Confidential Data is present.",
            backstory = """
                    This agent understands and manages confidential data such as trade secrets, proprietary algorithms, research and development data, 
                    customer data, contractual agreements, strategic plans, legal documents, vendor information, M&A documents, and confidential business 
                    reports. the agent is professional and responsible for ensuring that sensitive and confidential information is protected from unauthorized access 
                    and disclosure, and is handled in compliance with legal and regulatory requirements
                """,
            verbose = True,
            #max_rpm = 2,
            allow_delegation = False,
            llm = self.llm
            )
    

    def restricted_data_agent(self):
        return Agent(
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
            #max_rpm = 2,
            allow_delegation = False,
            llm = self.llm
            )
    

    def public_data_agent(self):
        return Agent(
            role = "Public Data Detection",
            goal = "Check in the given {information} if any Public Data is present.",
            backstory = """
                    This agent is specialized in understanding and managing public data such as press releases, publicly available financial reports, published research papers, 
                    company marketing materials, public blog posts, news articles, public government records, public social media posts, product catalogs,
                    and user manuals of a company very well. This agent is responsible for handling and disseminating public information, ensuring that 
                    the company's public data is accurate, consistent, and effectively communicates the intended message to the public.
                    """,
            verbose = True,
            #max_rpm = 2,
            allow_delegation = False,
            llm = self.llm
            )
    

    def summary_agent(self):
        return Agent(
            role = "Create brief summary",
            goal = "Summarize the output of the Agents.",
            backstory = """This agent is a specialized AI agent designed to integrate and summarize the outputs of five distinct data-handling agents 
                    (i.e private_data_agent, internal_data_agent, confidential_data_agent, restricted_data_agent, public_data_agent). 
                    Each of these agents focuses on a specific category of data, ensuring comprehensive and secure processing. 
                    summary_agent's primary mission is to provide a clear, cohesive summary of the work done by all five agents, convert the output
                    into JSON format and delivering valuable insights and actionable information.""",
            verbose = True,
            #max_rpm = 2,
            allow_delegation = False,
            llm = self.llm
)


