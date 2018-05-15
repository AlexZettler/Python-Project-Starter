from manage_project import ProjectExtention, UnopenableProject
from manage_project import print_indent_title, get_indent, INDENTATION_LEVEL, TABS_PER_INDENT

import os.path as osp

class PycharmProject(ProjectExtention):
    def _create(self):
        self.create_folder_structure(
            osp.join(self.proj_path, ".idea")
        )

    def _load(self):
        pass

    def _open(self):
        raise UnopenableProject()

    def _check_for_existing(self):
        pass

    def _on_existing_create_new(self):
        pass
