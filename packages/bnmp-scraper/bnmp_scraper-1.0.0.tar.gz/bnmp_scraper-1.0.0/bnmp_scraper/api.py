"""
Implementa as classes Estado, Municipio e OrgaoExpedidor
que são usadas pelo usuário para acessar os dados do
portal BNMP utilizando o Python.
"""

import requests
from .settings import NUM_MAP
import concurrent.futures
import warnings
from tqdm import tqdm
from .filtro import Filtro


class Estado(Filtro):
    """
    Classe usada para representar uma Unidade Federativa (UF)

    Attributes
    ----------
    _id : int
        id interno do BNMP que representa um determinado estado
    _init_info : dict
        informações básicas de uma página
    _totalElements : int
        número de mandados totais de um estado
    _munic_info : int
        dict que mapeia os nomes dos municípios de um estado ao id interno deles no BNMP
    _munic_objs : list
        lista de instâncias da classe Municipio com os municípios de um determinado estado

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    baixar_mandados(limit: int = 0, force: bool = False)
        Baixa todos os mandados do estado selecionado e armazena-os em self._mandados_list
    obter_municicipios(ids=False)
        Se ids=False(Default) retorna uma lista com os nomes de todos os municípios dessa uf(padrão)
        ou um dicionário mapeando cada cidade dessa UF ao seu respectivo id interno do BNMP.
    _baixar_municipios(force=False)
        A partir do id da de uma UF retorna um dict mapeando todos os municípios dessa UF aos seus ids.
    _gerar_municipios(force=False)
        Retorna uma lista de objetos Municipiocom todos os municípios de um Estado

    """
    def __init__(self, headers, id_estado: int):
        """
        Parameters
        ----------
        headers : dict
            Os headers para serem passados no networking
        id_estado : int
            Id interno do BNMP que representa um determinado estado
        """
        super().__init__(headers)
        self._id = id_estado
        self._init_info = self._obter_post_pag1(self._id)
        self._totalElements = self._init_info['totalElements']
        self._munic_info = {}
        self._munic_objs = []

    def baixar_mandados(self, limit: int = 0, force: bool = False) -> None: # TODO: Adicionar extend para quem não quer tanta informação
        """
        Baixa todos os mandados do estado selecionado
        e armazena-os em self._mandados_list

        Parameters
        ----------
        limit : int
            Limita os mandados baixados a até 2000 (dois mil) mandados.

        force : bool
            Se False(default) a função não realiza networking caso já tenha
            baixado os mandados. Se True baixa novamente os mandados e
            sobreescreve os mandados previamente baixados.

        Notes
        -----
        Para obter uma lista com as informações dos mandados, utilize .data
        após baixar os mandados.
        """
        if self._mandados_list and not force:
            warnings.warn(
                (
                    '\nVocê está baixando os mandados múltiplas vezes. O cache foi usado para evitar uma '
                    'sobrecarga de rede.\n\nSe você quiser mesmo baixar os mandados várias vezes, utilize '
                    '.baixar_mandados(force=True)'
                )
            )
            return None
        if limit:  # TODO: Alerta limite > 2000 vai ser ignorado
            mandados_parciais = self._obter_post_pag1(self._id, size=limit)['content']
            self._mandados_list = self._baixar_conteudo_completo_parallel(mandados_parciais)
            return None
        if self._totalElements <= 20000:
            if self._totalElements <= 10000:
                mandados_parciais = self._request_post_poucos_mandados(self._init_info, self._id)
            else:
                mandados_parciais = self._request_post_expandido(self._init_info, self._id)
            self._mandados_list = self._baixar_conteudo_completo_parallel(mandados_parciais)
        else:
            municips = self._gerar_municipios()
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=32)
            list(tqdm(executor.map(Municipio.baixar_mandados, municips), total=len(municips)))
            self._mandados_list = [item for munic in municips for item in munic.obter_mandados()]
        print(f"Recuperados {len(self._mandados_list)}/{self._totalElements} mandados")

    def obter_municicipios(self, ids=False) -> [list, dict]:
        """
        Se ids=False(Default) retorna uma lista com os nomes de
        todos os municípios dessa uf. Se ids=True retorna um
        dicionário mapeando cada cidade dessa UF ao seu
        respectivo id interno do BNMP.
        """
        if not ids:
            return list(self._baixar_municipios().keys())
        else:
            return self._baixar_municipios()

    def _baixar_municipios(self, force: bool = False) -> dict:
        """
        A partir do id da de uma UF retorna um
        dict mapeando todos os municípios dessa
        UF aos seus ids.
        """
        if self._munic_info and not force:
            return self._munic_info
        response_munic = requests.get(
            url=f'https://portalbnmp.cnj.jus.br/scaservice/api/municipios/por-uf/{self._id}',
            headers=self._headers
        )
        munic_list = response_munic.json()
        self._munic_info = {munic['nome']: munic['id'] for munic in munic_list}
        return self._munic_info.copy()

    def _gerar_municipios(self, force: bool = False) -> list:
        """
        Retorna uma lista de objetos Municipio
        com todos os municípios de um Estado.
        """
        if self._munic_objs and not force:
            return self._munic_objs
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=32)
        munics_ids = list(self._baixar_municipios().values())  # Pega os ids dos municípios
        munic = list(executor.map(
            lambda munic_id: Municipio(self._headers, self._id, munic_id), munics_ids
        ))  # Cria as instâncias
        self._munic_objs = [m for m in munic if len(m) > 0]
        return self._munic_objs  # retorna somente os municípios que tem mandados

    def _get_sigla(self):
        return NUM_MAP[self._id]

    def __add__(self, val):
        if not isinstance(val, (Estado, Municipio, OrgaoExpedidor)):
            raise TypeError("Você só pode somar elementos das classes Estado, Municipio ou OrgaoExpedidor")
        return self.data + val.data

    sigla = property(_get_sigla, None)  # Sinônimo de nome
    nome = property(_get_sigla, None)


class Municipio(Filtro):
    """
    Classe usada para representar um município
    """
    def __init__(self, headers, id_estado: int, id_munic: int, nome: str = "Não especificado"):
        super().__init__(headers)
        self._id_estado = id_estado
        self._id = id_munic
        self._nome = nome
        self._init_info = self._obter_post_pag1(self._id_estado, self._id)
        self._totalElements = self._init_info['totalElements']
        self._mandados_list = []
        self._orgaos_info = {}
        self._orgaos_objs = []

    def baixar_mandados(self, limit: int = 0, force: bool = False) -> None: # TODO: Adicionar extend para quem não quer tanta informação
        """
        Baixa todos os mandados do município selecionado
        e armazena-os em self._mandados_list

        Parameters
        ----------
        limit : int
            Limita os mandados baixados a até 2000 (dois mil) mandados.

        force : bool
            Se False(default) a função não realiza networking caso já tenha
            baixado os mandados. Se True baixa novamente os mandados e
            sobreescreve os mandados previamente baixados.

        Notes
        -----
        Para obter uma lista com as informações dos mandados, utilize .data
        após baixar os mandados.
        """
        if self._mandados_list and not force:
            warnings.warn(
                (
                    '\nVocê está baixando os mandados múltiplas vezes. O cache foi usado para evitar uma '
                    'sobrecarga de rede.\n\nSe você quiser mesmo baixar os mandados várias vezes, utilize '
                    '.baixar_mandados(force=True)'
                )
            )
            return None
        if limit:
            mandados_parciais = self._obter_post_pag1(self._id_estado, self._id, size=limit)['content']
            self._mandados_list = self._baixar_conteudo_completo_parallel(mandados_parciais)
            return None
        if self._totalElements <= 20000:
            if self._totalElements <= 10000:
                mandados_parciais = self._request_post_poucos_mandados(self._init_info, self._id_estado, self._id)
            else:
                mandados_parciais = self._request_post_expandido(self._init_info, self._id_estado, self._id)
            self._mandados_list = self._baixar_conteudo_completo_parallel(mandados_parciais)
        else:
            orgaos = self._gerar_orgaos()
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=32)
            list(tqdm(executor.map(OrgaoExpedidor.baixar_mandados, orgaos), total=len(orgaos)))
            self._mandados_list = [item for orgao in orgaos for item in orgao.obter_mandados()]
        # print(f"Recuperados {len(self._mandados_list)}/{self._totalElements} mandados")

    def _baixar_orgaos(self, force: bool = False) -> dict:
        """
        A partir do id da de um município retorna
        um dict mapeando todos os Órgãos Expeditores
        desse município aos seus ids.
        """
        if self._orgaos_info and not force:
            return self._orgaos_info
        response_org = requests.get(
            url=f'https://portalbnmp.cnj.jus.br/bnmpportal/api/pesquisa-pecas/orgaos/municipio/{self._id}',
            headers=self._headers
        )
        org_list = response_org.json()
        self._orgaos_info = {org['nome']: org['id'] for org in org_list}
        return self._orgaos_info.copy()

    def obter_orgaos(self) -> list:
        """
        Retorna uma lista com os nomes de todos os Órgãos Expedidores dessa uf.
        """
        return list(self._baixar_orgaos().keys())

    def _gerar_orgaos(self, force: bool = False) -> list:
        """
        Retorna uma lista de objetos Municipio
        com todos os municípios de um Estado.
        """
        if self._orgaos_objs and not force:
            return self._orgaos_objs
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=32)
        orgaos_ids = list(self._baixar_orgaos().values())  # Pega os ids dos órgãos expedidores
        org = list(executor.map(
            lambda org_id: OrgaoExpedidor(self._headers, self._id_estado, self._id, org_id), orgaos_ids
        ))  # Cria as instâncias
        return [o for o in org if len(o) > 0]  # retorna somente os órgãos que tem mandados

    def _get_nome(self):
        return self._nome

    def __add__(self, val):
        if not isinstance(val, (Estado, Municipio, OrgaoExpedidor)):
            raise TypeError("Você só pode somar elementos das classes Estado, Municipio ou OrgaoExpedidor")
        return self.data + val.data

    nome = property(_get_nome, None)


class OrgaoExpedidor(Filtro):
    def __init__(self, headers, id_estado, id_munic, id_orgao, nome: str = "Não especificado"):
        super().__init__(headers)
        self._id_estado = id_estado
        self._id_munic = id_munic
        self._id = id_orgao
        self._nome = nome
        self._init_info = self._obter_post_pag1(self._id_estado, self._id_munic, self._id)
        self._totalElements = self._init_info['totalElements']
        self._mandados_list = []

    def baixar_mandados(self, force: bool = False) -> None: # TODO: Adicionar extend para quem não quer tanta informação
        if self._mandados_list and not force:
            warnings.warn(
                (
                    '\nVocê está baixando os mandados múltiplas vezes. O cache foi usado para evitar uma '
                    'sobrecarga de rede.\n\nSe você quiser mesmo baixar os mandados várias vezes, utilize '
                    '.baixar_mandados(force=True)'
                )
            )
            return None
        if self._totalElements <= 20000:
            if self._totalElements <= 10000:
                mandados_parciais = self._request_post_poucos_mandados(
                    self._init_info, self._id_estado, self._id_munic, self._id
                )
            else:
                mandados_parciais = self._request_post_expandido(
                    self._init_info, self._id_estado, self._id_munic, self._id
                )
            self._mandados_list = self._baixar_conteudo_completo_parallel(mandados_parciais)
        else:
            mandados_parciais = self._request_post_forcabruta(self._id_estado, self._id_munic, self._id)
            self._mandados_list = self._baixar_conteudo_completo_parallel(mandados_parciais)
        # print(f"Recuperados {len(self._mandados_list)}/{self._totalElements} mandados")

    def __add__(self, val):
        if not isinstance(val, (Estado, Municipio, OrgaoExpedidor)):
            raise TypeError("Você só pode somar elementos das classes Estado, Municipio ou OrgaoExpedidor")
        return self.data + val.data

    def _get_nome(self):
        return self._nome

    nome = property(_get_nome, None)
