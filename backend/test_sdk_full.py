from sdk import GhostGrid

gg = GhostGrid()

agent = gg.register_agent(
    "sdk-agent"
)

print("\nREGISTERED")
print(agent)

agent_id = agent["id"]

print("\nTRUST SCORE")
print(
    gg.get_trust_score(agent_id)
)

print("\nINSIGHTS")
print(
    gg.get_insights(agent_id)
)