import pytest
from core.sql_safety import validate_select_only


def test_valid_select():
    ok, reason = validate_select_only("SELECT * FROM fact_kpis")
    assert ok is True
    assert reason == ""


def test_select_with_join():
    sql = "SELECT a.id, b.value FROM fact_kpis a JOIN dim_date b ON a.date = b.date"
    ok, reason = validate_select_only(sql)
    assert ok is True
    assert reason == ""


def test_select_with_cte():
    sql = "WITH monthly AS (SELECT date, SUM(value) AS total FROM fact_kpis GROUP BY date) SELECT * FROM monthly"
    ok, reason = validate_select_only(sql)
    assert ok is True
    assert reason == ""


def test_drop_table():
    ok, reason = validate_select_only("DROP TABLE fact_kpis")
    assert ok is False
    assert "DROP" in reason


def test_stacked_select_then_drop():
    ok, reason = validate_select_only("SELECT * FROM fact_kpis; DROP TABLE fact_kpis")
    assert ok is False
    # Caught by the multiple-statement check, before the token walk
    assert "1 statement" in reason


def test_update():
    ok, reason = validate_select_only("UPDATE fact_kpis SET value = 0 WHERE date = '2024-01-01'")
    assert ok is False
    assert "UPDATE" in reason


def test_insert():
    ok, reason = validate_select_only("INSERT INTO fact_kpis (date, value) VALUES ('2024-01-01', 42)")
    assert ok is False
    assert "INSERT" in reason


def test_cte_with_delete_inside():
    sql = "WITH evil AS (DELETE FROM fact_kpis RETURNING date) SELECT * FROM evil"
    ok, reason = validate_select_only(sql)
    assert ok is False
    assert "DELETE" in reason
