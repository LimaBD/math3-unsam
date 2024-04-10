#

"""
Standards Translate Example
"""

from mezcla import standards_translate #  this is like six
from mezcla.standards_translate import glue_helpers

if __name__ == "__main__":

    ## NOTE: this is not working yet
    ## standards_translate.use_mezcla_api()
    standards_translate.use_standard_api()

    # Print the module name, good to see
    # if is being used Mezcla or posixpath
    print(glue_helpers.form_path.__module__)

    # Print a usage example
    example = glue_helpers.form_path("tmp", "file.txt")
    print(f"Running example: {example}")
