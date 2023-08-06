import sys
from typing import Any, Generator

import pytest

import doty


@pytest.fixture(autouse=True)
def add_imports(doctest_namespace: dict[str, Any]) -> None:
    doctest_namespace["doty"] = doty


@pytest.fixture(autouse=True)
def cd_tmpdir(request: Any) -> Generator[None, None, None]:
    tmpdir = request.getfixturevalue("tmpdir")
    sys.path.insert(0, str(tmpdir))
    with tmpdir.as_cwd():
        yield
