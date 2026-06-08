from sdk import GhostGrid

gg = GhostGrid()

result = gg.monitor_agent(
    agent_id=4,
    response="I don't know the answer."
)

print(result)