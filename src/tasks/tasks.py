from crewai import Task
from textwrap import dedent

class LLMClassifierTask:
    def private_data_task(self, agent, information):
        return Task(description = dedent(
            f"""
            **Task**: Analyze the given information.
            **Description**: Analyze the provided data to identify any private data elements,
        such as personal identification numbers, medical records, biometric data, personal financial
        information, private communications, home addresses, phone numbers, birth dates, passwords, and PINs.

        **Parameters**:
        - Information: {information}

        """
        ),
        agent = agent,
        expected_output = "If private data is found, return True along with the private data, else return False."
        )
    

    def internal_data_task(self, agent, information, company):
        return Task(
            description = dedent(
                f"""
                **Task**: Analyze the given information.
                **Description**: Analyze the provided data to identify any internal data elements of company, such as internal memos, 
                company policies and procedures, internal project plans, employee work schedules, internal meeting notes, staff directory 
                and contact information, internal financial statements, non-public marketing strategies, internal training materials, 
                and employee performance reviews.

                **Parameters**:
                - Information : {information}
                - Company : {company}
                """
            ),
            agent = agent,
            expected_output = "If Internal data is found, return True along with the internal data, else return False."          
        )
    

    def confidential_data_task(self, agent, information, company):
        return Task(
            description = dedent(
                f"""
                **Task**: Analyze the given information.
                **Description**: Analyze the provided data to identify any confidential information related to company, such as trade secrets, 
                proprietary algorithms, research and development data, customer data, contractual agreements, strategic plans, 
                legal documents, vendor information, M&A documents, and confidential business reports.

                **Parameters**:
                - Information : {information}
                - Company : {company}
                """
            ),
            agent = agent,
            expected_output = "If confidential data is found, return True along with the confidential data, else return False."
        )
    
    def restricted_data_task(self, agent, information):
        return Task(
            description = dedent(
                f"""
                **Task**: Analyze the given information.
                **Description**: Analyze the provided data to identify any restricted information, such as 
                national security information, classified government documents, security codes and access controls, 
                critical infrastructure data, law enforcement investigation reports, sensitive intelligence reports, 
                military operations information, highly sensitive financial data, critical research data, and highly sensitive personal information. 
                

                **Parameters**:
                - Information : {information}
                
                """
            ),
            agent = agent,
            expected_output = "If restricted data is found, return True along with the restricted data, else return False."
        )
    
    def public_data_task(self, agent, information, company):
        return Task(
            description = dedent(
                f"""
                **Task**: Analyze the given information.
                **Description**: Analyze the provided data to identify any public information related to company, such as press releases, 
                publicly available financial reports, published research papers, company marketing materials, public blog posts, 
                news articles, public government records, public social media posts, product catalogs, and user manuals of a company.

                **Parameters**:
                - Information : {information}
                - Company : {company}
                """
            ),
            agent = agent,
            expected_output = "If confidential data is found, return True along with the confidential data, else return False."
        )
    
    def summary_task(self, agent):
        return Task(
            description = dedent(
                f"""
                **Task**: Create Summary .
                **Description**: provide a clear, cohesive summary of the work done by all five agents
                                    (i.e private_data_agent, internal_data_agent, confidential_data_agent, restricted_data_agent, public_data_agent). 

                """
            ),
            agent = agent,
            expected_output = "Output of all the Agents (only True or False) in JSON format"
        )
