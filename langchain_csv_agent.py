from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import create_csv_agent
from dotenv import load_dotenv 
import os

def main():
    load_dotenv()
    project_dir = os.path.dirname(os.path.abspath(__file__))
    filename = 'test_stock.csv'
    csv_file = os.path.join(project_dir, 'data', filename)
    agent = create_csv_agent(
        OpenAI(temperature=0),
        csv_file,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )
    #question = "price of tesla"
    question = "stocks which gain < -60%"
    answer = agent.run(question)
    print(f"question={question}, ans={answer}")

if __name__ == "__main__":
    main()