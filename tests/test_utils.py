import pandas as pd
import pytest

from rugby_stats_scraper.utils import check_file_has_data, get_json_element


@pytest.fixture
def data_folder(tmp_path):
    test_data_folder = tmp_path / "test_data"
    test_data_folder.mkdir()
    return test_data_folder


def test_get_json_element():
    # Test a dictionary with a single level of keys
    test_dict = {"a": 1, "b": 2, "c": 3}
    assert get_json_element(test_dict, ("a",)) == 1
    assert get_json_element(test_dict, ("b",)) == 2
    assert get_json_element(test_dict, ("c",)) == 3

    # Test a nested dictionary
    test_dict = {"a": {"b": {"c": 1}}}
    assert get_json_element(test_dict, ("a", "b", "c")) == 1

    # Test a path that doesn't exist
    assert get_json_element(test_dict, ("a", "b", "d")) is None


def test_check_file_has_data(data_folder):
    # Create an empty CSV file
    empty_file = data_folder / "empty_file.csv"
    empty_file.touch()
    assert not check_file_has_data(empty_file)

    # Create a non-empty CSV file
    nonempty_file = data_folder / "nonempty_file.csv"
    pd.DataFrame({"a": [1, 2, 3]}).to_csv(nonempty_file, index=False)
    assert check_file_has_data(nonempty_file)

    # Create a file that doesn't exist
    nonexistent_file = data_folder / "nonexistent_file.csv"
    assert not check_file_has_data(nonexistent_file)
