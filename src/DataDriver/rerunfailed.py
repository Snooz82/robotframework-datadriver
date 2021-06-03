"""Pre-run modifier that excludes tests that run PASS last time.
"""

import os
import re

from robot.api import ExecutionResult, ResultVisitor, SuiteVisitor  # type: ignore
from robot.running.model import Variable  # type: ignore


class rerunfailed(SuiteVisitor):
    def __init__(self, original_output_xml):
        if not os.path.isfile(original_output_xml):
            raise FileNotFoundError(f"{original_output_xml} is no file")
        result = ExecutionResult(original_output_xml)
        results_visitor = DataDriverResultsVisitor()
        result.visit(results_visitor)
        self._failed_tests = results_visitor.failed_tests

    def start_suite(self, suite):
        """Remove tests that match the given pattern."""
        if self.has_no_tests(suite.name):
            suite.tests.clear()
            return None
        if self._suite_is_data_driven(suite):
            dynamic_tests = Variable("@{DYNAMICTESTS}", self._failed_tests, suite.source)
            suite.resource.variables.append(dynamic_tests)
        else:
            suite.tests = [
                t for t in suite.tests if f"{t.parent.name}.{t.name}" in self._failed_tests
            ]

    def has_no_tests(self, name):
        r = re.compile(f'^{re.escape(f"{name}.")}.*$')
        return not bool(list(filter(r.match, self._failed_tests)))

    def _suite_is_data_driven(self, suite):
        for resource in suite.resource.imports:
            if resource.name == "DataDriver":
                return True

    def end_suite(self, suite):
        """Remove suites that are empty after removing tests."""
        suite.suites = [s for s in suite.suites if s.test_count > 0]

    def visit_test(self, test):
        """Avoid visiting tests and their keywords to save a little time."""
        pass


class DataDriverResultsVisitor(ResultVisitor):
    def __init__(self):
        self.failed_tests = list()

    def start_test(self, test):
        if test.status == "FAIL":
            self.failed_tests.append(f"{test.parent.name}.{test.name}")
