from manage_project import ProjectExtention
from manage_project import print_indent_title, get_indent, INDENTATION_LEVEL, TABS_PER_INDENT

import confirm_command

import subprocess
import os
import platform


class PipenvProject(ProjectExtention):

    # The requirements file located in the project root
    REQUIREMENTS_FILE = "requirements.txt"

    def __init__(self, name: str,
                 proj_path: str):
        super().__init__(name, proj_path)

        # title_text("Creating pip enviroment")
        # self.create_pip_env()
        # self.python_path = self.get_pipenv_python_path()

    def _create(self):
        """
        Create a pipenv enviroment in the given directory

        :param proj_path:str:
            The path to the project source folder
        """

        # Change directory
        os.chdir(self.source_path)

        # create the working pipenv
        subprocess.run(["pipenv", "--python", "3.6"], stdout=subprocess.PIPE)

        # run platform specific instructions
        if platform.system() == "Windows":
            pass
        elif platform.system() == "Linux":
            pass

    def _check_for_existing(self):
        """
        check if a project of this type has already been created
        """
        os.chdir(self.source_path)
        return "Pipfile" in os.listdir()

    def _on_existing_create_new(self):
        """
        handle a project of this type already existing
        """

        # check if a requirements file exists
        os.chdir(self.proj_path)
        if self.REQUIREMENTS_FILE in os.listdir():
            print("requirements file found!")
            if confirm_command.give_permission_after_verification(
                "Found {} in your project folder, would you like to recreate your pipenv?".format(
                    self.REQUIREMENTS_FILE),
                "reinstalling pipenv",
                    "passing"):
                return True

        elif confirm_command.give_permission_after_verification(
            "Could not find a {} in your project folder! Would you like to recreate your pipenv?".format(
                self.REQUIREMENTS_FILE),
            "reinstalling pipenv",
                "passing"):
            return True

        else:
            return False

    def get_pipenv_python_path(self):
        """
        Returns the path to the python executable
            :param self:
        """

        # cd into source directory
        os.chdir(self.source_path)
        result = subprocess.run(["pipenv", "--py"], stdout=subprocess.PIPE)

        # formats the path correctly
        python_path = result.stdout.decode("utf-8").replace("\n", "")
        return python_path

    def install_requirements(self):
        """
        Installs the requirements from the requirements file if it exists

        :param proj_path:str:
            The path to the project folder
        """

        os.chdir(self.proj_path)
        if self.REQUIREMENTS_FILE in os.listdir():

            # go to the source folder and install pipenv requirements
            os.chdir(self.source_path)
            subprocess.run(
                ["pipenv", "install", "-r", self.REQUIREMENTS_FILE],
                stdout=subprocess.PIPE)
        else:
            print("No requirements found")
