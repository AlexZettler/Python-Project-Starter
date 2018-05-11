# Bundled
import os
import subprocess
import platform
import sys
import argparse

# Local files
import confirm_command
import workspace_maker
import git


class BaseProject(object):
    """
    The base class that all subproject classes inherit from
    """

    def __init__(self,
                 name: str,
                 proj_path: str):

        self.name = name
        self.proj_path = proj_path

        self.source_path = "{}/{}".format(proj_path, "source")
        print(self.source_path)

        # create folder structure
        workspace_maker.create_folder_structure(
            self.proj_path,
            *(
                base_path,
                self.proj_path,
                self.source_path
            )
        )
        '''
        print("####")
        for base in self.__class__.__bases__:
            print("base: {}".format(base.__name__))
        '''


class ProjectExtention(BaseProject):
    """
    This is an abstract class for all project extentions.

    To create an extention, call the _create method to verfiy the 
    """
    def __init__(self,
                 name: str,
                 proj_path: str):

        super().__init__(name, proj_path)
        self.project_extentions = set()
        '''
        print("****")
        #print base class names
        for base in self.__class__.__bases__:
            print("base: {}".format(base.__name__))
        '''

    def _create(self, extention_class):
        '''print("""
        extention type is: {}
        self type is: {}

        """.format(
            extention_class,
            self.__class__
        ))'''

        if issubclass(extention_class, ProjectExtention):
            print("creating subproject: {}".format(extention_class))
            extention_class.create(self)
            self.project_extentions.add(extention_class.__name__)

        else:
            raise Exception("Extention must extend ProjectExtention")

    def create(self):
        raise NotImplementedError


class PipenvProject(ProjectExtention):

    # The requirements file located in the project root
    REQUIREMENTS_FILE = "requirements.txt"

    def __init__(self, name: str,
                 proj_path: str):
        super().__init__(name, proj_path)

        #title_text("Creating pip enviroment")
        # self.create_pip_env()
        #self.python_path = self.get_pipenv_python_path()

    def create(self):
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


class VSCodeWorkspaceProject(ProjectExtention):
    def __init__(self,
                 name: str,
                 proj_path: str,):
        super().__init__(name, proj_path)

    def create(self):
        if self.check_for_workspace():
            confirm_command.execute_command_after_verification(
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


class GitProject(ProjectExtention):

    def __init__(self,
                 name: str,
                 proj_path: str,):
        super().__init__(name, proj_path)

    def create(self):
        print("One day I will be able to create your glorious git repo")
        git.create_git_repo(proj_path)


class Project(PipenvProject, VSCodeWorkspaceProject, GitProject):
    """
    Project with all project extentions applied
    """

    def __init__(self,
                 name: str,
                 proj_path: str,
                 pip_env_proj: bool,
                 git_proj: bool,
                 vs_code_workspace: bool):

        super().__init__(name, proj_path)

        # Map the flags to the creation methods
        project_creation_flags = {
            git_proj: GitProject,
            pip_env_proj: PipenvProject,
            vs_code_workspace: VSCodeWorkspaceProject
        }
        print(project_creation_flags)
        #import inspect
        # print(inspect.getfullargspec(self.__init__))
        '''
        title_text("Now creating subprojects", 20)
        # iterate through flags passed and create the subprojects if so
        for flag, subproject in project_creation_flags.items():
            print("{} {}".format("*"*5, "New project being tested"))
            print(flag, subproject)
            if flag:
                ProjectExtention._create(self, subproject)
        '''

###
#  Some misc functions
###


def title_text(string_to_title, title_bar_length=15):
    print("\n{1}\n{0}\n{1}".format(string_to_title, "*"*title_bar_length))



#################################
#  Lets get this show started!  #
#################################
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

    human_readable_is_being_created = {
        True: "being",
        False: "not being"}

    # Print these bad bois
    print("Project name is: {}".format(args.name))
    print("Git is {} created".format(
        human_readable_is_being_created[args.git]))
    print("VS code workspace is {} created".format(
        human_readable_is_being_created[args.vscws]))
    print("Pipenv is {} created".format(
        human_readable_is_being_created[args.pipenv]))

    ###########
    #  Paths  #
    ###########

    # full path of the directory containing and including this file
    manager_directory = os.path.dirname(
        os.path.realpath(__file__))
    print(manager_directory)

    # full path of the main managed projects directory
    base_path = "{}/managed_projects".format(
        os.path.dirname(manager_directory))
    print(base_path)

    # full path to the directory containing the project
    proj_path = "{}/{}".format(base_path, args.name)
    print(proj_path)

    #######################
    #  Create our object  #
    #######################
    working_project = Project(
        name=args.name,
        proj_path=proj_path,
        pip_env_proj=args.pipenv,
        git_proj=args.git,
        vs_code_workspace=args.vscws
    )
