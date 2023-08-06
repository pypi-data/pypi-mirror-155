"""
Implementa a classe Filtro que fornece vários métodos
de networking com o site BNMP e é a classe base das
classes Estado, Municipio e OrgaoExpedidor que são
implementadas em api.py
"""
from .errors import MandadosNotFoundError
import requests
import concurrent.futures
from itertools import repeat
from .settings import PARAMS_FORCA_BRUTA
from .utils import obter_data_post
from tqdm import tqdm
import warnings
import json


class Filtro:
    def __init__(self, headers):
        self._mandados_list = []
        self._headers = headers
        self._totalElements = None

    def to_json(self, caminho: str = '', modo='w'):
        # Error checking
        if modo not in ('a', 'w', 'x'):
            raise ValueError("modo deve ser igual a 'a', 'w' ou 'x'.")
        if not (isinstance(caminho, str) or caminho is None):
            raise ValueError('caminho precisa ser uma str ou None')

        if caminho:
            with open(f'{caminho}', modo) as file:
                json.dump(self.data, file)
        else:
            with open(f'{self.nome}.json', modo) as file:
                json.dump(self.data, file)

    def _obter_mandados(self) -> list:
        """
        Retorna uma cópia dos mandados baixados
        """
        if not self._mandados_list:
            raise MandadosNotFoundError("Você ainda não baixou os mandados. Utilize .baixar_mandados() para baixa-los")
        return self._mandados_list.copy()

    # def __add__(self, val):
    #     if not isinstance(val, (Estado, Municipio, OrgaoExpedidor)):
    #         raise TypeError("Você só pode somar elementos das classes Estado, Municipio ou OrgaoExpedidor")
    #     return self.obter_mandados() + val.obter_mandados()

    def _request_post(self, params, data):
        """Faz uma requisição do tipo POST e retorna
        um dict se ela for bem sucedida e um NoneType
        caso contrário"""
        response = requests.post(
            url='https://portalbnmp.cnj.jus.br/bnmpportal/api/pesquisa-pecas/filter',
            headers=self._headers,
            params=params,
            data=data
        )
        if response.ok:
            return response.json()
        else:
            responsetxt = response.json().get('detail', '')
            warnings.warn(
                f"ERROR! POST request não bem sucedida.\nStatus code {response.status_code}: '{responsetxt}'"
            )

    def _obter_post_pag1(self, id_estado: int, id_municipio: int = 0, id_orgao: int = 0, size: int = 10) -> dict:
        """Faz um POST request da primeira página para
        obter até 2.000 elementos. Retorna um dict
        com o total de mandados daquele id."""
        params = (
            ('page', '0'),
            ('size', f'{size}'),
            ('sort', 'dataExpedicao,DESC'),
        )

        data = obter_data_post(id_estado, id_municipio, id_orgao)

        raw_data = self._request_post(params, data)
        return raw_data

    def _request_post_poucos_mandados(self, response_pag1: dict, id_estado: int, id_municipio: int = 0,
                                      id_orgao: int = 0) -> list:
        """
        Obtém até 10.000 linhas de dados.
        Retorna uma lista de dicts
        :param response_pag1: 'raw_data': dict
        :param id_estado: id que pertence ao intervalo [1,27].
        :param id_municipio: id interno
        :param id_orgao: id interno
        :return: list: lista de dicionários de mandados
        """
        data = obter_data_post(id_estado, id_municipio, id_orgao)
        tot_elements = response_pag1.get('totalElements')
        tot_pages = tot_elements // 2000 if tot_elements % 2000 == 0 else tot_elements // 2000 + 1
        params = tuple((('page', str(x)), ('size', '2000'), ('sort', 'dataExpedicao,DESC')) for x in range(0, tot_pages))
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            novos_mandados = list(executor.map(self._request_post, params, repeat(data)))
        return [x for sublist in novos_mandados for x in sublist['content']]  # List unpacking

    def _request_post_expandido(self, response_pag1: dict, id_estado: int, id_municipio: int = 0,
                                id_orgao: int = 0) -> list:
        """
        Aproveita-se da ordenação para extrapolar o
        limite de 10.000 linhas e alcaçar até o dobro disso.
        Retorna uma lista de dicts
        """
        data = obter_data_post(id_estado, id_municipio, id_orgao)
        tot_elements = response_pag1['totalElements']
        params = tuple((('page', str(x)), ('size', '2000'), ('sort', 'dataExpedicao,DESC')) for x in range(0, 5))
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            novos_mandados = list(executor.map(self._request_post, params, repeat(data)))
        all_mandados = [x for sublist in novos_mandados for x in sublist['content']]  # List unpacking
        paginas_restantes = (tot_elements - 10000) // 2000
        if paginas_restantes >= 1:
            params = tuple(
                (('page', str(x)), ('size', '2000'),
                 ('sort', 'dataExpedicao,ASC')) for x in range(0, int(paginas_restantes)))
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                novos_mandados = executor.map(self._request_post, params, repeat(data))
            for e in [x['content'] for x in novos_mandados]:
                all_mandados.extend(e)
        params = (('page', str(paginas_restantes)), ('size', '2000'), ('sort', 'dataExpedicao,ASC'))
        ultima_pag = self._request_post(params, data)
        all_mandados.extend([x for x in ultima_pag['content'] if x not in all_mandados])
        return all_mandados

    def _request_post_forcabruta(self, id_estado: int, id_municipio: int, id_orgao: int) -> list:
        """
        Aplica todas as ordenações disponíveis para
        obter o maior número de mandados possíveis,
        mesmo sem conseguir acessar todas as páginas
        do Banco de Dados.
        Retorna uma lista com todos os mandados adquiridos.
        """
        data = '{"buscaOrgaoRecursivo":false,"orgaoExpeditor":{"id":' + str(id_orgao) + '},"idEstado":' + str(
            id_estado) + ',"idMunicipio":' + str(id_municipio) + '}'

        all_mandados = list()

        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            novos_mandados = list(
                tqdm(executor.map(self._request_post, PARAMS_FORCA_BRUTA, repeat(data)), total=len(PARAMS_FORCA_BRUTA)))
        for lista_mandados in [x['content'] for x in novos_mandados if x]:
            all_mandados.extend([mandado for mandado in lista_mandados if mandado not in all_mandados])
        return all_mandados

    def _pega_conteudo_completo(self, linha: dict):
        """
        "Entra" em cada um dos mandados com o
        método GET para pegar mais informações
        e retorna-as como um dict
        """
        if not isinstance(linha, dict):
            warnings.warn(f"ERROR! Mandado should be a dict, not a {type(linha)}")
            return None
        # HEADERS['user-agent'] = ua.random
        id_mandado = linha.get("id")
        id_tipo_peca = linha.get("idTipoPeca")
        if id_tipo_peca is None:
            id_tipo_peca = linha['tipoPeca'].get('id')

        response = requests.get(
            url=f'https://portalbnmp.cnj.jus.br/bnmpportal/api/certidaos/{id_mandado}/{id_tipo_peca}',
            headers=self._headers
        )
        if response.ok:
            return response.json()
            # with open(f"jsons/{response_dict['id']}.json", 'wb') as outf:
            #     outf.write(response.content)
        else:
            responsetxt = response.json().get('detail', '')
            warnings.warn(
                f"ERROR! GET request não bem sucedida.\nStatus code {response.status_code}: '{responsetxt}'"
            )

    def _baixar_conteudo_completo_parallel(self, lista_mandados: list) -> list:
        """
        Dada uma lista de mandados com informações parciais,
        utiliza concorrência para fazer requisições do tipo
        GET e assim extrair mais informações de maneira mais
        eficiente.

        Retorna uma lista de dicts de mandados com as informações expandidas.
        """
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=32)
        result = list(executor.map(self._pega_conteudo_completo, lista_mandados))
        return [mandado for mandado in result if mandado is not None]

    def __len__(self):
        return self._totalElements

    @property
    def nome(self):
        raise NotImplementedError

    data = property(_obter_mandados, None)
