from dataclasses import dataclass


@dataclass
class TaskConfig:

    # Travel parameters
    context: str
    task: str

    # Custom parameters
    project: str
    region: str
    repository: str
    action: str  # Can be upload or install
    packages: str = None
