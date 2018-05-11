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

global INDENTATION_LEVEL
INDENTATION_LEVEL = 0

global TABS_PER_INDENT
TABS_PER_INDENT = 4


class BaseProject(object):
    """
    The base class that ProjectExtention classes inherit from

    This sets the:
        project name,
        directory,
        source path

    And creates the folder structure for the project 
    """

    def __init__(self,
                 name: str,
                 proj_path: str):

        self.name = name
        self.proj_path = proj_path

        self.source_path = "{}/{}".format(proj_path, "source")
        # print(self.source_path)

        # create folder structure
        workspace_maker.create_folder_structure(
            self.proj_path,
            *(
                base_path,
                self.proj_path,
                self.source_path
            )
        )

        # Creates the set of project extentions currently loaded
        self.project_extentions = set()


class ProjectExtention(BaseProject):
    """
    This is an abstract class for all project extentions.

    To create an extention, call the _create method to verfiy the
    """

    def __init__(self,
                 name: str,
                 proj_path: str):

        super().__init__(name, proj_path)

        '''
        print("****")
        # print base class names
        for base in self.__class__.__bases__:
            print("base: {}".format(base.__name__))
        '''

    def _create(self):
        raise NotImplementedError

    def create(self, extention_class):
        
        '''print("""
        extention type is: {}
        self type is: {}

        """.format(
            extention_class,
            self.__class__
        ))'''

        if issubclass(extention_class, ProjectExtention):

            print_indented(
                "creating subproject: {}".format(extention_class))

            extention_class._create(self)
            self.project_extentions.add(extention_class.__name__)

        else:
            raise Exception("Extention must extend ProjectExtention")

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

    def _create(self):
        if self.check_for_workspace():
            confirm_command.execute_command_after_verification(
                """{0}I would hate to overwrite your vs code workspace,\n{0}are you sure you want to create a new one?""".format(
                    " "*INDENTATION_LEVEL*TABS_PER_INDENT),
                "{}vs code workspace was created".format(
                    " "*INDENTATION_LEVEL*TABS_PER_INDENT),
                "{}vs code workspace was not created".format(
                    " "*INDENTATION_LEVEL*TABS_PER_INDENT),
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
        workspace_maker.create_workspace(proj_path, self.name)


class GitProject(ProjectExtention):

    def __init__(self, name: str, proj_path: str,):
        super().__init__(name, proj_path)

    def _create(self):
        print("One day I will be able to create your glorious git repo")
        git.create_git_repo(proj_path)


class Project(PipenvProject, VSCodeWorkspaceProject, GitProject):
    """
    Project with all project extentions applied
    """

    def __init__(self, name: str, proj_path: str, **kwargs):

        super().__init__(name, proj_path)

        # Map the flags to the creation methods
        project_creation_flags = {
            "git_proj": GitProject,
            "pip_env_proj": PipenvProject,
            "vs_code_workspace": VSCodeWorkspaceProject
        }

        # Print statement anouncing creation of subprojects
        print_indent_title("Now creating Project Extentions")

        # Reference our global indentation
        global INDENTATION_LEVEL
        INDENTATION_LEVEL += 1

        # iterate through flags passed and create the subprojects if so
        for flag, subproject in project_creation_flags.items():

            # Test to see if the flag was passed into the constructor
            try:

                # Test to see if the project type passed into the constructer was a valid type
                if kwargs[flag] == True:
                    print_indent_title("{} project being created!".format(
                        subproject.__name__))

                    # indent and additional information during creation of subproject
                    INDENTATION_LEVEL += 1
                    ProjectExtention.create(self, subproject)
                    INDENTATION_LEVEL -= 1

                else:
                    pass
                    #print_indented("{} is not being created".format(subproject.__name__))

            # If the flag is not a valid project type
            except KeyError:
                print_indented("Invalid project flag: {}".format(flag))

        INDENTATION_LEVEL -= 1

        print_indent_title("Listing projects created")
        print_indented("\n".join(self.project_extentions))

###############################
#  Some misc print functions  #
###############################


def print_indented(text_str):
    """
    Prints a formatted message to the console
        -indented properly
    """
    print("{1}{0}".format(text_str, " "*(INDENTATION_LEVEL*TABS_PER_INDENT)))


def print_indent_title(title_str):
    """
    Prints a formatted title to the console
        -indented properly
        -surrounded with asterics
    """
    print("{2}{1}\n{2}{0}\n{2}{1}".format(
        "*  {}  *".format(title_str),
        "*"*(len(title_str)+6),
        " "*(INDENTATION_LEVEL*TABS_PER_INDENT)
    ))



#################################
#  Lets get this show started!  #
#################################
if __name__ == "__main__":
    print_indent_title("Arguements Parsing Details")

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
    # print(manager_directory)

    # full path of the main managed projects directory
    base_path = "{}/managed_projects".format(
        os.path.dirname(manager_directory))
    # print(base_path)

    # full path to the directory containing the project
    proj_path = "{}/{}".format(base_path, args.name)
    # print(proj_path)

    #######################
    #  Create our object  #
    #######################
    working_project = Project(
        name=args.name,
        proj_path=proj_path,
        # kwargs
        pip_env_proj=args.pipenv,
        git_proj=args.git,
        vs_code_workspace=args.vscws
    )
