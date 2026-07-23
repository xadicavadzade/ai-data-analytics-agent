import pytest

from app.validation.sql_validation import SQLValidator


validator = SQLValidator()


def test_valid_select_query():
    validator.validate_sql(
        "SELECT * FROM employees"
    )


def test_empty_sql():
    with pytest.raises(ValueError):
        validator.validate_sql("")


def test_drop_table():
    with pytest.raises(ValueError):
        validator.validate_sql(
            "DROP TABLE employees"
        )


def test_delete_query():
    with pytest.raises(ValueError):
        validator.validate_sql(
            "DELETE FROM employees"
        )


def test_update_query():
    with pytest.raises(ValueError):
        validator.validate_sql(
            "UPDATE employees SET salary=100"
        )


def test_insert_query():
    with pytest.raises(ValueError):
        validator.validate_sql(
            "INSERT INTO employees VALUES (1)"
        )


def test_non_select_query():
    with pytest.raises(ValueError):
        validator.validate_sql(
            "CREATE TABLE users(id INTEGER)"
        )