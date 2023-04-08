#!/usr/bin/env python
#
# Utils for analysis
#

"""
Utils for analysis
"""

# Standard packages
## NOTE: Nothing for now

# Installed packages
## NOTE: Nothing for now

# Local packages
## NOTE: Nothing for now

class Diff:
    """Calculate difference between two stages?"""

    def __init__(self) -> None:
        self.starting = None

    def start(self, value: float|int) -> None:
        """Set starting value"""
        self.starting = value

    def stop(self, value: float|int) -> float:
        """Calculate absolute difference between starting and
           stopping value, calculate percent difference"""
        if self.starting is None:
            raise ValueError('Starting value is not set.')
        diff = value - self.starting
        perc = percent(self.starting, diff)
        return abs(diff), perc

def percent(total: float|int, part: float|int) -> float:
    """Calculate percent of part to total"""
    return round((part / total) * 100, 3)

def acre_to_sqft(acre: float|int) -> float:
    """Convert acre to square feet"""
    return acre * 43560

if __name__ == '__main__':
    print('This is a module, not a script.')
