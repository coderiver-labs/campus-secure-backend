from rest_framework.test import APIClient

# import pytest
import pytest


# create fixture


@pytest.fixture
def api_client():
    return APIClient()

