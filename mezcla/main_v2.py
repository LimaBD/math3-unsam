#

"""
main v2 example
"""

class BaseArgument:
    """Argument base class"""

    def __init__(self, name, shortname, description, default):
        self.name = name
        self.shortname = shortname
        self.description = description
        self.default = default
        self.value = None

    def parse(self):
        """Extract argument from command-line"""
        raise NotImplementedError("must be implemented")

class IntArgument(BaseArgument):
    """Int argument class"""

    def parse(self):
        """Extract argument from command-line"""
        self.value = 1213 # as example

class BooleanArgument(BaseArgument):
    """Boolean argument class"""

    def parse(self):
        """Extract argument from command-line"""
        self.value = True # as example

class StringArgument(BaseArgument):
    """String argument class"""

    def parse(self):
        """Extract argument from command-line"""
        self.value = "tmp" # as example

class Arguments:
    """Argument parser class"""

    def __init__(self, **input_args):
        self.input_args = input_args

    def parse(self):
        """Parse arguments from command-line"""
        for name, value in self.input_args.items():
            assert isinstance(value, BaseArgument)
            value.parse()
            setattr(self, name, value.value)

class MainV2:
    """Main version 2 script class"""

    def __init__(
            self,
            input_arguments,
            on_startup=None,
            on_all_files=None,
            on_every_file=None,
            on_every_line=None,
            on_finish=None,
            on_every_paragraph=None,
        ):
        # ...
        self.input_arguments = input_arguments
        self.on_startup = on_startup
        self.on_all_files = on_all_files
        self.on_every_file = on_every_file
        self.on_every_line = on_every_line
        self.on_finish = on_finish
        self.on_every_paragraph = on_every_paragraph
        # ...

    def run(self):
        """Run the script"""
        self.input_arguments.parse()
        # ...
        if self.on_every_file is not None:
            self.on_every_file(self.input_arguments, "file.txt")
        # ...
