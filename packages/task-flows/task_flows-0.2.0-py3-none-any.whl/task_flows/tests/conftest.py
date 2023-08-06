import pytest
from task_flows.admin import create_tables


@pytest.fixture
def tables():
    # TODO temp db.
    # TODO pg url.
    create_tables()
