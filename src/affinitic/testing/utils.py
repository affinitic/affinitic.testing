# encoding: utf-8
"""
affinitic.testing

Created by mpeeters
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""


def import_data_from_file(session, filepath):
    fd = open(filepath, 'r')
    session.bind.execute(fd.read())
    fd.close()
