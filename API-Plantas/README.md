# API de Plantas

Projeto acadêmico de uma API REST em Python, Flask e MySQL, organizado no padrão MVC. A API possui cinco endpoints CRUD e documentação interativa com Swagger.

## Estrutura

```text
API-Plantas/
├── Config/conexao.py
├── Controller/PlantaController.py
├── Model/Planta.py
├── View/PlantaView.py
├── tests/test_api.py
├── app.py
├── database.sql
└── requirements.txt
```

O banco se chama `api_plantas`. A tabela `plantas` está no plural e possui sete colunas. O arquivo e a classe do Model se chamam `Planta`, no singular.

## 1. Criar o banco no phpMyAdmin

1. Inicie o Apache e o MySQL no XAMPP.
2. Acesse `http://localhost/phpmyadmin`.
3. Abra a aba **SQL**.
4. Cole todo o conteúdo de `database.sql` e clique em **Executar**.

O script cria o banco, a tabela e oito registros de exemplo.

## 2. Preparar o ambiente virtual

No terminal, entre na pasta do projeto e execute:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --upgrade -r requirements.txt
```

As configurações padrão já funcionam no XAMPP com usuário `root`, senha vazia e porta `3306`. Caso sua instalação seja diferente:

```bash
cp .env.example .env
```

Depois, edite o arquivo `.env`.

## 3. Executar

Com o ambiente virtual ativado:

```bash
python app.py
```

- API: `http://127.0.0.1:5000/api/plantas`
- Swagger: `http://127.0.0.1:5000/apidocs/`

## Endpoints

| Método | Endpoint | Função |
|---|---|---|
| GET | `/api/plantas` | Consultar todas |
| GET | `/api/plantas/{id}` | Consultar por ID |
| POST | `/api/plantas` | Cadastrar |
| PUT | `/api/plantas/{id}` | Atualizar |
| DELETE | `/api/plantas/{id}` | Excluir |

### JSON para cadastrar ou atualizar

```json
{
  "nome_popular": "Jiboia",
  "nome_cientifico": "Epipremnum aureum",
  "tipo": "Trepadeira",
  "necessidade_luz": "Luz indireta",
  "frequencia_rega_dias": 7,
  "toxica": true
}
```

## Testes automatizados

```bash
pytest -v
```

Os testes usam simulações do Model para validar separadamente os cinco endpoints, as validações e o acesso ao Swagger. Para a apresentação, também teste as operações pelo botão **Try it out** do Swagger depois de importar o banco.
