# Bundled
import os

import platform
import sys
import argparse


# Local files
import confirm_command

#must import this file so that classes have the same namespace as projects that extend it 
import manage_project

global INDENTATION_LEVEL
INDENTATION_LEVEL = 0

global TABS_PER_INDENT
TABS_PER_INDENT = 4


###############################
#  Some misc print functions  #
###############################


def get_indent(text_str):
    """
    Prints a formatted message to the console
        -indented properly
    """
    return "{1}{0}".format(text_str, " "*(INDENTATION_LEVEL*TABS_PER_INDENT))


def print_indent_title(title_str):
    """
    Prints a formatted title to the console
        -indented properly
        -surrounded with asterics
    """
    print("{1}\n{0}\n{1}".format(
        get_indent("*  {}  *".format(title_str)),
        get_indent("*"*(len(title_str)+6)),
    ))

###############################
#  Other misc functions  #
###############################


def create_folder_structure(proj_path, *paths):
    """
    Creates a folder structure fiven by paths
    """
    import pathlib
    for d in paths:
        pathlib.Path(d).mkdir(parents=True, exist_ok=True)

    if "source" not in os.listdir(proj_path):
        raise Exception("project source folder could not be created")


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
        create_folder_structure(
            self.proj_path,
            *(
                self.proj_path,
                self.source_path,
            )
        )

        # Creates the set of project extentions currently loaded
        self.project_extentions = set()


class ProjectExtention(manage_project.BaseProject):
    """
    This is an abstract class for all project extentions.

    To create an extention, call the _create method to verfiy the
    """

    def __init__(self, name: str, proj_path: str):

        super().__init__(name, proj_path)

        '''
        print("****")
        # print base class names
        for base in self.__class__.__bases__:
            print("base: {}".format(base.__name__))
        '''

    def _create(self):
        """
        An abstract method for actions to:
            create a new project extention of this type
        """
        raise NotImplementedError

    def _load(self):
        """
        An abstract method for actions to:
            load attributes from an existing project extention
        """
        raise NotImplementedError

    def _check_for_existing(self):
        """
        An abstract method for actions to:
            check if a project of this type has already been created
        """
        raise NotImplementedError

    def _on_existing_create_new(self):
        """
        An abstract method for actions to:
            handle a project of this type already existing
        """
        raise NotImplementedError

    def create(self, extention_class):
        """
        A method responsable for creating subclasses
        """

        if issubclass(extention_class, manage_project.ProjectExtention):

            if not extention_class._check_for_existing(self):

                print(get_indent("creating subproject: {}".format(extention_class)))
                extention_class._create(self)
                self.project_extentions.add(extention_class.__name__)

            else:
                
                #Try to load attributes from the extention
                try:
                    extention_class._load(self)

                #If attributes could not be loaded
                except NotImplementedError as e:
                    print(get_indent("_load was not implemented. This should not be the case."))
                    raise e

                #If other exception was caught, give option to overwrite the extention
                except Exception as e:
                    if extention_class._on_existing_create_new(self):
                        print(get_indent(
                            "Permission granted from subproject to create over existing: {}".format(extention_class)))
                        extention_class._create(self)
                        self.project_extentions.add(extention_class.__name__)

                    else:
                        print(get_indent(
                            "Permission denied from subproject to create over existing: {}".format(extention_class)))
                        raise e

        else:
            raise Exception("Extention must extend ProjectExtention")


# Extention files
from project_extentions.git_project import GitProject
from project_extentions.pipenv_project import PipenvProject
from project_extentions.vscode_workspace_project import VSCodeWorkspaceProject


class Project(PipenvProject, VSCodeWorkspaceProject, GitProject):
    """
    Project with all project extentions applied
    """

    def __init__(self, name: str, proj_path: str, **kwargs):

        super().__init__(name, proj_path)

        # Map the flags to the creation methods
        project_creation_flags = {
            "git_proj":  GitProject,
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
                    # print(get_indent("{} is not being created".format(subproject.__name__))

            # If the flag is not a valid project type
            except KeyError:
                print(get_indent("Invalid project flag: {}".format(flag)))

        INDENTATION_LEVEL -= 1

        print_indent_title("Listing projects created")
        print(get_indent("\n".join(self.project_extentions)))



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
