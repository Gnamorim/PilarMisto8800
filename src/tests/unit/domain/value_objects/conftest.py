import pytest

from MY_PACKAGE.domain.value_objects.ObjetoConcreto import ConcretoNormal
from MY_PACKAGE.domain.value_objects.ObjetoAco import AcoEstrutural, AcoArmadura
from MY_PACKAGE.domain.value_objects.pilar_misto_retangular import (
    PilarRetangularPreenchido,
)


@pytest.fixture
def concreto():
    return ConcretoNormal(fck=40)


@pytest.fixture
def aco_estrutural():
    return AcoEstrutural(fy=345)


@pytest.fixture
def aco_armadura():
    return AcoArmadura(fy=500)


@pytest.fixture
def criar_pilar_retangular_preenchido():
    def _criar_pilar_retangular_preenchido(
        concreto,
        aco_estrutural,
        aco_armadura=None,
        **substituicoes,
    ):
        parametros = {
            "altura_tubo": 300,
            "largura_tubo": 200,
            "espessura_tubo": 10,
            "comprimento_pilar_destravado": 3000,
            "material_aco_estrutural": aco_estrutural,
            "material_concreto": concreto,
            "material_armadura": aco_armadura,
            "diametro_armadura_longitudinal": 0,
            "numero_armadura_longitudinal": 0,
            "diametro_armadura_transversal": 0,
            "espacamento_armadura_transversal": 0,
            "cobrimento": 0,
        }
        parametros.update(substituicoes)
        return PilarRetangularPreenchido(**parametros)

    return _criar_pilar_retangular_preenchido
