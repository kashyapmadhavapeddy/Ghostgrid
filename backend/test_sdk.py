from sdk import GhostGrid

gg = GhostGrid()

result = gg.log_event(
    agent_id=3,
    event_type="TASK_SUCCESS",
    severity="LOW"
)

print(result)