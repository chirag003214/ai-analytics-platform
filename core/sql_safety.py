import sqlparse
import sqlparse.tokens as T

# Keywords that must never appear anywhere in the token tree
FORBIDDEN = {"DROP", "CREATE", "ALTER", "TRUNCATE", "INSERT", "UPDATE", "DELETE"}


def _iter_tokens(token):
    """Yield every token in the tree, depth-first."""
    yield token
    if hasattr(token, "tokens"):
        for child in token.tokens:
            yield from _iter_tokens(child)


def validate_select_only(sql: str) -> tuple[bool, str]:
    """
    Return (True, "") when sql is a single SELECT with no dangerous keywords.
    Return (False, reason) otherwise.

    Checks performed (in order):
      1. Exactly one non-empty statement.
      2. Full recursive token walk — rejects any DDL or DML keyword in
         FORBIDDEN regardless of nesting depth (catches CTEs with DELETE, etc.).
      3. At least one SELECT token exists anywhere in the tree — ensures the
         query is actually a SELECT even for CTEs where get_type() returns None.
    """
    statements = [s for s in sqlparse.parse(sql.strip()) if str(s).strip()]

    if len(statements) != 1:
        return (False, f"Expected 1 statement, got {len(statements)}")

    stmt = statements[0]

    found_select = False
    for token in _iter_tokens(stmt):
        if token.ttype in (T.DDL, T.DML):
            val = token.normalized.upper()
            if val in FORBIDDEN:
                return (False, f"Forbidden keyword: {val}")
            if val == "SELECT":
                found_select = True

    if not found_select:
        return (False, "No SELECT statement found")

    return (True, "")
