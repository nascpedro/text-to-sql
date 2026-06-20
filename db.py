from sqlalchemy import create_engine, inspect, text


def build_db_url(db_type, user, password, host, port, database):
    if db_type == "postgresql":
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    if db_type == "mysql":
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    raise ValueError("Tipo de banco inválido. Use postgresql ou mysql.")


def connect(db_url):
    return create_engine(db_url)


def get_schema(engine):
    inspector = inspect(engine)
    schema_lines = []

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)

        column_names = []
        for col in columns:
            column_names.append(f"{col['name']} ({col['type']})")

        schema_lines.append(f"Tabela: {table_name}")
        schema_lines.append("Colunas: " + ", ".join(column_names))
        schema_lines.append("")

    return "\n".join(schema_lines)


def execute_select(engine, sql):
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        columns = result.keys()

    return columns, rows