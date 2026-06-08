import requests

from .monitor import analyze_response


class GhostGrid:

    def __init__(
        self,
        base_url="http://127.0.0.1:8000"
    ):
        self.base_url = base_url

    def register_agent(
        self,
        name
    ):

        payload = {
            "name": name
        }

        response = requests.post(
            f"{self.base_url}/agents/register",
            json=payload
        )

        return response.json()

    def list_agents(
        self
    ):

        response = requests.get(
            f"{self.base_url}/agents"
        )

        return response.json()

    def delete_agent(
        self,
        agent_id
    ):

        response = requests.delete(
            f"{self.base_url}/agents/{agent_id}"
        )

        return response.json()

    def log_event(
        self,
        agent_id,
        event_type,
        severity
    ):

        payload = {
            "agent_id": agent_id,
            "event_type": event_type,
            "severity": severity
        }

        response = requests.post(
            f"{self.base_url}/events/log",
            json=payload
        )

        return response.json()

    def get_trust_score(
        self,
        agent_id
    ):

        response = requests.get(
            f"{self.base_url}/agents/{agent_id}/trust-score"
        )

        return response.json()

    def get_insights(
        self,
        agent_id
    ):

        response = requests.get(
            f"{self.base_url}/agents/{agent_id}/insights"
        )

        return response.json()

    def monitor_agent(
        self,
        agent_id,
        response
    ):

        analysis = analyze_response(
            response
        )

        return self.log_event(
            agent_id=agent_id,
            event_type=analysis["event_type"],
            severity=analysis["severity"]
        )