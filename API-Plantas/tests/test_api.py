from unittest.mock import patch

import pytest

from app import criar_app


PLANTA = {
    "id": 1,
    "nome_popular": "Jiboia",
    "nome_cientifico": "Epipremnum aureum",
    "tipo": "Trepadeira",
    "necessidade_luz": "Luz indireta",
    "frequencia_rega_dias": 7,
    "toxica": True,
}

ENTRADA = {chave: valor for chave, valor in PLANTA.items() if chave != "id"}


@pytest.fixture
def cliente():
    app = criar_app({"TESTING": True})
    return app.test_client()


@patch("Controller.PlantaController.Planta.consultar_todas", return_value=[PLANTA])
def test_consultar_todas(mock_consultar, cliente):
    resposta = cliente.get("/api/plantas")
    assert resposta.status_code == 200
    assert resposta.get_json() == [PLANTA]
    mock_consultar.assert_called_once()


@patch("Controller.PlantaController.Planta.consultar_por_id", return_value=PLANTA)
def test_consultar_por_id(mock_consultar, cliente):
    resposta = cliente.get("/api/plantas/1")
    assert resposta.status_code == 200
    assert resposta.get_json() == PLANTA
    mock_consultar.assert_called_once_with(1)


@patch("Controller.PlantaController.Planta.consultar_por_id", return_value=None)
def test_consultar_id_inexistente(mock_consultar, cliente):
    resposta = cliente.get("/api/plantas/999")
    assert resposta.status_code == 404
    assert resposta.get_json()["erro"] == "Planta não encontrada."


@patch("Controller.PlantaController.Planta.consultar_por_id", return_value=PLANTA)
@patch("Controller.PlantaController.Planta.cadastrar", return_value=1)
def test_cadastrar(mock_cadastrar, mock_consultar, cliente):
    resposta = cliente.post("/api/plantas", json=ENTRADA)
    assert resposta.status_code == 201
    assert resposta.get_json()["planta"] == PLANTA
    mock_cadastrar.assert_called_once_with(ENTRADA)


def test_cadastrar_com_dados_invalidos(cliente):
    resposta = cliente.post("/api/plantas", json={"nome_popular": "Jiboia"})
    assert resposta.status_code == 400
    assert "Campos obrigatórios ausentes" in resposta.get_json()["erro"]


@patch("Controller.PlantaController.Planta.atualizar", return_value=True)
@patch("Controller.PlantaController.Planta.consultar_por_id", return_value=PLANTA)
def test_atualizar(mock_consultar, mock_atualizar, cliente):
    resposta = cliente.put("/api/plantas/1", json=ENTRADA)
    assert resposta.status_code == 200
    assert resposta.get_json()["planta"] == PLANTA
    mock_atualizar.assert_called_once_with(1, ENTRADA)


@patch("Controller.PlantaController.Planta.excluir", return_value=True)
@patch("Controller.PlantaController.Planta.consultar_por_id", return_value=PLANTA)
def test_excluir(mock_consultar, mock_excluir, cliente):
    resposta = cliente.delete("/api/plantas/1")
    assert resposta.status_code == 200
    assert resposta.get_json()["mensagem"] == "Planta excluída com sucesso."
    mock_excluir.assert_called_once_with(1)


def test_swagger_disponivel(cliente):
    resposta = cliente.get("/apidocs/")
    assert resposta.status_code == 200

