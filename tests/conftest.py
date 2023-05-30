# mypy: disable-error-code="no-any-return"
import pytest

def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--live", action="store_true", help="run integration tests live")
    parser.addoption("--delay", action="store", default="0.1", help="delay used when running integration tests live")

@pytest.fixture
def live(request: pytest.FixtureRequest) -> bool:
    return request.config.getoption("--live")

@pytest.fixture
def delay(request: pytest.FixtureRequest) -> float:
    return float(request.config.getoption("--delay"))


