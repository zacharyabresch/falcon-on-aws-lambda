import os
import shutil
import subprocess

from zipfile import ZipFile

DIST_DIR = "dist"
BUILD_DIR = os.path.join(DIST_DIR, "build")


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
