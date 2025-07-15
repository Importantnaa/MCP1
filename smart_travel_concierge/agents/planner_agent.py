import re
import json

class PlannerAgent:
    def __init__(self, user_goal):
        self.user_goal = user_goal.lower()
        self.output = {
            "subtasks": [],
            "location": "",
            "dates": {},
            "travelers": {},
            "budget": {}
        }

    def parse(self):
        # Location
        if "umrah" in self.user_goal:
            self.output["location"] = "Makkah, Saudi Arabia"

        # Dates
        if "december" in self.user_goal:
            self.output["dates"] = {
                "start": "2025-12-10",
                "end": "2025-12-15"
            }

        # Travelers
        adults = re.search(r'(\d+)\s*adults?', self.user_goal)
        children = re.search(r'(\d+)\s*children?', self.user_goal)
        self.output["travelers"] = {
            "adults": int(adults.group(1)) if adults else 1,
            "children": int(children.group(1)) if children else 0
        }

        # Budget
        if "budget" in self.user_goal or "cheap" in self.user_goal:
            self.output["budget"] = {
                "level": "low",
                "estimated_total_usd": 2500
            }

        # Subtasks
        self.output["subtasks"] = [
            "Find budget round-trip flights to Jeddah (JED)",
            "Book hotel near Masjid al-Haram in Makkah",
            "Suggest affordable halal food options nearby",
            "Build daily prayer-friendly and rest-optimized itinerary"
        ]

    def get_output(self):
        self.parse()
        return {
            "agent": "PlannerAgent",
            "goal": "Break down user trip request into structured subtasks",
            "input": {
                "user_goal": self.user_goal
            },
            "output": self.output
        }
