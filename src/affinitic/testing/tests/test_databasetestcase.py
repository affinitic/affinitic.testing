# encoding: utf-8
"""
affinitic.testing

Created by mpeeters
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""

import inspect
import mock
import os

import zope.component
from affinitic.db import interfaces

from affinitic.testing import BaseTestCase, DatabaseTestCase
from affinitic.testing.testing import DB_LAYER, TestResult


class TestDatabaseTestCase(BaseTestCase):
    layer = DB_LAYER

    @property
    def _session(self):
        return zope.component.getUtility(interfaces.IDatabase,
                                         'testdb').session

    @property
    def _count(self):
        """ Returns the number of lines in table_a and table_b """
        query_count = 'select count(*) from %s'
        return (self._session.execute(query_count % 'table_a').fetchone()[0],
                self._session.execute(query_count % 'table_b').fetchone()[0])

    @property
    def _sql_directory(self):
        return os.path.join(os.path.dirname(inspect.getfile(self.__class__)),
                            'sql')

    def test_run_normal(self):
        db_case_cls = type('TestDatabaseTestCase', (DatabaseTestCase, ),
                           {'test_method': mock.Mock(return_value=None),
                            'databases': ('testdb', ),
                            'testdb_sql_file': ['table_a', 'table_b']})
        db_case = db_case_cls(methodName='test_method')
        test_result = TestResult()
        db_case.run(result=test_result)
        self.assertEqual((0, 0), self._count)
        self.assertEqual(0, test_result.error)
        self.assertEqual(1, test_result.success)

    def test_run_exception_before(self):
        db_case_cls = type('TestDatabaseTestCase', (DatabaseTestCase, ),
                           {'test_method': mock.Mock(return_value=None),
                            'databases': ('testdb', ),
                            'testdb_sql_file': ['table_a', 'table_b']})
        db_case = db_case_cls(methodName='test_method')
        db_case._execute_sql_files = mock.Mock(side_effect=ValueError)
        test_result = TestResult()
        db_case.run(result=test_result)
        self.assertEqual((0, 0), self._count)
        self.assertEqual(1, test_result.error)
        self.assertEqual(0, test_result.success)

    def test_run_exception_after(self):
        db_case_cls = type('TestDatabaseTestCase', (DatabaseTestCase, ),
                           {'test_method': mock.Mock(return_value=None),
                            'databases': ('testdb', ),
                            'testdb_sql_file': ['table_a', 'table_b']})
        db_case = db_case_cls(methodName='test_method')
        db_case._execute_sql_files = mock.Mock(side_effect=(None, ValueError))
        test_result = TestResult()
        db_case.run(result=test_result)
        self.assertEqual((0, 0), self._count)
        self.assertEqual(1, test_result.error)
        self.assertEqual(1, test_result.success)

    def test_execute_sql_file(self):
        db_case_cls = type('TestDatabaseTestCase', (DatabaseTestCase, ),
                           {'test_method': None,
                            'databases': ('testdb', ),
                            'testdb_sql_file': ['table_a', 'table_b',
                                                'view_a']})
        db_case = db_case_cls(methodName='test_method')
        self.assertEqual((0, 0), self._count)
        db_case._execute_sql_files(method='insert')
        self.assertEqual((4, 1), self._count)
        db_case._execute_sql_files(method='delete')
        self.assertEqual((0, 0), self._count)

    def test_execute_sql_file_error(self):
        db_case_cls = type('TestDatabaseTestCase', (DatabaseTestCase, ),
                           {'test_method': None,
                            'databases': ('testdb', ),
                            'testdb_sql_file': ['table_x']})
        db_case = db_case_cls(methodName='test_method')
        self.assertRaises(ValueError, db_case._execute_sql_files)

    def test_sql_files_not_list(self):
        db_case_cls = type('TestDatabaseTestCase', (DatabaseTestCase, ),
                           {'test_method': None,
                            'db_sql_file': 'table'})
        db_case = db_case_cls(methodName='test_method')
        filepath = os.path.join(self._sql_directory, 'db_table_insert.sql')
        self.assertEqual([filepath], db_case._sql_files('db', 'insert'))

    def test_sql_files_delete(self):
        db_case_cls = type('TestDatabaseTestCase', (DatabaseTestCase, ),
                           {'test_method': None,
                            'db_sql_file': ['table_a', 'table_b']})
        db_case = db_case_cls(methodName='test_method')
        files = [os.path.join(self._sql_directory, 'db_table_b_delete.sql'),
                 os.path.join(self._sql_directory, 'db_table_a_delete.sql')]
        self.assertEqual(files, db_case._sql_files('db', 'delete'))

    def test_custom_sql_directory(self):
        db_case_cls = type('TestDatabaseTestCase', (DatabaseTestCase, ),
                           {'test_method': None,
                            'sql_directory': '../tests/sql/',
                            'db_sql_file': 'table'})
        db_case = db_case_cls(methodName='test_method')
        cls_path = os.path.dirname(inspect.getfile(self.__class__))
        filepath = os.path.join(cls_path, '..', 'tests', 'sql',
                                'db_table_insert.sql')
        self.assertEqual([filepath], db_case._sql_files('db', 'insert'))
