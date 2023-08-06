import argparse
import dataclasses

from traveltask_google_artifact_registry.config import TaskConfig
from traveltask_google_artifact_registry.task import perform


def parse_arguments() -> dict:

    # Get all fields of the config
    fields = {field.name: field.type for field in dataclasses.fields(TaskConfig)}

    # Parse arguments
    parser = argparse.ArgumentParser()
    for name, kind in fields:
        parser.add_argument(f"--{name}", type=kind)

    # Convert to dictionary
    return vars(parser.parse_args())

def main():

    # Parse arguments and perform the task
    args = parse_arguments()
    perform(TaskConfig(**args))


if __name__ == '__main__':

    main()
