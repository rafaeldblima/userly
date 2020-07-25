import re
from collections import namedtuple

Endereco = namedtuple('Endereco', ['logradouro', 'bairro', 'cidade', 'uf', 'ibge', 'complemento'])

import json
import requests


class ViaCEP:

    def __init__(self, cep):
        self.cep = cep

    def getDadosCEP(self):
        url_api = ('http://www.viacep.com.br/ws/%s/json' % self.cep)
        req = requests.get(url_api)
        if req.status_code == 200:
            dados_json = json.loads(req.text)
            return dados_json

    def __validade_cep(self):
        self.cep = re.sub("[^0-9]", "", self.cep)

    def buscar_cep(self) -> Endereco:
        self.__validade_cep()
        dados_json = self.getDadosCEP()
        resp = {
            'logradouro': dados_json.get('logradouro'),
            'bairro': dados_json.get('bairro'),
            'cidade': dados_json.get('localidade'),
            'uf': dados_json.get('uf'),
            'ibge': dados_json.get('ibge'),
            'complemento': dados_json.get('complemento'),
        }
        endereco = Endereco(**resp)
        return endereco
