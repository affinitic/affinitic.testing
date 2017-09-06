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


class DatabaseBase(object):
    databases = ()

    def _execute_sql_files(self, method='insert'):
        """ Executes the sql files to fill or clean the database """
        dbs = [d for d in self.databases if hasattr(self, '%s_sql_file' % d)]
        for database in dbs:
            session = self._db_session(database)
            for sql_file in self._sql_files(database, method):
                if os.path.exists(sql_file) is False:
                    raise ValueError('Missing file "%s"' % sql_file)
                utils.import_data_from_file(session, sql_file)
            session.close()

    def _sql_files(self, database, method):
        """ Returns a list of sql file for the given database and method """
        sql_files = getattr(self, '%s_sql_file' % database)
        if isinstance(sql_files, basestring) is True:
            sql_files = [sql_files]
        sql_directory = self._sql_directory
        files = [os.path.join(sql_directory, '%s_%s_%s.sql' % (database, f,
                                                               method))
                 for f in sql_files]
        if method == 'delete':
            files.reverse()
        return files

    @property
    def _sql_directory(self):
        """Return the directory with the sql file if the variable
        sql_directory is not defined the default path is ./sql"""
        cls_path = os.path.dirname(inspect.getfile(self.__class__))
        if hasattr(self, 'sql_directory'):
            return os.path.join(cls_path, self.sql_directory)
        return os.path.join(cls_path, 'sql')

    def _db_session(self, database):
        """ Returns the %s_session property or the database utility """
        return (getattr(self, '%s_session' % database, None) or
                zope.component.getUtility(IDatabase, database).session)


class DatabaseTestCase(case.BaseTestCase, DatabaseBase):

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
