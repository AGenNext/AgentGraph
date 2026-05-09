"""
01 Quick Chat - 5 lines of code.

Run: python examples/01_quick_chat.py
"""

from ui import create_chat

def my_agent(msg):
    return f"You said: {msg}"

demo = create_chat(my_agent, "Quick Chat")
demo.launch()
