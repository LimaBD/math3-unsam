#!/usr/bin/env python3
#
# Tests for properties_scraping script
#

"""Tests for properties_scraping script"""

# Standard packages
## NOTE: this is empty for now

# Installed packages
import pytest

# Local packages
from PDP.properties_scraping import Map

class TestPropertiesScrapingScript:
    """Class for testcase definition"""

    def test_map_segments(self):
        """Test map segmentation"""
        test_map = Map(100, 0, 200, 50)
        test_map.set_segment_size(10)
        segment = test_map.get_next_segment()
        assert segment.west == 100
        assert segment.east == 110
        assert segment.south == 0
        assert segment.north == 10
        segment = test_map.get_next_segment()
        assert segment.west == 110
        assert segment.east == 120
        assert segment.south == 0
        assert segment.north == 10
        for _ in range(1, 8):
            _ = test_map.get_next_segment()
        segment = test_map.get_next_segment()
        assert segment.west == 190
        assert segment.east == 200
        assert segment.south == 0
        assert segment.north == 10
        segment = test_map.get_next_segment()
        assert segment.west == 100
        assert segment.east == 110
        assert segment.south == 10
        assert segment.north == 20


if __name__ == '__main__':
    pytest.main([__file__])
