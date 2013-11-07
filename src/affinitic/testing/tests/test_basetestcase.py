# encoding: utf-8
"""
affinitic.testing

Created by mpeeters
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""

import mock

from affinitic.testing import BaseTestCase
from affinitic.testing.testing import TestResult


class Monster(object):
    name = u'CERBERUS'
    _weight = 100

    def __init__(self, age):
        self._age = age

    def growl(self):
        return u'GRRR'

    @property
    def age(self):
        return self._age

    @staticmethod
    def size():
        return 10

    @classmethod
    def weight(cls):
        return cls._weight


class Obj(object):
    __slots__ = ('attr1', )

    @property
    def test(self):
        return 'FOO'


def message(text=u'FOO'):
    return text


class TestBaseTestCase(BaseTestCase):

    def test_run_normal(self):
        test_case_cls = type('TestTestCase', (BaseTestCase, ),
                             {'test_method': mock.Mock(return_value=None)})
        test_case = test_case_cls(methodName='test_method')
        test_result = TestResult()
        test_case.run(result=test_result)
        self.assertEqual(0, test_result.error)
        self.assertEqual(1, test_result.success)

    def test_run_with_exception(self):
        test_case_cls = type('TestTestCase', (BaseTestCase, ),
                             {'test_method': mock.Mock(return_value=None)})
        test_case = test_case_cls(methodName='test_method')
        test_case._cleanup = mock.Mock(side_effect=ValueError)
        test_result = TestResult()
        test_case.run(result=test_result)
        self.assertEqual(1, test_result.error)
        self.assertEqual(1, test_result.success)

    def test_cleanup(self):
        from affinitic.testing.tests import test_basetestcase
        test_case_cls = type('TestTestCase', (BaseTestCase, ),
                             {'test_method': mock.Mock(return_value=None)})
        test_case = test_case_cls(methodName='test_method')
        test_case.mock(test_basetestcase, 'message', return_value='BAR')
        self.assertEqual(1, len(test_case._mocks))
        test_case._cleanup()
        self.assertEqual(0, len(test_case._mocks))

    def test_mock_function(self):
        from affinitic.testing.tests import test_basetestcase
        self.assertEqual(u'FOO', message())
        self.mock(test_basetestcase, 'message',
                  mock=mock.Mock(return_value=u'BAR'))
        self.assertIsInstance(test_basetestcase.message, mock.Mock)
        self.assertEqual(u'BAR', message())

        self.unmock(message)
        self.assertEqual(u'FOO', message())

    def test_mock_class(self):
        from affinitic.testing.tests import test_basetestcase
        self.assertEqual(u'CERBERUS', Monster.name)
        self.mock(test_basetestcase, 'Monster',
                  mock=type('Vampire', (object, ), {'name': u'DRACULA'}))
        self.assertEqual(u'DRACULA', Monster.name)

        self.unmock(Monster)
        self.assertEqual(u'CERBERUS', Monster.name)

    def test_mock_method(self):
        from affinitic.testing.tests import test_basetestcase
        self.assertEqual(u'GRRR', Monster(3000).growl())
        self.mock(test_basetestcase.Monster, u'growl', return_value=u'BOOOO')
        self.assertEqual(u'BOOOO', Monster(3000).growl())

    def test_mock_property(self):
        from affinitic.testing.tests import test_basetestcase
        self.assertEqual(3000, Monster(3000).age)
        self.mock(test_basetestcase.Monster, u'age', return_value=20)
        self.assertEqual(20, Monster(3000).age)

        self.unmock(Monster.age)
        self.assertEqual(3000, Monster(3000).age)

    def test_mock_staticmethod(self):
        from affinitic.testing.tests import test_basetestcase
        self.assertEqual(10, Monster(3000).size())
        self.assertEqual(10, Monster.size())
        self.mock(test_basetestcase.Monster, u'size', return_value=5)
        self.assertEqual(5, Monster(3000).size())
        self.assertEqual(5, Monster.size())

        self.unmock(Monster.size)
        self.assertEqual(10, Monster(3000).size())
        self.assertEqual(10, Monster.size())

    def test_mock_classmethod(self):
        self.assertEqual(100, Monster.weight())
        self.mock(Monster, 'weight', return_value=200)
        self.assertEqual(200, Monster.weight())

        self.unmock(Monster.weight)
        self.assertEqual(100, Monster.weight())

    def test_mock_without_kwargs(self):
        from affinitic.testing.tests import test_basetestcase
        self.assertRaises(ValueError, self.mock, test_basetestcase, 'message')

    def test_mock_multiple_possibilities(self):
        from affinitic.testing.tests import test_basetestcase
        self.mock(test_basetestcase, 'message', mock=mock.Mock(return_value=0),
                  return_value=1)
        self.assertEqual(0, test_basetestcase.message())

    def test_multiple_mock(self):
        from affinitic.testing.tests import test_basetestcase
        self.mock(test_basetestcase, 'message', return_value=0)
        self.mock(test_basetestcase, 'message', return_value=1)
        self.assertEqual(1, test_basetestcase.message())
        self.unmock(test_basetestcase.message)
        self.assertEqual(1, len(self._mocks))
        self.assertEqual('FOO', test_basetestcase.message())

    def test_get_object(self):
        """ Test the _get_object method with an object without __dict__ """
        test_object = Monster(10)
        self.assertEqual(getattr(test_object, 'size')(),
                         self._get_object(test_object, 'size')())
