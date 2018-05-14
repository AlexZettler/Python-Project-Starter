from manage_project import ProjectExtention
from manage_project import print_indent_title, get_indent, INDENTATION_LEVEL, TABS_PER_INDENT

VALID_TRUE = ["yes", "y", "true", "t"]
VALID_FALSE = ["no", "n", "false", "f"]


def give_permission_after_verification(
        message: str,
        completed_message: str,
        incomplete_message: str, *args, **kwargs):
    """
    Returns a boolean representing if the command was accepted
    """

    while True:

        resp = input(get_indent(message)).lower()

        if resp in VALID_TRUE:
            print(completed_message)
            return True

        elif resp in VALID_FALSE:
            print(incomplete_message)
            return False
        else:
            print("""unknown command, please try again.
				Valid True commands are: {}

				Valid Flase commands are: {}""".format(
                ", ".join(VALID_TRUE),
                ", ".join(VALID_FALSE)
            )
            )
