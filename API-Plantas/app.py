import os

from flasgger import Swagger
from flask import Flask

from Controller.PlantaController import plantas_bp


SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "API de Plantas",
        "description": "API REST em Python, MySQL e MVC para gerenciar plantas.",
        "version": "1.0.0",
    },
    "basePath": "/api",
    "schemes": ["http"],
    "definitions": {
        "PlantaEntrada": {
            "type": "object",
            "required": [
                "nome_popular",
                "nome_cientifico",
                "tipo",
                "necessidade_luz",
                "frequencia_rega_dias",
                "toxica",
            ],
            "properties": {
                "nome_popular": {"type": "string", "example": "Jiboia"},
                "nome_cientifico": {"type": "string", "example": "Epipremnum aureum"},
                "tipo": {"type": "string", "example": "Trepadeira"},
                "necessidade_luz": {"type": "string", "example": "Luz indireta"},
                "frequencia_rega_dias": {"type": "integer", "example": 7},
                "toxica": {"type": "boolean", "example": True},
            },
        },
        "Planta": {
            "allOf": [
                {"$ref": "#/definitions/PlantaEntrada"},
                {
                    "type": "object",
                    "properties": {"id": {"type": "integer", "example": 1}},
                },
            ]
        },
        "Erro": {
            "type": "object",
            "properties": {"erro": {"type": "string"}},
        },
    },
    "responses": {
        "ErroInterno": {
            "description": "Erro ao acessar o banco de dados",
            "schema": {"$ref": "#/definitions/Erro"},
        }
    },
}


def criar_app(configuracao=None):
    app = Flask(__name__)
    if configuracao:
        app.config.update(configuracao)

    app.register_blueprint(plantas_bp, url_prefix="/api")
    Swagger(
        app,
        template=SWAGGER_TEMPLATE,
        config={
            "headers": [],
            "specs": [
                {
                    "endpoint": "apispec_1",
                    "route": "/apispec_1.json",
                    "rule_filter": lambda rule: True,
                    "model_filter": lambda tag: True,
                }
            ],
            "static_url_path": "/flasgger_static",
            "swagger_ui": True,
            "specs_route": "/apidocs/",
        },
    )
    return app


app = criar_app()


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="127.0.0.1", port=5000, debug=debug)

