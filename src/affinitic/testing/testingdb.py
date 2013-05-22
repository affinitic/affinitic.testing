# encoding: utf-8
"""
affinitic.testing

Created by mpeeters
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""

import sqlalchemy as sa

import grokcore.component as grok
from zope.component import interfaces as zc_interfaces
from affinitic.db import db, interfaces


class TableA(object):
    pass


class TableB(object):
    pass


class IDBReady(zc_interfaces.IObjectEvent):
    pass


class DBReady(object):
    grok.implements(IDBReady)

    def __init__(self, objectToAdapt):
        self.object = objectToAdapt


class TestDB(db.DB):
    grok.name('testdb')
    notifyInterface = DBReady

    @property
    def url(self):
        return 'sqlite:///:memory:'


@grok.subscribe(interfaces.IMetadata, IDBReady)
def set_mappers(metadata, event):
    table_a = sa.Table('table_a', metadata,
                       sa.Column('pk', sa.Integer, primary_key=True,
                                 nullable=False),
                       sa.Column('a', sa.Text, nullable=False))
    sa.orm.mapper(TableA, table_a)
    table_b = sa.Table('table_b', metadata,
                       sa.Column('pk', sa.Integer, primary_key=True,
                                 nullable=False),
                       sa.Column('b', sa.Text, nullable=False))
    sa.orm.mapper(TableB, table_b)
    metadata.create_all()
