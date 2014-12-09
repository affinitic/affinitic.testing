# encoding: utf-8
"""
affinitic.testing

Created by mpeeters
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""

import sqlparse

from Products.Transience.TransientObject import TransientObject

from zope.publisher.browser import TestRequest


def import_data_from_file(session, filepath):
    fd = open(filepath, 'r')
    for sql in split_sql_statements(fd.read()):
        session.bind.execute(sql)
    fd.close()


def split_sql_statements(sql):
    statements = [s.strip() for s in sql.splitlines()]
    sql = ' '.join([s for s in statements if not s.startswith('--')])
    return sqlparse.split(sql)


class AdvancedTestRequest(TestRequest):

    __items = {}

    def __init__(self, *params, **kw):
        super(AdvancedTestRequest, self).__init__(*params, **kw)
        self.SESSION = TransientObject('1234')

    def __setitem__(self, key, value):
        """
        """
        self.__items[key] = value

    def __getitem__(self, key):
        """
        """
        return self.__items[key]
