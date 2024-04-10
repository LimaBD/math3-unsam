#

"""
Translation six-like from Mezcla wrappers to standard API and vice versa
"""

import sys
import os
import shutil
import io
from mezcla import (
    glue_helpers as mezcla_gh,
    system as mezcla_system,
)

API = "standard" # or "standard"

def set_api(api):
    """set the API to use"""
    assert api in ["mezcla", "standard"], "API must be 'wrappers' or 'standard'"
    global API
    API = api

def use_standard_api():
    """Use the standard API"""
    set_api("standard")

def use_mezcla_api():
    """Use the mezcla API"""
    set_api("mezcla")

class ModuleItem:
    """Module class"""

    def __init__(self, wrapper, standard):
        self.name = wrapper.__name__
        self.wrapper = wrapper
        self.standard = standard

    @property
    def attr(self):
        """Return the attribute"""
        if API == "mezcla":
            return self.wrapper
        elif API == "standard":
            return self.standard

class ModuleTranslation:
    """System class"""

    def __init__(self):
        # Load this module
        thismodule = sys.modules[__name__]
        setattr(thismodule, self.__class__.__name__.lower(), self)
        # Attributes
        self.items = []

    def append(self, wrapper, standard):
        """Append a translation from wrapper to standard"""
        self.items.append(ModuleItem(wrapper, standard))

    def load(self):
        """Load the module"""
        for item in self.items:
            setattr(self, item.name, item.attr)

# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
class System(ModuleTranslation):
    """system module class"""

# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
class GlueHelpers(ModuleTranslation):
    """Glue helpers module class"""

system = System()
system.append(mezcla_system.open_file, io.open)
system.append(mezcla_system.getenv, os.getenv)
system.append(mezcla_system.read_directory, os.listdir)
system.load()
glue_helpers = GlueHelpers()
glue_helpers.append(mezcla_gh.form_path, os.path.join)
glue_helpers.append(mezcla_gh.copy_file, shutil.copy)
glue_helpers.load()
