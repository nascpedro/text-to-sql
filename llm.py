import requests


def generate_sql(question, schema, model="qwen2.5-coder:3b", db_type="mysql"):
    prompt = f"""
Você é um gerador de SQL para {db_type}.

Use exclusivamente as tabelas e colunas abaixo.
Não use nenhuma coluna que não esteja listada no schema.

Schema do banco:
{schema}

Regras obrigatórias:
- Retorne somente uma consulta SQL.
- A consulta deve ser SELECT.
- Não use markdown.
- Não explique.
- Não invente tabelas.
- Não invente colunas.
- Verifique cuidadosamente se cada coluna usada pertence à tabela correta.
- Quando uma informação estiver diretamente em uma tabela, prefira consultar essa tabela diretamente, sem JOIN desnecessário.
- Use JOIN apenas quando a pergunta exigir dados que estejam em tabelas diferentes.
- Não use agregações como AVG, SUM, COUNT, MIN ou MAX, exceto quando a pergunta pedir explicitamente média, soma, total, quantidade, mínimo ou máximo.
- Quando a pergunta pedir "cada", "liste", "listar" ou "selecione", retorne linhas detalhadas, não um resumo agregado.
- Quando a pergunta pedir dados de professores, use a tabela instructor.
- Quando listar salário de professores, inclua pelo menos name, dept_name e salary quando essas colunas existirem no schema.
- Quando filtrar por departamento informado em português, use o valor equivalente em inglês quando ele aparecer no schema ou nos dados prováveis. Exemplo: biologia = Biology.

Pergunta:
{question}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_ctx": 4096
            }
        },
        timeout=120
    )

    response.raise_for_status()

    sql = response.json()["response"].strip()

    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql
