from tabulate import tabulate

from db import build_db_url, connect, get_schema, execute_select
from llm import generate_sql
from sql_guard import is_safe_select


def main():
    print("=== Text-to-SQL com LLM ===")

    db_type = input("Banco [postgresql/mysql]: ").strip().lower()
    host = input("Host: ").strip()
    port = input("Porta: ").strip()
    user = input("Usuário: ").strip()
    password = input("Senha: ").strip()
    database = input("Database: ").strip()

    db_url = build_db_url(db_type, user, password, host, port, database)

    print("\nConectando ao banco...")
    engine = connect(db_url)

    print("Carregando schema...")
    schema = get_schema(engine)

    print("\nSchema encontrado:")
    print(schema)

    model = "qwen2.5-coder:3b"

    while True:
        question = input("\nDigite sua pergunta ou 'sair': ").strip()

        if question.lower() == "sair":
            break

        print("\nGerando SQL...")
        sql = generate_sql(question, schema, model, db_type)

        print("\nSQL gerado:\n")
        print(sql)

        if not is_safe_select(sql):
            print("\nSQL bloqueado por segurança. Apenas SELECT é permitido.")
            continue

        confirm = input("\nExecutar essa consulta? [s/N]: ").strip().lower()

        if confirm != "s":
            print("Consulta cancelada.")
            continue

        try:
            columns, rows = execute_select(engine, sql)

            print("\nResultado:")
            print(tabulate(rows, headers=columns, tablefmt="grid"))

        except Exception as e:
            print("\nErro ao executar SQL:")
            print(e)


if __name__ == "__main__":
    main()
