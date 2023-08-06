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

import ezplugins

from ..base import BaseTest

__all__ = [
    "TestPackageBasicFunctionality",
]


class TestPackageBasicFunctionality(BaseTest):
    """Test basic functionality of EZPlugins."""

    data: Dict[str, ezplugins.EZPluginManager] = {}

    def test_package_load(self) -> None:
        """Test loading of plugins."""
        self.data["plugins"] = ezplugins.EZPluginManager()
        self.data["plugins"].load_package(self.plugin_path("plugins"))

        expected_modules = [
            "tests.t10_basic.plugins.plugin1",
            "tests.t10_basic.plugins.plugin2",
            "tests.t10_basic.plugins.plugin3_plus_4",
            "tests.t10_basic.plugins.plugin5_alias",
            "tests.t10_basic.plugins.plugin6a_alias",
            "tests.t10_basic.plugins.plugin6b_alias",
            "tests.t10_basic.plugins.plugin6c_no_alias",
            "tests.t10_basic.plugins.plugin7_method_order",
            "tests.t10_basic.plugins.plugin8_call_parameters",
            "tests.t10_basic.plugins.subplugin.subplugin1",
            "tests.t10_basic.plugins.subplugin_init",
            "tests.t10_basic.plugins.subsubplugin.thesubsubplugin.subsubplugin1",
        ]

        received_modules = [x.module_name for x in self.data["plugins"].modules]

        assert received_modules == expected_modules, "All plugins did not get loaded"

    def test_get_single_plugin_from_single_plugin_file(self) -> None:
        """Test getting a single plugin."""

        expected_plugins = ["tests.t10_basic.plugins.plugin1#Plugin1"]

        received_plugins = [x.fqn for x in self.data["plugins"].get_plugin("tests.t10_basic.plugins.plugin1#Plugin1")]

        assert received_plugins == expected_plugins, "We did not get the plugins we should of gotten back"

    def test_get_single_plugin_from_multi_plugin_file(self) -> None:
        """Test getting a single plugin from a multi-plugin file."""

        expected_plugins = ["tests.t10_basic.plugins.plugin3_plus_4#Plugin3"]

        received_plugins = [x.fqn for x in self.data["plugins"].get_plugin("tests.t10_basic.plugins.plugin3_plus_4#Plugin3")]

        assert received_plugins == expected_plugins, "We did not get the plugins we should of gotten back"

    def test_call_all(self) -> None:
        """Test calling a plugin method from all plugins."""

        expected_results = [
            (
                "tests.t10_basic.plugins.plugin7_method_order#Plugin7b",
                "test_func1",
                "atests.t10_basic.plugins.plugin7_method_order.tests.t10_basic.plugins.plugin7_method_order#Plugin7b",
            ),
            (
                "tests.t10_basic.plugins.plugin1#Plugin1",
                "test_func1",
                "tests.t10_basic.plugins.plugin1.tests.t10_basic.plugins.plugin1#Plugin1",
            ),
            (
                "tests.t10_basic.plugins.plugin2#Plugin2",
                "test_func1",
                "tests.t10_basic.plugins.plugin2.tests.t10_basic.plugins.plugin2#Plugin2",
            ),
            (
                "tests.t10_basic.plugins.plugin3_plus_4#Plugin3",
                "test_func1",
                "tests.t10_basic.plugins.plugin3_plus_4.tests.t10_basic.plugins.plugin3_plus_4#Plugin3",
            ),
            (
                "tests.t10_basic.plugins.plugin3_plus_4#Plugin4",
                "test_func1",
                "tests.t10_basic.plugins.plugin3_plus_4.tests.t10_basic.plugins.plugin3_plus_4#Plugin4",
            ),
            (
                "tests.t10_basic.plugins.plugin5_alias#Plugin5",
                "test_func1",
                "tests.t10_basic.plugins.plugin5_alias.tests.t10_basic.plugins.plugin5_alias#Plugin5",
            ),
            (
                "tests.t10_basic.plugins.plugin6a_alias#Plugin6a",
                "test_func1",
                "tests.t10_basic.plugins.plugin6a_alias.tests.t10_basic.plugins.plugin6a_alias#Plugin6a",
            ),
            (
                "tests.t10_basic.plugins.plugin6b_alias#Plugin6b",
                "test_func1",
                "tests.t10_basic.plugins.plugin6b_alias.tests.t10_basic.plugins.plugin6b_alias#Plugin6b",
            ),
            (
                "tests.t10_basic.plugins.plugin6c_no_alias#Plugin6c",
                "test_func1",
                "tests.t10_basic.plugins.plugin6c_no_alias.tests.t10_basic.plugins.plugin6c_no_alias#Plugin6c",
            ),
            (
                "tests.t10_basic.plugins.subplugin.subplugin1#SubPlugin1",
                "test_func1",
                "tests.t10_basic.plugins.subplugin.subplugin1.tests.t10_basic.plugins.subplugin.subplugin1#SubPlugin1",
            ),
            (
                "tests.t10_basic.plugins.subplugin_init#SubPluginInit1",
                "test_func1",
                "tests.t10_basic.plugins.subplugin_init.tests.t10_basic.plugins.subplugin_init#SubPluginInit1",
            ),
            (
                "tests.t10_basic.plugins.subsubplugin.thesubsubplugin.subsubplugin1#SubSubPlugin1",
                "test_func1",
                "tests.t10_basic.plugins.subsubplugin.thesubsubplugin.subsubplugin1.tests.t10_basic.plugins."
                "subsubplugin.thesubsubplugin.subsubplugin1#SubSubPlugin1",
            ),
            (
                "tests.t10_basic.plugins.plugin7_method_order#Plugin7a",
                "test_func1",
                "tests.t10_basic.plugins.plugin7_method_order.tests.t10_basic.plugins.plugin7_method_order#Plugin7a",
            ),
        ]

        received_results = []
        for method, plugin in self.data["plugins"].methods(where_name="test_func1"):
            result = method.run()
            # Save plugin results with a name
            received_results.append((plugin.fqn, method.name, result))

        assert received_results == expected_results, "Results don't match what they should"

    def test_call_with_plugin_fqn(self) -> None:
        """Test calling a plugin method using a fully qualified plugin name."""

        expected_results = [
            (
                "tests.t10_basic.plugins.plugin1#Plugin1",
                "test_func1",
                "tests.t10_basic.plugins.plugin1.tests.t10_basic.plugins.plugin1#Plugin1",
            ),
        ]

        received_results = []
        for method, plugin in self.data["plugins"].methods(
            where_name="test_func1", from_plugin="tests.t10_basic.plugins.plugin1#Plugin1"
        ):
            result = method.run()
            # Save plugin results with a name
            received_results.append((plugin.fqn, method.name, result))

        assert received_results == expected_results, "Results don't match what they should"

    def test_call_with_plugin_name(self) -> None:
        """Test calling a plugin method using a plugin name."""

        expected_results = [
            (
                "tests.t10_basic.plugins.plugin1#Plugin1",
                "test_func1",
                "tests.t10_basic.plugins.plugin1.tests.t10_basic.plugins.plugin1#Plugin1",
            ),
        ]

        received_results = []
        for method, plugin in self.data["plugins"].methods(where_name="test_func1", from_plugin="#Plugin1"):
            result = method.run()
            # Save plugin results with a name
            received_results.append((plugin.fqn, method.name, result))

        assert received_results == expected_results, "Results don't match what they should"

    def test_call_with_plugin_alias(self) -> None:
        """Test calling a plugin method using a plugin alias."""

        expected_results = [
            (
                "tests.t10_basic.plugins.plugin6a_alias#Plugin6a",
                "test_func1",
                "tests.t10_basic.plugins.plugin6a_alias.tests.t10_basic.plugins.plugin6a_alias#Plugin6a",
            ),
            (
                "tests.t10_basic.plugins.plugin6b_alias#Plugin6b",
                "test_func1",
                "tests.t10_basic.plugins.plugin6b_alias.tests.t10_basic.plugins.plugin6b_alias#Plugin6b",
            ),
        ]

        received_results = []
        for method, plugin in self.data["plugins"].methods(where_name="test_func1", from_plugin="plugin6"):
            result = method.run()
            # Save plugin results with a name
            received_results.append((plugin.fqn, method.name, result))

        assert received_results == expected_results, "Results don't match what they should"
