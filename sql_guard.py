import sqlparse


BLOCKED_KEYWORDS = [
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "create",
    "truncate",
    "grant",
    "revoke"
]


def is_safe_select(sql):
    parsed = sqlparse.parse(sql)

    if not parsed:
        return False

    first_statement = parsed[0]

    if first_statement.get_type() != "SELECT":
        return False

    sql_lower = sql.lower()

    for keyword in BLOCKED_KEYWORDS:
        if keyword in sql_lower:
            return False

    return True