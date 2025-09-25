import kozmodb_sdk
from uuid import uuid4
import os

con = kozmodb_sdk.connect()

open_ai_key = os.getenv('OPENAI_API_KEY')
model_name = 'gpt-4o'

# Now create an agent that will use the model we just created.
agent = con.agents.create(name=f'kozmodb_retrieval_agent_{model_name}_{uuid4().hex}',
                          model=model_name,
                          params={'return_context': True})

agent.add_file('./data/tokaido-rulebook.pdf', 'rule book for the board game Tokaido')

question = "what are the rules for the game takaido?"
answer = agent.completion([{'question': question, 'answer': None}])
print(answer.context)
print(answer)

