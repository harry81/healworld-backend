from django_nose import NoseTestSuiteRunner
from djcelery.contrib.test_runner import CeleryTestSuiteRunner


class TestRunner(CeleryTestSuiteRunner, NoseTestSuiteRunner):
    pass
