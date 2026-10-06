from flask import jsonify


class PlantaView:
    """Padroniza as respostas JSON enviadas pela API."""

    @staticmethod
    def _serializar(planta):
        if planta is None:
            return None
        resultado = dict(planta)
        resultado["toxica"] = bool(resultado["toxica"])
        return resultado

    @staticmethod
    def listar(plantas):
        return jsonify([PlantaView._serializar(planta) for planta in plantas]), 200

    @staticmethod
    def exibir(planta):
        return jsonify(PlantaView._serializar(planta)), 200

    @staticmethod
    def criada(planta):
        return jsonify(
            {
                "mensagem": "Planta cadastrada com sucesso.",
                "planta": PlantaView._serializar(planta),
            }
        ), 201

    @staticmethod
    def atualizada(planta):
        return jsonify(
            {
                "mensagem": "Planta atualizada com sucesso.",
                "planta": PlantaView._serializar(planta),
            }
        ), 200

    @staticmethod
    def excluida():
        return jsonify({"mensagem": "Planta excluída com sucesso."}), 200

    @staticmethod
    def erro(mensagem, status=400):
        return jsonify({"erro": mensagem}), status
