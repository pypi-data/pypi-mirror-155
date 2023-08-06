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

from typing import Dict

import pytest

import ezplugins

from ..base import BaseTest

__all__ = [
    "TestPluginCallException",
]


class TestPluginCallException(BaseTest):
    """Test for the case that the plugin package doesn't exist."""

    data: Dict[str, ezplugins.EZPluginManager] = {}

    def test_plugin_load(self) -> None:
        """Test loading of plugins."""
        self.data["plugins"] = ezplugins.EZPluginManager()
        self.data["plugins"].load_package(self.plugin_path("plugins_call_exception"))

        expected_modules = [
            "tests.t20_exceptions.plugins_call_exception.plugin1",
            "tests.t20_exceptions.plugins_call_exception.plugin2",
        ]

        received_modules = [x.module_name for x in self.data["plugins"].modules]

        assert received_modules == expected_modules, "Result from plugin load does not match"

    def test_call_with_exception(self) -> None:
        """Test calling a plugin method that raises an exception."""

        expected_results = [
            (
                "tests.t20_exceptions.plugins_call_exception.plugin1#Plugin1",
                "test_func1",
                "RuntimeError('tests.t20_exceptions.plugins_call_exception.plugin1.tests.t20_exceptions."
                "plugins_call_exception.plugin1')",
            ),
            (
                "tests.t20_exceptions.plugins_call_exception.plugin2#Plugin2",
                "test_func1",
                "tests.t20_exceptions.plugins_call_exception.plugin2.tests.t20_exceptions.plugins_call_exception.plugin2#Plugin2",
            ),
        ]

        received_results = []
        for method, plugin in self.data["plugins"].methods(where_name="test_func1"):
            try:
                result = method.run()
                received_results.append((plugin.fqn, method.name, result))
            except Exception as exception:  # pylint: disable=broad-except
                received_results.append((plugin.fqn, method.name, repr(exception)))

        assert received_results == expected_results, "Results don't match what they should"

    def test_call_no_method(self) -> None:
        """Test calling a method from a plugin that doesn't exist."""

        with pytest.raises(ezplugins.EZPluginMethodNotFoundError) as excinfo:
            # Coerce the results into a list so we iterate
            list(self.data["plugins"].methods(where_name="test_func2"))

        assert ("No EZPlugin method(s) found", None, "test_func2") == (
            str(excinfo.value),
            excinfo.value.plugin_name,
            excinfo.value.method_name,
        ), "Exception raised does not match"

    def test_call_no_plugin(self) -> None:
        """Test calling a method from a specific plugin that doesn't exist."""

        with pytest.raises(ezplugins.EZPluginMethodNotFoundError) as excinfo:
            # Coerce the results into a list so we iterate
            list(self.data["plugins"].methods(where_name="test_func1", from_plugin="#DoesNotExist"))

        assert ("No EZPlugin method(s) found", "#DoesNotExist", "test_func1") == (
            str(excinfo.value),
            excinfo.value.plugin_name,
            excinfo.value.method_name,
        ), "Exception raised does not match"
