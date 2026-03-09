import pytest
from unittest.mock import patch

from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

@pytest.fixture
def mock_db():
    with patch("main.SessionLocal"):
        yield
