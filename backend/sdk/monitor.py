def analyze_response(response):

    response = response.lower()

    if len(response) < 10:
        return {
            "event_type": "TOOL_FAILURE",
            "severity": "MEDIUM"
        }

    if "i don't know" in response:
        return {
            "event_type": "HALLUCINATION",
            "severity": "HIGH"
        }

    if "error" in response:
        return {
            "event_type": "TOOL_FAILURE",
            "severity": "HIGH"
        }

    return {
        "event_type": "TASK_SUCCESS",
        "severity": "LOW"
    }