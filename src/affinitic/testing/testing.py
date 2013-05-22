# encoding: utf-8
"""
affinitic.testing

Created by mpeeters
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""

from plone.testing import zca

from affinitic import testing as package


class TestResult(object):

    def __init__(self):
        self.error = 0
        self.success = 0

    def startTest(self, test_case):
        return

    def stopTest(self, test_case):
        return

    def addError(self, test_case, output):
        self.error += 1

    def addSuccess(self, test_case):
        self.success += 1


class DatabaseLayer(zca.ZCMLSandbox):
    pass


DB_LAYER = DatabaseLayer(name="DB_LAYER", filename="testing.zcml",
                         package=package)
