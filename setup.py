from setuptools import setup, find_packages

# Read requirements from the file
with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="your_project_name",
    version="0.1",
    packages=find_packages(),
    install_requires=required,
)
