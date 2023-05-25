import os
import langchain
import json 
from langchain.llms import OpenAI 
from langchain.agents import load_tools
from langchain.agents import initialize_agent

gpt3 = OpenAI(model_name='text-davinci-003', temperature =0)
# ollm = OpenAI(temperature=0.7) #OpenAI LLM with a temperature of 0.7 increasing its creativity 

#The search tool used to search the internet
tool_names = ["serpapi"]
tools = load_tools(tool_names)

#Initializing the agent that uses the search tool and the openAI LLM to answer questions
agent = initialize_agent(tools, llm =gpt3 , agent="zero-shot-react-description", verbose=True)


def scrape(company_name, country, url=None):
    ''' 
    Function that takes in Company and country, 
    and searches the internet to get's the description and then gets 
    the products and services from the description as a commaseperated list. 

    Keyword arguments:
    company_name: str 
    country: str 

    Returns 
    (Description : str, products :str) : tuple
       
    '''
    # details = ''
    try:
        query = f'''
            I need you to answer some questions about the company in double  quotes ''{company_name}'' that is based in this country in angle brackets <{country}> :
            Before giving the answer to the questions check for the following:
            1 - Find out information about the Company and make a clear distinction between their products and services 
            2 - Check if they have products, if they don't have, just put no products 
            3 - Check if they have Services that can be listed in a one word comma seperated list, if they don't have, just put no services 

            Here are the questions
            1 - Provide no less than a two sentence description of the company, that focuses on the industry it operates in, its country, its products and services.
            2 - What are all the Products the company offers ?, output this in a one to two word comma seperated list.
            3 - What are all the Services the company offers ?, output this in a one to two word comma seperated list.
            4 - What are the key words associated with this company and its product ?, output not less than 3 words in a comma seperated list.

            Return a JSON object with the following keys: Description,Keywords, Products, Services, where the products and services are in a list and not a string object. 
            
            Make sure to use double quotes for the keys of the JSON object
            Make sure the description is not less than two sentences. 
            Make sure the services is a valid type of service that can be rendered by a company. 
        '''
        
    
        details = agent.run(query)

        
        new = json.loads(details)

        new_dict ={'Products': new["Products"], 'Services': new["Services"]}
        print(new["Products"])
        

        
        query2 = f'''
        I need you to answer some questions about the values in the Python Dictionary Object in double  quotes ''{new_dict}'' : 
        1 - What are the SIC codes from the SEC for each of the Values in the Key in angle brackets, <Products>, output in a comma seperated list 
        2 - What are the SIC codes from the SEC for each of the Values in the Key in triple back ticks, ```Services```, output in a comma seperated list 
        3 - What are the NAICS codes for the each of Values in the Key in angle brackets, <Products>, output in a comma seperated list 
        4 - What are the NAICS codes for the each of Values in the Key in triple back ticks, ```Services```, output in a comma seperated list

        Make sure to take your time to go through each value in the keys specified and find the answer for each value.

        Return a JSON object with the following keys: SIC Products, SIC Services, NAICS Products, NAICS Services, where all the values are in a list and not a string object.
        Make sure to use double quotes for the keys of the JSON object
        Make sure to find the codes for each value seperately.
        '''

        s_n_codes = agent.run(query2)
        # docs1 = [Document(page_content=description)]
        # query1 = "only give me a comma seperated list of the products and services offered that are related to the industry, with their complete names"
        # chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
        # products = chain.run(input_documents=docs1, question=query1)

        return (details,s_n_codes)
        # return products
    except Exception as e:
        print(e)
        return 'There was an error. Try again!'


if __name__ == '__main__':
    answer = agent.run(f"What products/services does the company Google offer?")
    print(answer)