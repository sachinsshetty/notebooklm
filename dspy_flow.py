import dspy
from typing import List, Dict
import googleapiclient.discovery  # Added for Google Calendar API (if used)
from datetime import datetime, timedelta
import os
import requests

# Environment variables
vllm_ip = os.getenv("VLLM_IP", "http://localhost")  # Default to localhost if not set
vllm_port = 8000  # Default vLLM port; adjust if different
DOORDASH_API_KEY = os.getenv("DOORDASH_API_KEY")


lm = dspy.LM("gemma3",
             api_base=f"{vllm_ip}:{vllm_port}/v1",  # ensure this points to your port
             api_key="local", model_type="chat")



dspy.configure(lm=lm)


# Mock APIs (replace with real API credentials and endpoints)
GOOGLE_CALENDAR_API = None  # Initialize with googleapiclient.discovery for real use

# DSPy Signatures
class IntentParser(dspy.Signature):
    """Parse a user request into intent and entities."""
    request: str = dspy.InputField()
    intent: str = dspy.OutputField(desc="Main goal of the request")
    entities: Dict[str, str] = dspy.OutputField(desc="Key details like time, people, location")

class TaskPlanner(dspy.Signature):
    """Generate a list of tasks to complete the request."""
    intent: str = dspy.InputField()
    entities: Dict[str, str] = dspy.InputField()
    tasks: List[str] = dspy.OutputField(desc="Ordered list of tasks to execute")

class DecisionMaker(dspy.Signature):
    """Make decisions based on available options."""
    context: str = dspy.InputField(desc="Current task and options")
    decision: str = dspy.OutputField(desc="Chosen option or action")

class ClarificationModule(dspy.Signature):
    """Generate a clarification question when needed."""
    context: str = dspy.InputField(desc="Ambiguous or missing information")
    question: str = dspy.OutputField(desc="Question to ask the user")

# DSPy Modules
class MeetingSchedulerAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.parser = dspy.Predict(IntentParser)
        self.planner = dspy.Predict(TaskPlanner)
        self.decision_maker = dspy.Predict(DecisionMaker)
        self.clarifier = dspy.Predict(ClarificationModule)

    def forward(self, request: str):
        parsed = self.parser(request=request)
        intent, entities = parsed.intent, parsed.entities

        plan = self.planner(intent=intent, entities=entities)
        tasks = plan.tasks

        results = []
        for task in tasks:
            result = self.execute_task(task, entities)
            if result.get("status") == "needs_clarification":
                question = self.clarifier(context=result["context"]).question
                return {"status": "clarification_needed", "question": question}
            results.append(result)

        return {"status": "completed", "results": results}

    def execute_task(self, task: str, entities: Dict[str, str]) -> Dict:
        if "check calendars" in task.lower():
            slots = self.check_calendars(entities.get("attendees", []), entities.get("duration", "2 hours"))
            if not slots:
                return {"status": "needs_clarification", "context": "No available slots found."}
            decision = self.decision_maker(context=f"Available slots: {slots}").decision
            entities["selected_slot"] = decision

        elif "book conference room" in task.lower():
            success = self.book_room(entities.get("selected_slot"), entities.get("room", "main conference room"))
            if not success:
                return {"status": "needs_clarification", "context": "Room unavailable."}

        elif "send calendar invites" in task.lower():
            self.send_invites(entities.get("attendees", []), entities.get("selected_slot"))

        elif "order catering" in task.lower():
            self.order_catering(entities.get("attendees", []), entities.get("selected_slot"))

        return {"status": "success", "task": task}

    def check_calendars(self, attendees: List[str], duration: str) -> List[str]:
        start_date = datetime.now() + timedelta(days=1)
        end_date = start_date + timedelta(days=7)
        slots = ["2025-07-22 10:00-12:00", "2025-07-23 14:00-16:00"]  # Mock data
        return slots

    def book_room(self, slot: str, room: str) -> bool:
        return True

    def send_invites(self, attendees: List[str], slot: str):
        pass

    def order_catering(self, attendees: List[str], slot: str):
        pass

# Voice Interface (Mock)
def speech_to_text(audio_input):
    return "Set up our quarterly review with the product team. Find a 2-hour slot that works for everyone and book the main conference room."

def text_to_speech(text):
    print(f"Speaking: {text}")

# Main Execution
def main():
    agent = MeetingSchedulerAgent()
    audio = None  # Mock audio input
    request = speech_to_text(audio)
    result = agent(request=request)
    if result["status"] == "clarification_needed":
        text_to_speech(result["question"])
    else:
        text_to_speech("Meeting scheduled successfully. Details sent to your email.")

if __name__ == "__main__":
    main()