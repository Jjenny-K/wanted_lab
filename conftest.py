import pytest

from rest_framework.test import APIClient


@pytest.fixture()
def client():
    return APIClient()


# test error message custom
def pytest_assertrepr_compare(left, right, op):
    print("Assertion 왼쪽 값은 {0}, 오른쪽 값은 {1}, 비교 값은 {2}".format(left, right, op))
