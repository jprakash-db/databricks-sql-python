"""
The order of these imports is important. Test cases are imported first from SQLAlchemy,
then are overridden by our local skip markers in _regression, _unsupported, and _future.
"""


# type: ignore
# fmt: off
from sqlalchemy.testing.suite import *
from sqlalchemy_db.test._regression import *
from sqlalchemy_db.test._unsupported import *
from sqlalchemy_db.test._future import *
from sqlalchemy_db.test._extra import TinyIntegerTest, DateTimeTZTestCustom
