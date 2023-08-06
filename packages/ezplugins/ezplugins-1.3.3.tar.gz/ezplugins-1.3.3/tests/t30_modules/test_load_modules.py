#
# SPDX-License-Identifier: MIT
#
# Copyright (C) 2019-2021, AllWorldIT.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""EZPlugins tests."""

from typing import Dict, List

import ezplugins

from ..base import BaseTest

__all__ = [
    "TestLoadModulesFunctionality",
]


class TestLoadModulesFunctionality(BaseTest):
    """Test basic functionality of EZPlugins."""

    data: Dict[str, ezplugins.EZPluginManager] = {}

    def test_modules_load(self) -> None:
        """Test loading of plugins."""
        self.data["plugins"] = ezplugins.EZPluginManager()

        self.data["plugins"].load_modules(r"^tests($|\.t30_modules($|\.plugins($|\.)))")

        expected_modules = [
            "tests.t30_modules.plugins",
            "tests.t30_modules.plugins.plugin1",
            "tests.t30_modules.plugins.plugin2",
        ]

        received_modules = [x.module_name for x in self.data["plugins"].modules]

        assert received_modules == expected_modules, "All plugins did not get loaded"

    def test_load_blank_modules(self) -> None:
        """Test loading of blank plugin."""
        self.data["plugins"] = ezplugins.EZPluginManager()

        self.data["plugins"].load_modules(r"^tests($|\.t30_modules($|\.plugins_blank($|\.)))")

        expected_modules: List[str] = []

        received_modules = [x.module_name for x in self.data["plugins"].modules]

        assert received_modules == expected_modules, "All plugins did not get loaded"
