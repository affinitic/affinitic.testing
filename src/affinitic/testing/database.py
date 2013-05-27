# encoding: utf-8
"""
affinitic.testing

Created by mpeeters
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""

import inspect
import os
import sys
import time

import zope.component

from affinitic.db.interfaces import IDatabase
from affinitic.testing import case, utils


class DatabaseTestCase(case.BaseTestCase):
    databases = ()

    def run(self, result=None):
        """ Override of the run method from unittest2.TestCase """
        try:
            self._execute_sql_files(method='insert')
        except Exception:
            if not hasattr(result, '_start_time'):
                result._start_time = time.time()
            result.addError(self, sys.exc_info())
        else:
            super(DatabaseTestCase, self).run(result=result)
            try:
                self._execute_sql_files(method='delete')
            except Exception:
                result.addError(self, sys.exc_info())

    def _execute_sql_files(self, method='insert'):
        """ Executes the sql files to fill or clean the database """
        dbs = [d for d in self.databases if hasattr(self, '%s_sql_file' % d)]
        for database in dbs:
            for sql_file in self._sql_files(database, method):
                if os.path.exists(sql_file) is False:
                    raise ValueError('Missing file "%s"' % sql_file)
                utils.import_data_from_file(self._db_session(database),
                                            sql_file)

    def _sql_files(self, database, method):
        """ Returns a list of sql file for the given database and method """
        sql_files = getattr(self, '%s_sql_file' % database)
        if isinstance(sql_files, basestring) is True:
            sql_files = [sql_files]
        sql_directory = os.path.join(os.path.dirname(inspect.getfile(
            self.__class__)), 'sql')
        files = [os.path.join(sql_directory, '%s_%s_%s.sql' % (database, f,
            method)) for f in sql_files]
        if method == 'delete':
            files.reverse()
        return files

    def _db_session(self, database):
        """ Returns the %s_session property or the database utility """
        return getattr(self, '%s_session' % database,
                       zope.component.getUtility(IDatabase, database).session)
