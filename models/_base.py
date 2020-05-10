#!/usr/bin/env python3
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

__all__ = ['Base']
mymetadata = MetaData(schema='public')
Base = declarative_base(metadata=mymetadata)
