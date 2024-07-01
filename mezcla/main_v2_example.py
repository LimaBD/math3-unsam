#

"""
main v2 example
"""

from main_v2 import (
    IntArgument, BooleanArgument,
    StringArgument, Arguments, MainV2,
)

def run_on_startup(state):
    """Run on startup"""
    print("Running on startup")
    return state

def some_example_function(state, file):
    """Run every file"""
    print(f"temp_dir={state.temp_dir} file={file}")

if __name__ == "__main__":

    args = Arguments(
        threshold = IntArgument("threshold", "t", "Amount of tests that should pass", 5),
        temp_dir = StringArgument("temp_dir", "d", "Temporary directory to use for tests", "tmp"),
        version = BooleanArgument("version", "v", "Print software version", False),
        bash_eval = BooleanArgument("bash_eval", "bh", "Evaluate tests with Bash", True),
        bats_eval = BooleanArgument("bats_eval", "bs", "Evaluate tests with Bats", False),
    )

    script = MainV2(
        input_arguments = args,
        on_startup=run_on_startup,
        on_every_file = some_example_function,
    )

    script.run()
