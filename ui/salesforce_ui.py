"""
Salesforce UI Toolkit.

https://developer.salesforce.com/
"""

from typing import Dict


class SalesforceUI:
    """Salesforce UI components."""
    
    @staticmethod
    def einstein_agent_component():
        """Einstein Agent."""
        return {"type": "agent", "component": "sf_einstein_agent"}
    
    @staticmethod
    def einstein_bot_component():
        """Einstein Bot."""
        return {"type": "bot", "component": "sf_einstein_bot"}
    
    @staticmethod
    def flow_component():
        """Flow Builder."""
        return {"type": "flow", "component": "sf_flow"}
