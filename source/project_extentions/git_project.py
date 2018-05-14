from manage_project import ProjectExtention, UnopenableProject
from manage_project import print_indent_title, get_indent, INDENTATION_LEVEL, TABS_PER_INDENT

import os


class GitProject(ProjectExtention):

    def __init__(self, name: str, proj_path: str,):
        super().__init__(name, proj_path)

    def _create(self):
        print("One day I will be able to create your glorious git repo")
        # git.create_git_repo(proj_path)
        raise NotImplementedError

    def _load(self):
        pass

    def _open(self):
        raise UnopenableProject

    def _check_for_existing(self):
        """
        checks for existing .git repository in specified directory
        """
        os.chdir(self.proj_path)

        #return True in [f for f in os.listdir() if os.path.isdir(f) and f == ".git"]

        for f in os.listdir():
            if os.path.isdir(f):
                if f == ".git":
                    return True
        return False


    def _on_existing_create_new(self):
        return False
