from setuptools import setup, find_packages

setup(
    name="falconi",
    version="0.0.1",
    description="An eample of running Falcon on AWS Lambda",
    package=find_packages("src"),
    package_dir={"": "src"},
)

