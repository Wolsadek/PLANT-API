import mysql.connector
from flasgger import swag_from
from flask import Blueprint, request

from Model.Planta import Planta
from View.PlantaView import PlantaView


plantas_bp = Blueprint("plantas", __name__)

CAMPOS_OBRIGATORIOS = (
    "nome_popular",
    "nome_cientifico",
    "tipo",
    "necessidade_luz",
    "frequencia_rega_dias",
    "toxica",
)


def validar_dados(dados):
    if not isinstance(dados, dict):
        return "Envie os dados em formato JSON."

    faltando = [campo for campo in CAMPOS_OBRIGATORIOS if campo not in dados]
    if faltando:
        return f"Campos obrigatórios ausentes: {', '.join(faltando)}."

    campos_texto = (
        "nome_popular",
        "nome_cientifico",
        "tipo",
        "necessidade_luz",
    )
    if any(not isinstance(dados[campo], str) or not dados[campo].strip() for campo in campos_texto):
        return "Os campos de texto não podem estar vazios."

    frequencia = dados["frequencia_rega_dias"]
    if isinstance(frequencia, bool) or not isinstance(frequencia, int) or frequencia < 1:
        return "frequencia_rega_dias deve ser um número inteiro maior que zero."

    if not isinstance(dados["toxica"], bool):
        return "toxica deve ser true ou false."

    return None


class PlantaController:
    @staticmethod
    @plantas_bp.get("/plantas")
    @swag_from(
        {
            "tags": ["Plantas"],
            "summary": "Consultar todas as plantas",
            "responses": {
                200: {
                    "description": "Lista de plantas",
                    "schema": {"type": "array", "items": {"$ref": "#/definitions/Planta"}},
                },
                500: {"$ref": "#/responses/ErroInterno"},
            },
        }
    )
    def listar():
        try:
            return PlantaView.listar(Planta.consultar_todas())
        except mysql.connector.Error:
            return PlantaView.erro("Não foi possível consultar o banco de dados.", 500)

    @staticmethod
    @plantas_bp.get("/plantas/<int:planta_id>")
    @swag_from(
        {
            "tags": ["Plantas"],
            "summary": "Consultar uma planta pelo ID",
            "parameters": [{"name": "planta_id", "in": "path", "type": "integer", "required": True}],
            "responses": {
                200: {"description": "Planta encontrada", "schema": {"$ref": "#/definitions/Planta"}},
                404: {"description": "Planta não encontrada"},
                500: {"$ref": "#/responses/ErroInterno"},
            },
        }
    )
    def consultar_por_id(planta_id):
        try:
            planta = Planta.consultar_por_id(planta_id)
            if planta is None:
                return PlantaView.erro("Planta não encontrada.", 404)
            return PlantaView.exibir(planta)
        except mysql.connector.Error:
            return PlantaView.erro("Não foi possível consultar o banco de dados.", 500)

    @staticmethod
    @plantas_bp.post("/plantas")
    @swag_from(
        {
            "tags": ["Plantas"],
            "summary": "Cadastrar uma planta",
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {"$ref": "#/definitions/PlantaEntrada"},
                }
            ],
            "responses": {
                201: {"description": "Planta cadastrada"},
                400: {"description": "Dados inválidos"},
                500: {"$ref": "#/responses/ErroInterno"},
            },
        }
    )
    def cadastrar():
        dados = request.get_json(silent=True)
        erro = validar_dados(dados)
        if erro:
            return PlantaView.erro(erro, 400)

        try:
            planta_id = Planta.cadastrar(dados)
            planta = Planta.consultar_por_id(planta_id)
            return PlantaView.criada(planta)
        except mysql.connector.Error:
            return PlantaView.erro("Não foi possível cadastrar a planta.", 500)

    @staticmethod
    @plantas_bp.put("/plantas/<int:planta_id>")
    @swag_from(
        {
            "tags": ["Plantas"],
            "summary": "Atualizar uma planta",
            "parameters": [
                {"name": "planta_id", "in": "path", "type": "integer", "required": True},
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {"$ref": "#/definitions/PlantaEntrada"},
                },
            ],
            "responses": {
                200: {"description": "Planta atualizada"},
                400: {"description": "Dados inválidos"},
                404: {"description": "Planta não encontrada"},
                500: {"$ref": "#/responses/ErroInterno"},
            },
        }
    )
    def atualizar(planta_id):
        dados = request.get_json(silent=True)
        erro = validar_dados(dados)
        if erro:
            return PlantaView.erro(erro, 400)

        try:
            if Planta.consultar_por_id(planta_id) is None:
                return PlantaView.erro("Planta não encontrada.", 404)
            Planta.atualizar(planta_id, dados)
            return PlantaView.atualizada(Planta.consultar_por_id(planta_id))
        except mysql.connector.Error:
            return PlantaView.erro("Não foi possível atualizar a planta.", 500)

    @staticmethod
    @plantas_bp.delete("/plantas/<int:planta_id>")
    @swag_from(
        {
            "tags": ["Plantas"],
            "summary": "Excluir uma planta",
            "parameters": [{"name": "planta_id", "in": "path", "type": "integer", "required": True}],
            "responses": {
                200: {"description": "Planta excluída"},
                404: {"description": "Planta não encontrada"},
                500: {"$ref": "#/responses/ErroInterno"},
            },
        }
    )
    def excluir(planta_id):
        try:
            if Planta.consultar_por_id(planta_id) is None:
                return PlantaView.erro("Planta não encontrada.", 404)
            Planta.excluir(planta_id)
            return PlantaView.excluida()
        except mysql.connector.Error:
            return PlantaView.erro("Não foi possível excluir a planta.", 500)

