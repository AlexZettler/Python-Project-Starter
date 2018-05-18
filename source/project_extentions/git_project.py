from manage_project import ProjectExtention, UnopenableProject
from manage_project import print_indent_title, get_indent, INDENTATION_LEVEL, TABS_PER_INDENT

import os
import git
import os.path as osp
import subprocess
import sys

class GitProject(ProjectExtention):
    """
    This extention creates a git project and adds some essential files

    Basic tutorial follows:
    https://gitpython.readthedocs.io/en/stable/tutorial.html#the-commit-object
    """

    def __init__(self, name: str, proj_path: str,):
        super().__init__(name, proj_path)

    def _create(self):

        # Get a list of files to add to the repo by default
        files = ["__init__.py"]
        files = [osp.join(self.proj_path, "source", fn) for fn in files]

        # Initialize the repo
        self.repo = git.Repo.init(self.proj_path)

        # Creates empty files
        for file_name in files:
            open(file_name, 'wb').close()

        # adds the files to the repo
        self.repo.index.add(files)

        # make first commit to the repo
        self.repo.index.commit("initial commit")

    def _load(self):
        self.repo = git.Repo(self.proj_path)

    def _open(self):

        
        try:

            p = subprocess.Popen(["/usr/share/gitkraken/gitkraken", "-p" , self.proj_path, ">/dev/null", "&"])
            #os.system(" ".join())


        except KeyError as e:
            print("{} does not have a run command mapped".format(sys.platform))
            raise e

        raise UnopenableProject

    def _check_for_existing(self):
        """
        Checks for existing git repository in specified directory
        """

        try:
            git.Repo(self.proj_path)
            return True

        except git.InvalidGitRepositoryError:
            return False

    def _on_existing_create_new(self):
        return False
