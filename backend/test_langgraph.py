from langchain_core.messages import HumanMessage
from langgraph.graph import START, StateGraph
from typing import TypedDict

from sdk import GhostGrid


class State(TypedDict):
    question: str
    answer: str


gg = GhostGrid()


def chatbot(state: State):

    question = state["question"]

    if "capital" in question.lower():

        answer = "The capital of France is Paris."

    else:

        answer = "I don't know."

    return {
        "answer": answer
    }


builder = StateGraph(State)

builder.add_node(
    "chatbot",
    chatbot
)

builder.add_edge(
    START,
    "chatbot"
)

graph = builder.compile()


result = graph.invoke(
    {
        "question":
        "What is the capital of France?"
    }
)

print("\nLANGGRAPH OUTPUT")
print(result)


trust_result = gg.monitor_agent(
    agent_id=3,
    response=result["answer"]
)

print("\nGHOSTGRID RESULT")
print(trust_result)