import json
from dataclasses import dataclass
from typing import List

@dataclass
class Idea:
    name: str
    description: str

@dataclass
class Template:
    name: str
    description: str

@dataclass
class Metric:
    name: str
    value: int

class Launchpad:
    def __init__(self):
        self.ideas = []
        self.templates = [
            Template("Web App", "A basic web application template"),
            Template("Mobile App", "A basic mobile application template"),
        ]
        self.metrics = []

    def validate_idea(self, idea: Idea) -> str:
        if not idea.name or not idea.description:
            return "Invalid idea: name and description are required"
        self.ideas.append(idea)
        return "Idea validated successfully"

    def get_templates(self) -> List[Template]:
        return self.templates

    def get_dashboard(self) -> List[Metric]:
        self.metrics.append(Metric("Number of Ideas", len(self.ideas)))
        return self.metrics

def main():
    launchpad = Launchpad()
    idea = Idea("My Web App", "A web app for selling products")
    print(launchpad.validate_idea(idea))
    print(json.dumps([template.__dict__ for template in launchpad.get_templates()], indent=4))
    print(json.dumps([metric.__dict__ for metric in launchpad.get_dashboard()], indent=4))

if __name__ == "__main__":
    main()
