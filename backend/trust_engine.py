EVENT_SCORES = {
    "TASK_SUCCESS": 2,
    "TASK_FAILURE": -3,
    "HALLUCINATION": -5,
    "TOOL_MISUSE": -10,
    "SAFE_EXECUTION": 1
}

def calculate_score(current_score, event_type):

    impact = EVENT_SCORES.get(event_type, 0)

    return current_score + impact, impact
def get_risk_level(score):

    if score >= 80:
        return "LOW"

    elif score >= 50:
        return "MEDIUM"

    return "HIGH"