from sdk import GhostGrid

gg = GhostGrid()

print("\nAGENTS")
print(
    gg.list_agents()
)

print("\nDELETE")
print(
    gg.delete_agent(4)
)

print("\nAGENTS AFTER DELETE")
print(
    gg.list_agents()
)