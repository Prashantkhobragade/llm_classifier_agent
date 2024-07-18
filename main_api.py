from crewai import Crew
from textwrap import dedent
from src.agents import LLMClassifierAgent
from src.tasks import LLMClassifierTask
import os
import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

class InputData(BaseModel):
    information: str
    company: str


class LLMClassifier:
    def __init__(self, information: str, company: str):
        self.information = information
        self.company = company


    def run(self)-> Dict[str, Any]:
        try:
            agents = LLMClassifierAgent()
            tasks = LLMClassifierTask()
        
            private_data_agent = agents.private_data_agent()
            internal_data_agent = agents.internal_data_agent()
            confidential_data_agent = agents.confidential_data_agent()
            restricted_data_agent = agents.restricted_data_agent()
            public_data_agent = agents.public_data_agent()
            summary_agent = agents.summary_agent()

            private_data = tasks.private_data_task(
                private_data_agent,
                self.information
            )

            internal_data = tasks.internal_data_task(
                internal_data_agent,
                self.information,
                self.company
            )

            confidential_data = tasks.confidential_data_task(
                confidential_data_agent,
                self.information,
                self.company
            )

            restricted_data = tasks.restricted_data_task(
                restricted_data_agent,
                self.information
            )

            public_data = tasks.public_data_task(
                public_data_agent,
                self.information,
                self.company
            )

            summary = tasks.summary_task(
                summary_agent
            )

            #Define your crew
            crew = Crew(
                agents = [private_data_agent,
                        internal_data_agent,
                        confidential_data_agent,
                        restricted_data_agent,
                        public_data_agent,
                        summary_agent],

                tasks = [private_data, internal_data, confidential_data, restricted_data, public_data, summary], 
                verbose=True
            )

            result = crew.kickoff()
            return result
        
        except Exception as e:
            logger.error("Error in LLMClassifier running: %s", e)
            raise HTTPException(status_code=500, detail=str(e))
    


@app.post("/classify/")
async def classify(input_data: InputData):
    try:
        llm_classifier = LLMClassifier(input_data.information, input_data.company)
        result = llm_classifier.run()
        return result
    except Exception as e:
        logger.error("Error in endpoints: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
    


"""
if __name__ == "__main__":
    try:
        print("LLM Classifier Initiated")
        print("-------------------------------------")
        information = input(
            dedent("
                Enter your information
                ")
        )

        company = input("Enter Company Name: ")

        llm_classifier = LLMClassifier(information, company)
        result = llm_classifier.run()
        print("\n\n################################")
        print("## Classification Result")
        print("################################\n")
        print(result)
    except Exception as e:
        logger.error("Error in main execution: %s", e)
        raise
        
"""