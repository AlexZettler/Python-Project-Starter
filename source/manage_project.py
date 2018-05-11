import os
import subprocess
import platform
import sys
import argparse

import confirm_command
import workspace_maker
import git


class BaseProject(object):
    def __init__(self,
                 name: str,
                 proj_path: str
                 ):

        self.name = name
        self.proj_path = proj_path
        self.source_path = "{}/{}".format(proj_path, "source")
        print(self.source_path)

        # create folder structure
        create_folder_structure(
            base_path,
            self.proj_path,
            self.source_path
        )


class PipenvProject(BaseProject):

    REQUIREMENTS_FILE = "requirements.txt"

    def __init__(self):
        super().__init__()

        title_text("Creating pip enviroment")
        self.create_pip_env()
        self.python_path = self.get_pipenv_python_path()

    def create_pip_env(self):
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

    def get_pipenv_python_path(self):
        # Gets the python virtual enviroment path

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


class VSCodeWorkspaceProject(BaseProject):
    def __init__(self):
        super().__init__()
        if self.check_for_workspace():
            confirm_command.execute_command_arter_verification(
                "I would hate to overwrite your vs code workspace, are you sure you want to create a new one?",
                "vs code workspace was created",
                "vs code workspace was not created",
                self.make_vs_code_workspace
            )
        else:
            self.make_vs_code_workspace()

    def check_for_workspace(self):

        try:
            with open(workspace_maker.get_workspace_path(self.proj_path, self.name), "r") as f:
                return True

        except FileNotFoundError:
            return False

    def make_vs_code_workspace(self, *args, **kwargs):

        title_text("Creating workspace")
        workspace_maker.create_workspace(proj_path, self.name)


class GitProject(BaseProject):

    def __init__(self):
        super().__init__()
        print("One day I will be able to create your glorious git repo")
        git.create_git_repo(proj_path)


class Project(PipenvProject, VSCodeWorkspaceProject, GitProject):

    def __init__(self,
                 name: str,
                 proj_path: str,
                 pip_env_proj: bool,
                 git_proj: bool,
                 vs_code_workspace: bool):

        if pip_env_proj:
            super(PipenvProject).__init__()

        if vs_code_workspace:
            super(VSCodeWorkspaceProject, self).__init__()

        if git_proj:
            super(GitProject, self).__init__()


###
#  Some misc functions
###

def create_folder_structure(*paths):

    for d in (paths):
        try:
            os.mkdir(d)
        except FileExistsError:
            pass

    if "source" not in os.listdir(proj_path):
        raise Exception("project folder could not be created")


def title_text(string_to_title, title_bar_length=15):
    print("\n{1}\n{0}\n{1}".format(string_to_title, "*"*title_bar_length))


if __name__ == "__main__":

    title_text("Arguements Parsing Details")

    ############
    #  Parser  #
    ############
    parser = argparse.ArgumentParser(
        description='Optional app description'
    )

    # Required positional argument
    parser.add_argument(
        'name',
        type=str,
        help='A required string for the project name')

    # Switch for git initialization
    parser.add_argument('--pipenv', action='store_true',
                        help='Add to create a pipenv enviroment in the source folder')

    # Switch for git initialization
    parser.add_argument('--vscws', action='store_true',
                        help='Add to initialize a vs code workspace')

    # Switch for git initialization
    parser.add_argument('--git', action='store_true',
                        help='Add to initialize a git repository')

    # Parse the args
    args = parser.parse_args()

    # Print these bad bois
    print("Project name is: {}".format(args.name))
    print("Git is {} created".format(
        {True: "being", False: "not being"}[args.git]))
    print("VS code workspace is {} created".format(
        {True: "being", False: "not being"}[args.vscws]))
    print("Pipenv is {} created".format(
        {True: "being", False: "not being"}[args.pipenv]))

    ###########
    #  Paths  #
    ###########

    # full path of the directory containing
    manager_directory = os.path.dirname(
        os.path.realpath(__file__))
    print(manager_directory)

    base_path = "{}/managed_projects".format(
        os.path.dirname(manager_directory))
    print(base_path)

    proj_path = "{}/{}".format(base_path, args.name)
    print(proj_path)

    #######################
    #  Create our object  #
    #######################

    working_project = BaseProject(
        name=args.name,
        proj_path=proj_path,
        pip_env_proj=args.pipenv,
        git_proj=args.git,
        vs_code_workspace=args.vscws
    )
