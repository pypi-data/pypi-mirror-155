#!/usr/bin/env python
#
# Copyright (C) 2022 Leah Lackner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from typing import Any, Generator

import pytest

import parsealot as _parsealot


@pytest.fixture(autouse=True)
def add_imports(doctest_namespace: dict[str, Any]) -> None:
    doctest_namespace["parsealot"] = _parsealot


@pytest.fixture()
def parsealot() -> Any:
    return _parsealot


@pytest.fixture(autouse=True)
def cd_tmpdir(request: Any) -> Generator[None, None, None]:
    tmpdir = request.getfixturevalue("tmpdir")
    sys.path.insert(0, str(tmpdir))
    with tmpdir.as_cwd():
        yield
