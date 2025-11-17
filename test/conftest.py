"""Shared pytest fixtures for all test modules"""

import pytest


@pytest.fixture
def valid_notebook_data():
    """Returns valid test notebook json with sequential execution counts."""
    return {
        "cells": [
            {"cell_type": "code", "execution_count": 1, "source": ["print('foo')"]},
            {"cell_type": "code", "execution_count": 2, "source": ["print('foo')"]},
            {"cell_type": "code", "execution_count": 3, "source": ["print('foo')"]},
        ]
    }


@pytest.fixture
def out_of_order_notebook_data():
    """Returns notebook data with out-of-order execution counts."""
    return {
        "cells": [
            {"cell_type": "code", "execution_count": 1, "source": ["print('foo')"]},
            {"cell_type": "code", "execution_count": 3, "source": ["print('foo')"]},
            {"cell_type": "code", "execution_count": 2, "source": ["print('foo')"]},
        ]
    }


@pytest.fixture
def notebook_cell_not_run_data():
    """Returns notebook data with an unexecuted code cell."""
    return {
        "cells": [
            {"cell_type": "code", "execution_count": 1, "source": ["print('foo')"]},
            {"cell_type": "code", "execution_count": 2, "source": ["print('foo')"]},
            {"cell_type": "code", "execution_count": None, "source": ["print('foo')"]},
        ]
    }


@pytest.fixture
def empty_notebook_cells():
    """Returns notebook data with empty code cells."""
    return {
        "cells": [
            {"cell_type": "code", "execution_count": 1, "source": []},
            {"cell_type": "code", "execution_count": None, "source": []},
            {"cell_type": "code", "execution_count": None, "source": []},
        ]
    }


@pytest.fixture
def notebook_data_with_mixed_cells():
    """Returns notebook data with code and markdown cells."""
    return {
        "cells": [
            {"cell_type": "markdown", "source": ["# Title"]},
            {"cell_type": "code", "execution_count": 1, "source": ["print('cell 1')"]},
            {"cell_type": "markdown", "source": ["Some text"]},
            {"cell_type": "code", "execution_count": 2, "source": ["print('cell 2')"]},
            {"cell_type": "code", "execution_count": 3, "source": ["print('cell 3')"]},
        ]
    }


@pytest.fixture
def notebook_data_only_code_cells():
    """Returns notebook data with only code cells."""
    return {
        "cells": [
            {"cell_type": "code", "execution_count": 1, "source": ["x = 1"]},
            {"cell_type": "code", "execution_count": 2, "source": ["y = 2"]},
        ]
    }


@pytest.fixture
def notebook_data_no_code_cells():
    """Returns notebook data with no code cells (only markdown/raw)."""
    return {
        "cells": [
            {"cell_type": "markdown", "source": ["# Title"]},
            {"cell_type": "markdown", "source": ["Some text"]},
            {"cell_type": "raw", "source": ["Raw cell"]},
        ]
    }


@pytest.fixture
def notebook_data_empty():
    """Returns notebook data with no cells at all."""
    return {"cells": []}
