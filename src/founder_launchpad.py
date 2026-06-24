import json
from dataclasses import dataclass
from typing import List

@dataclass
class StackItem:
    name: str
    description: str
    cost_estimate: float

@dataclass
class TechStack:
    frontend: List[StackItem]
    backend: List[StackItem]
    database: List[StackItem]
    hosting_provider: List[StackItem]

def suggest_tech_stack() -> TechStack:
    frontend = [StackItem("React", "A JavaScript library for building user interfaces", 1000.0)]
    backend = [StackItem("Node.js", "A JavaScript runtime for building server-side applications", 2000.0)]
    database = [StackItem("MongoDB", "A NoSQL database for storing and retrieving data", 500.0)]
    hosting_provider = [StackItem("AWS", "A cloud hosting provider for deploying applications", 1500.0)]
    return TechStack(frontend, backend, database, hosting_provider)

def display_tech_stack(stack: TechStack) -> str:
    if not isinstance(stack, TechStack):
        raise AttributeError("Invalid TechStack object")
    output = ""
    output += "Frontend:\n"
    for item in stack.frontend:
        output += f" - {item.name}: {item.description}, Cost Estimate: ${item.cost_estimate:.2f}\n"
    output += "Backend:\n"
    for item in stack.backend:
        output += f" - {item.name}: {item.description}, Cost Estimate: ${item.cost_estimate:.2f}\n"
    output += "Database:\n"
    for item in stack.database:
        output += f" - {item.name}: {item.description}, Cost Estimate: ${item.cost_estimate:.2f}\n"
    output += "Hosting Provider:\n"
    for item in stack.hosting_provider:
        output += f" - {item.name}: {item.description}, Cost Estimate: ${item.cost_estimate:.2f}\n"
    return output
