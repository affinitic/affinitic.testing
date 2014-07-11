# encoding: utf-8
"""
affinitic.testing

Created by mpeeters
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""

import sqlparse


def import_data_from_file(session, filepath):
    fd = open(filepath, 'r')
    for sql in split_sql_statements(fd.read()):
        session.bind.execute(sql)
    fd.close()


def split_sql_statements(sql):
    sql = ''.join(sql.splitlines())
    return sqlparse.split(sql)
