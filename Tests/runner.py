import importlib
from pathlib import Path

from connect_4 import Board


def run_test(test_name, test_function):
    try:
        test_function(Board())
    except AssertionError as e:
        print(f"[FAIL] {test_name}")
        print(f"       Reason: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] {test_name}")
        print(f"       Reason: Unexpected Error -> {e}")
        return False
    print(f"[PASS] {test_name}")
    return True


def main():
    print("--- Starting Connect 4 Engine Autotest ---\n")
    tests = []
    # Match all test_ functions inside all test_*.py files in this directory.
    for test_file in Path(__file__).parent.glob("test_*.py"):
        module = importlib.import_module(f"{__package__}.{test_file.stem}")
        for name, test in vars(module).items():
            if name.startswith("test_") and callable(test):
                tests.append((name, test))
    passed_tests = 0
    for name, test in tests:
        if run_test(name, test):
            passed_tests += 1
    failed_tests = len(tests) - passed_tests

    print("\n--- Test Summary ---")
    print(f"Total Tests Run: {len(tests)}")
    print(f"Passing: {passed_tests}")
    print(f"Failed:  {failed_tests}")
    return 1 if failed_tests else 0


if __name__ == "__main__":
    raise SystemExit(main())
