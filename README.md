# Text-to-SQL com LLM

Aplicação de linha de comando que transforma perguntas em linguagem natural em consultas SQL usando um modelo local via Ollama.

O projeto conecta em um banco MySQL ou PostgreSQL, lê o schema disponível, envia a pergunta do usuário para o modelo e gera uma consulta `SELECT`. Antes de executar, o SQL gerado é exibido na tela e precisa ser confirmado pelo usuário.

## O Que O Projeto Faz

- Conecta em bancos MySQL ou PostgreSQL.
- Lê tabelas e colunas do banco informado.
- Usa um modelo local do Ollama para gerar SQL.
- Gera somente consultas `SELECT`.
- Mostra o SQL antes da execução.
- Executa a consulta somente após confirmação.
- Exibe o resultado em formato de tabela no terminal.

## Pré-Requisitos

- Python 3.10 ou superior.
- Ollama instalado e rodando na máquina.
- Um modelo instalado no Ollama, por exemplo:

```bash
ollama pull qwen2.5-coder:3b
```

- Um banco MySQL ou PostgreSQL acessível.

Por padrão, o projeto chama o Ollama em:

```text
http://localhost:11434
```

## Ambiente De Teste

O projeto foi testado no seguinte ambiente:

```text
OS: Ubuntu 22.04.5 LTS x86_64
Host: VJFE59F11X-B0711H
Kernel: 6.8.0-124-generic
Shell: bash 5.1.16
DE: GNOME 42.9
WM: Mutter
Terminal: gnome-terminal
CPU: AMD Ryzen 7 5700U with Radeon G
GPU: AMD ATI 04:00.0 Lucienne
Memory: 6184MiB / 7312MiB
```

## Portas Padrão Dos Bancos

| Banco | Porta padrão |
| --- | --- |
| MySQL | `3306` |
| PostgreSQL | `5432` |

Quando o banco estiver rodando na própria máquina, normalmente o host usado será:

```text
localhost
```

## Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone <url-do-repositorio>
cd textToSql
```

Crie e ative um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como Rodar

Execute:

```bash
python3 main.py
```

Ao iniciar, o programa pedirá os dados de conexão do banco.

Exemplo usando MySQL local:

```text
Banco [postgresql/mysql]: mysql
Host: localhost
Porta: 3306
Usuário: seu_usuario
Senha: sua_senha
Database: university
```

Exemplo usando PostgreSQL local:

```text
Banco [postgresql/mysql]: postgresql
Host: localhost
Porta: 5432
Usuário: seu_usuario
Senha: sua_senha
Database: university
```

Depois da conexão, o programa carrega o schema do banco e permite digitar perguntas em linguagem natural.

## Exemplos De Perguntas

```text
liste todos os professores
```

```text
liste o nome e salário de todos os professores
```

```text
liste o salário de cada professor por departamento
```

```text
qual é a média salarial dos professores por departamento
```

```text
liste os alunos do departamento de Biology
```

```text
quantos alunos existem em cada departamento
```

```text
liste os cursos que cada professor ensina
```

```text
mostre os alunos e seus orientadores
```

Para sair do programa, digite:

```text
sair
```

## Exemplo De Fluxo

```text
=== Text-to-SQL com LLM ===
Banco [postgresql/mysql]: mysql
Host: localhost
Porta: 3306
Usuário: pedro
Senha: aula123
Database: university

Conectando ao banco...
Carregando schema...

Digite sua pergunta ou 'sair': liste o salário de cada professor por departamento

Gerando SQL...

SQL gerado:
SELECT name, dept_name, salary FROM instructor;

Executar essa consulta? [s/N]: s
```

## Segurança

O projeto possui uma validação básica para reduzir risco de execução indevida:

- Bloqueia comandos que não sejam `SELECT`.
- Bloqueia palavras como `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `TRUNCATE`, `GRANT` e `REVOKE`.
- Mostra o SQL gerado antes de executar.
- Pede confirmação manual antes da execução.

Mesmo assim, a consulta é gerada por uma LLM. Para uso mais seguro, recomenda-se conectar com um usuário de banco somente leitura.

## Limitações

- A qualidade do SQL depende do modelo usado no Ollama.
- Perguntas ambíguas podem gerar consultas diferentes do esperado.
- O projeto depende do Ollama rodando localmente.
- A validação de segurança é simples e não substitui permissões adequadas no banco.
- O schema usado no prompt contém tabelas e colunas, mas não inclui exemplos de dados.

## Estrutura Dos Arquivos

```text
main.py           Entrada principal da aplicação
db.py             Conexão, leitura do schema e execução SQL
llm.py            Comunicação com Ollama e geração do SQL
sql_guard.py      Validação básica de segurança do SQL
requirements.txt  Dependências do projeto
```
