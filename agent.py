from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from calendar_utils import get_available_slots, book_event

def check_slots(date: str, duration: int = 30):
    slots = get_available_slots(date, duration)
    return [f"{s[0].strftime('%H:%M')} - {s[1].strftime('%H:%M')}" for s in slots]

def book_slot(start: str, end: str, summary: str = "Meeting", desc: str = "Booked via Assistant"):
    link = book_event(datetime.fromisoformat(start), datetime.fromisoformat(end), summary, desc)
    return f"Booked successfully: {link}"

tools = [
    Tool(name="Check Availability", func=check_slots, description="Get available time slots for a given date"),
    Tool(name="Book Slot", func=book_slot, description="Book a slot given start and end time")
]

llm = ChatOpenAI(temperature=0, model="gpt-4")
agent = initialize_agent(tools, llm, agent="chat-conversational-react-description", verbose=True)

def chat_with_agent(message):
    return agent.run(message)