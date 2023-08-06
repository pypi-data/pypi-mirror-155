# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import wrapt
from flask_sqlalchemy import SQLAlchemy

import apm_client.sqlalchemy


def instrument_sqlalchemy(db):
    SQLAlchemy.get_engine = wrapped_get_engine(SQLAlchemy.get_engine)


@wrapt.decorator
def wrapped_get_engine(wrapped, instance, args, kwargs):
    engine = wrapped(*args, **kwargs)
    apm_client.sqlalchemy.instrument_sqlalchemy(engine)
    return engine
