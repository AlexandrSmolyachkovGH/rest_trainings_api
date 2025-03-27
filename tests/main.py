import pytest

if __name__ == "__main__":
    exit_code = pytest.main(["-v", "--tb=short", "--capture=no"])
    exit(exit_code)
