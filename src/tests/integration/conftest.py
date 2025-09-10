def pytest_addoption(parser):
    parser.addoption(
        "--api-url-value", action="store", default="default_value",
        help="Value to use for parameterizing tests"
    )

def pytest_generate_tests(metafunc):
    if "api_url" in metafunc.fixturenames:
        param_value = metafunc.config.getoption("api_url_value")
        metafunc.parametrize("api_url", [param_value])
