## AI Agent

Agent is combining LLM and self-defined tool. 
The core idea is we can use LLM to choose which action(=means tools) we want to take next and eventually to find out answer. 
By using our own defined tool, we can answer questions more accurately. For example, our tools can import our own documents or our tools can apply our own analysises.

### Background idea of AI Agent

Agent is based on [ReAct Pattern](https://react-lm.github.io/)(=Reason+Act).

### Setup
1. `pipenv shell`
2. `pipenv install`
3. need to update open api key in `.env.example` and change to `.env`

### How to Use
The repo includes 2 sample:
- `langchaing_csv_agent.py`: It is using langchain `create_csv_agent`.
- `csv_agent.py`: It is implement ReAct Pattern directly and also implement CSVReader as self-defined tool. The whole idea is referencing [Simple ReAct Agent](https://til.simonwillison.net/llms/python-react-pattern).


### Reference
- [LangChain Agent](https://python.langchain.com/docs/modules/agents.html)
- [Simple ReAct Agent](https://til.simonwillison.net/llms/python-react-pattern)