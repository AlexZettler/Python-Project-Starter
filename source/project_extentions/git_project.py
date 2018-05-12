from manage_project import ProjectExtention
from manage_project import print_indent_title, get_indent, INDENTATION_LEVEL, TABS_PER_INDENT

import os

class GitProject(ProjectExtention):
	
    def __init__(self, name: str, proj_path: str,):
        super().__init__(name, proj_path)

    def _create(self):
        print("One day I will be able to create your glorious git repo")
        #git.create_git_repo(proj_path)

    def _check_for_existing(self):
        """
        checks for existing .git repository in specified directory
        """
        os.chdir(self.proj_path)

        for f in os.listdir():
            if os.path.isdir(f):
                print(f)
        return True