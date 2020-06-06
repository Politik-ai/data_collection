import os
import middle.json
import yaml
import os
from datetime import date
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Date, sql
from sqlalchemy.orm import sessionmaker
import csv
from sqlalchemy.ext.declarative import declarative_base

"""
Given 2D array--
Each row:
Note: locations are relative to: 

1. dir path to eg. "hr2/"
data.json  (not bill-state dependent) (get from dir path above)
2. congress num
3. bill type (eg. hr or s)
4. bill code (eh, ih)


parse data.json
link data and insert to database
"""

bills = Table(
    'bills', meta
)