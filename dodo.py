import os
import shutil
import subprocess
import boto3

from zipfile import ZipFile

DOIT_CONFIG = {"verbosity": 2, "default_tasks": ["build", "deploy"]}

DIST_DIR = "dist"
BUILD_DIR = os.path.join(DIST_DIR, "build")
FUNCTION_NAME = "falcon-on-aws-lambda"

boto3.setup_default_session(profile_name="deploy")


def task_build():
    def mkdirs():
        """Makes dist and build directories"""
        if os.path.exists(DIST_DIR):
            shutil.rmtree(DIST_DIR)
        else:
            os.makedirs(BUILD_DIR)

    def install_packages():
        """Installs packages with Pipenv & pip"""
        with open("requirements.txt", "w") as requirements_file:
            subprocess.run(["pipenv", "lock", "-r"], stdout=requirements_file)

        subprocess.run(
            ["pip", "install", "-r", "requirements.txt", "--no-deps", "-t", BUILD_DIR]
        )

    def copy_source():
        """Copies source files & directories to build directory"""
        shutil.copytree("src", os.path.join(BUILD_DIR, "src"))
        for file in os.listdir("."):
            if os.path.isfile(file):
                shutil.copyfile(file, os.path.join(BUILD_DIR, file))

    def create_zip_file():
        """Creates a zip file of build directory"""
        shutil.make_archive(os.path.join(DIST_DIR, "build"), "zip", BUILD_DIR)

    return {"actions": [mkdirs, install_packages, copy_source, create_zip_file]}


def function_exists(client):
    """Determines if the function exists"""
    try:
        response = client.get_function(FunctionName=FUNCTION_NAME)
        print(response)
        return True
    except client.exceptions.ResourceNotFound as error:
        print(error)
        return False


def create_lambda_function(client):
    """Creates function code with build package in AWS Lambda"""
    try:
        # Blah ... this needs IAM junk and I'm too tired for that. I'll create it manually and move on for now.
        client.create_function(
            FunctionName=FUNCTION_NAME, RunTime="python3.8",
        )
    except client.exceptions.ServiceException as error:
        print(error)


def read_zip_file():
    """Reads build package and returns it in binary"""
    with open(os.path.join(DIST_DIR, "build.zip"), "rb") as zip_file:
        return zip_file.read()


def update_lambda_function(client):
    """Updates function code with build package in AWS Lambda"""
    try:
        update_options = {
            "FunctionName": FUNCTION_NAME,
            "ZipFile": read_zip_file(),
            "Publish": True,
        }
        client.update_function_code(**update_options)
    except client.exceptions.ServiceException as error:
        print(error)


def task_deploy():
    """Deploys build package to AWS Lambda"""
    client = boto3.client("lambda")

    def upload_build():
        if function_exists(client):
            update_lambda_function(client)
        else:
            create_lambda_function(client)

    return {"actions": [upload_build], "file_dep": [f"{DIST_DIR}/build.zip"]}


def task_tail_logs():
    def watch():
        actions = [
            "awslogs",
            "get",
            "/aws/lambda/falcon-on-aws-lambda",
            "--start=2h ago",
            "--watch",
        ]
        os.environ["AWS_PROFILE"] = "deploy"
        subprocess.run(actions)

    return {"actions": [watch]}
