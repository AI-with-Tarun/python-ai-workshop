from state import graph_builder
import pandas as pd
from ragas import EvaluationDataset
from ragas import evaluate
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness
from config import configure
import os

os.environ['OPENAI_API_KEY'] = configure.OPENAI_API_KEY

path = "./data/ragas_dataset.csv"
df = pd.read_csv(path)
df['reference_contexts'] = df['reference_contexts'].apply(eval)
retrieved_contexts = []
response = []

for query in df['user_input']:
    graph = graph_builder()
    result = graph.invoke({"query":query})
    
    response.append(result['answer'])
    retrieved_contexts.append(result['context'])

df['retrieved_contexts'] = retrieved_contexts
df['response'] = response

df.to_csv("final_response.csv", index=False)

# below code on VS Code
import pandas as pd

df = pd.read_csv("final_response.csv")
df['reference_contexts'] = df['reference_contexts'].apply(eval)
df['retrieved_contexts'] =df['retrieved_contexts'].apply(eval)

eval_dataset = EvaluationDataset.from_pandas(df)
print(eval_dataset)

result = evaluate(
    dataset = eval_dataset,
    metrics=[
        Faithfulness(),
        FactualCorrectness(),
        LLMContextRecall(),
    ],
)
print(result)