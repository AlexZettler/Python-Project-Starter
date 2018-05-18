#global INDENTATION_LEVEL, TABS_PER_INDENT

from manage_project import ProjectExtention, UnopenableProject, UnloadableProject
from manage_project import print_indent_title, get_indent, INDENTATION_LEVEL, TABS_PER_INDENT

import confirm_command
import json
import os.path as osp
import subprocess
import sys

class VSCodeWorkspaceProject(ProjectExtention):
    def __init__(self, name: str, proj_path: str,):
        super().__init__(name, proj_path)

    def _create(self):
        self.make_vs_code_workspace()

    def _load(self):
        """
        This method does not need to load anything about the workspace to this class currently
        however in the future, could verify that the json was able to be parsed corrrectly
        """
        pass

    def _open(self):
        """
        run vscode workspace using default application to open the program
        """


        try:
            subprocess.call([self.run_cmd_map[sys.platform], self.get_workspace_path()])
        except KeyError as e:
            print("{} does not have a run command mapped".format(sys.platform))
            raise e

    def _check_for_existing(self):

        print(get_indent("Checking for existing file"))
        try:
            with open(self.get_workspace_path(), "r") as f:
                print(get_indent("File read correctly"))
                return True

        except FileNotFoundError:
            return False

    def _on_existing_create_new(self):
        return True

    def make_vs_code_workspace(self, *args, **kwargs):
        self.create_workspace()

    def get_workspace_name(self):
        """
        returns the name of the workspace file to create
        """
        return "{}.code-workspace".format(self.name)

    def get_workspace_path(self):
        """
        returns the path and name of the workspace file to create
        """
        return osp.join(self.proj_path, self.get_workspace_name())

    def make_workspace_dict(self):
        """
        returns the populated vscode dictionary to write
        """
        vs_code_dict = {
            "folders": [{
                "path": "source"
            }],
            "settings": {
                # vs code by default looks for pipenv so this is irrelevent
                # "python.pythonPath": python_path
            }
        }
        return vs_code_dict

    def create_workspace(self):

        # Make the workspace dictionary
        vs_code_dict = self.make_workspace_dict()

        # Create the json file to write
        json_code_str = json.dumps(
            vs_code_dict, sort_keys=True, indent=2, separators=(',', ': '))

        # Create the path including the file name
        file_path_and_name = self.get_workspace_path()

        # Write json data
        with open(file_path_and_name, "w") as f:
            f.write(json_code_str)
