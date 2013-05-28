# encoding: utf-8
"""
affinitic.testing

Created by mpeeters
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""

import pickle
import sys
import unittest2
import warnings
from mock import Mock


class BaseTestCase(unittest2.TestCase):
    _mocks = {}

    def run(self, result=None):
        """ Override of the run method from unittest2.TestCase """
        super(BaseTestCase, self).run(result=result)
        try:
            self._cleanup()
        except Exception:
            result.addError(self, sys.exc_info())

    def _cleanup(self):
        for key in self._mocks:
            self._unmock(key)
        self._mocks = dict()

    def mock(self, source, obj_name, **kw):
        """
        Start mocking the given function, class or method

        :param source:  A module or a class that contains the object that need
            to be mocked

        :param obj_name:  The name of the object that need to be mocked

        :param mock:  Optional parameter to specify a replacement for the
            original object, that can be a Mock instance or any other object

        :param return_value:  Optional parameter to specify the return value
            that will be used to create a mock object.
        """
        if 'mock' not in kw and 'return_value' not in kw:
            raise ValueError(u'A mock instance or a return value must be '
                             u'provided!')
        if 'mock' in kw and 'return_value' in kw:
            warnings.warn(u'A mock instance and a return value was provided, '
                          u'the mock instance will be used.')
        mock = kw.get('mock', Mock(return_value=kw.get('return_value')))
        obj = self._get_object(source, obj_name)
        if isinstance(obj, Mock):
            self.unmock(obj)
            obj = getattr(source, obj_name)
        if isinstance(obj, property):
            mock = property(mock)
        setattr(source, obj_name, mock)
        self._mocks[self._mock_key(mock)] = {'src': source,
                                             'name': obj_name,
                                             'original': obj}

    @staticmethod
    def _get_object(source, obj_name):
        """ Returns the object from the source """
        if hasattr(source, '__dict__') and obj_name in source.__dict__:
            return source.__dict__.get(obj_name)
        return getattr(source, obj_name)

    def unmock(self, obj):
        """ Stop mocking the given function, class or method """
        key = self._mock_key(obj)
        self._unmock(key)
        del self._mocks[key]

    def _mock_key(self, obj):
        """ Returns a mocking key for the given object """
        return pickle.dumps(str(obj))

    def _unmock(self, key):
        """ Unmock a key """
        mock = self._mocks.get(key)
        setattr(mock.get('src'), mock.get('name'), mock.get('original'))
