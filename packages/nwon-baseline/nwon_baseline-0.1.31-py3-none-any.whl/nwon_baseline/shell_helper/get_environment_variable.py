from os import getenv


class EnvironmentVariableNotSet(Exception):
    message = ""

    def __init__(self, environment_variable: str, *args, **kwargs):

        self.message = "Environment variable " + environment_variable + " is not set."

        if len(args) > 0:
            self.message = str(args.pop(0))

        for key in list(kwargs.keys()):
            setattr(self, key, kwargs.pop(key))

        if not self.message:
            self.message = "{title} ({body})".format(
                title=getattr(self, "reason", "Unknown"),
                body=getattr(self, "error_type", vars(self)),
            )

        super().__init__(self.message, *args, **kwargs)

    def __str__(self):
        return self.message


def get_environment_variable(key: str) -> str:
    """
    Getting environment variable by key. Raises exception when variables is not set.
    """

    environment_variable = getenv(key)

    if environment_variable is None or environment_variable == "":
        raise EnvironmentVariableNotSet(key)

    return environment_variable


__all__ = ["get_environment_variable"]
