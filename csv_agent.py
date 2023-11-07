import openai
import pandas as pd
import os
import re
from difflib import SequenceMatcher
from collections import defaultdict

class CSVBot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})
    
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
    
    def execute(self):
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        # print(completion.usage)
        return completion.choices[0].message.content

class CSVReader:
    def  __init__(self, filename):
        self.handler = open(filename)
        self.df = pd.read_csv(filename)
        
    def find_row(self, name):
        for index, row in self.df.iterrows():
             for c in row:
                 if isinstance(c, str) and name.upper() in c:
                     return row
        
        return f"can't find row contains {name}, try find_column with {name}"

    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    def find_condition(self, operators, raw):
        for op in operators:
            parts = raw.split(op)
            
            if len(parts)>1: 
                operator = op
                right = parts[1]
                return operator, right

        return None, 0


    def find_column(self, condition):
        scores = defaultdict(float)
        for col in self.df:
            score = self.similar(col, condition)
            scores[col] = score

        sorted_score = [k for k, v in sorted(scores.items(), key=lambda item:item[1], reverse=True)]
        print(f"target column = {sorted_score[0]}")
        
        #check if condition exist
        operators = [">=", "<=", ">", "<", "="]
        operator, value = self.find_condition(operators, condition)
        
        print(f"condition={operator}, {value}") 
        if operator != None:
            ## Remove the '%' sign
            target_df = self.df[sorted_score[0]].str.replace("%", "")
            ## Convert to numeric, coercing errors to NaN
            target_df = pd.to_numeric(target_df, errors='coerce')
            target_df = target_df.astype('float')
            
            dest_value = float(value.replace("%", ""))

            if operator == '>':
                filtered_df = self.df[target_df > dest_value]
            elif operator == '<':
                filtered_df = self.df[target_df < dest_value]
            elif operator == '=':
                filtered_df = self.df[target_df == dest_value]
            elif operator == '>=':
                filtered_df = self.df[target_df >= dest_value]
            elif operator == '<=':
                filtered_df = self.df[target_df <= dest_value]
            return filtered_df
        
        return f"can't find column contains {condition}"
        

def query(question, reader, max_turns=5):
    prompt = """
    You run in a loop of Thought, Action, PAUSE, Observation.
    At the end of the loop you output an Answer
    Use Thought to describe your thoughts about the question you have been asked.
    Use Action to run one of the actions available to you - then return PAUSE.
    Observation will be the result of running those actions.

    Your available actions are:
    find_row, find_column
    
    Always look things up on find_row if you have the opportunity to do so.
    
    Example session:
    Question: stock price of tesla
    Thought: I need to find the row with tesla
    Action: find_row: tesla
    PAUSE

    You will be called again with Observation

    """.strip()
    action_re = re.compile('^Action: (\w+): (.*)$')

    known_actions = {
        "find_row": reader.find_row,
        "find_column": reader.find_column
    }

    i = 0
    bot = CSVBot(prompt)
    next_prompt = question
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)
        actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
        if actions:
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = "Observation: {}".format(observation)
        else:
            start = result.find("Observation:")
            ans = result[start+len("Observation:"):]
            return f"final answer: {ans}"
    
def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    filename = 'test_stock.csv'
    csv_file = os.path.join(project_dir, 'data', filename)
    reader = CSVReader(csv_file)
    
    # question = "price of tesla"
    question = "gain < -60%"
    ans = query(question, reader)
    print(ans)
    
if __name__=="__main__":
    main()    
    

