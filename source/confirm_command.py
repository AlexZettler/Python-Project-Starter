
VALID_TRUE = ["yes", "y", "true", "t"]
VALID_FALSE = ["no", "n", "false", "f"]


def execute_command_after_verification(message: str, completed_message: str, incomplete_message: str, command, *args, **kwargs):
    valid_resp = False

    while not valid_resp:

        resp = input(message).lower()

        if resp in VALID_TRUE:
            valid_resp = True
            command(args, kwargs)
            print(completed_message)

        elif resp in VALID_FALSE:
            valid_resp = True
            print(incomplete_message)
        else:
            print("""unknown command, please try again.
				Valid True commands are: {}

				Valid Flase commands are: {}""".format(
                ", ".join(VALID_TRUE),
                ", ".join(VALID_FALSE)
            )
            )
