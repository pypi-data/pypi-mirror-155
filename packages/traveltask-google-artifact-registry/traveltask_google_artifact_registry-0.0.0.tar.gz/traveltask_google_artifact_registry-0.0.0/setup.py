from setuptools import setup, find_packages
import os


# Read requirements
requirements_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
with open(requirements_file, "r") as f:
    requirements = f.read().splitlines()


# Package configuration
_NAME = "traveltask_google_artifact_registry"
setup(
    name=_NAME,
    version="0.0.0",
    description="A Travel Task to download/upload a Python package from/to Google Artifact Registry using Pip",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements
)
