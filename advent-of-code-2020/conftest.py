"""Configuration for pytest."""
import sys

import pytest

# For some reason pytest does not find base site-packages
sys.path.append("/usr/local/lib/python3.9/site-packages")

# Register custom metaclass for assert rewriting
pytest.register_assert_rewrite("advent.solver")
