from sqlalchemy.dialects import registry
import pytest

registry.register("databricks", "sqlalchemy_db", "DatabricksDialect")
# sqlalchemy's dialect-testing machinery wants an entry like this.
# This seems to be based around dialects maybe having multiple drivers
# and wanting to test driver-specific URLs, but doesn't seem to make
# much sense for dialects with only one driver.
registry.register("databricks.databricks", "sqlalchemy_db", "DatabricksDialect")

pytest.register_assert_rewrite("sqlalchemy.testing.assertions")

from sqlalchemy.testing.plugin.pytestplugin import *
