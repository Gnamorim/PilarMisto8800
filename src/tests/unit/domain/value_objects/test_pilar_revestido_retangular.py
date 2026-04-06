import pytest
import numpy as np

from MY_PACKAGE.domain.value_objects.pilar_revestido_retangular import PilarRevestido
from MY_PACKAGE.domain.value_objects.ObjetoConcreto import ConcretoNormal
from MY_PACKAGE.domain.value_objects.ObjetoAco import AcoEstrutural, AcoArmadura


@pytest.fixture
def concreto():
    return ConcretoNormal(fck=40)


@pytest.fixture
def aco_estrutural():
    return AcoEstrutural(fy=345)


@pytest.fixture
def aco_armadura():
    return AcoArmadura(fy=500)


def criar_pilar_revestido(
    concreto,
    aco_estrutural,
    aco_armadura,
    **substituicoes,
):
    parametros = {
        "altura_concreto": 500,
        "largura_concreto": 400,
        "altura_perfil": 300,
        "largura_perfil": 200,
        "espessura_mesa": 12.5,
        "espessura_alma": 8,
        "cx": 100,
        "cy": 100,
        "comprimento_pilar_destravado": 3000,
        "material_aco_estrutural": aco_estrutural,
        "material_concreto": concreto,
        "material_armadura": aco_armadura,
        "diametro_armadura_longitudinal": 16,
        "numero_armadura_longitudinal": 4,
        "diametro_armadura_transversal": 8,
        "espacamento_armadura_transversal": 150,
        "cobrimento": 30,
    }
    parametros.update(substituicoes)
    return PilarRevestido(**parametros)


class TestValidacaoRevestidoRetangular:
    def test_criacao_com_armadura(self, concreto, aco_estrutural, aco_armadura):
        pilar = criar_pilar_revestido(concreto, aco_estrutural, aco_armadura)

        assert pilar.material_armadura is not None
        assert pilar.numero_armadura_longitudinal == 4
        assert pilar.altura_concreto == 500
        assert pilar.largura_concreto == 400
        assert pilar.cx == 100
        assert pilar.cy == 100

    @pytest.mark.parametrize(
        ("campo", "valor"),
        [
            ("altura_concreto", "500"),
            ("largura_concreto", "400"),
            ("altura_perfil", "300"),
            ("largura_perfil", "200"),
            ("espessura_mesa", "12.5"),
            ("espessura_alma", "8"),
        ],
    )
    def test_tipo_invalido_dimensoes_principais(
        self, concreto, aco_estrutural, aco_armadura, campo, valor
    ):
        with pytest.raises(TypeError):
            criar_pilar_revestido(
                concreto,
                aco_estrutural,
                aco_armadura,
                **{campo: valor},
            )

    def test_tipo_invalido_material_aco(self, concreto, aco_armadura):
        with pytest.raises(TypeError):
            criar_pilar_revestido(
                concreto,
                aco_estrutural="aco",
                aco_armadura=aco_armadura,
            )

    def test_tipo_invalido_material_concreto(self, aco_estrutural, aco_armadura):
        with pytest.raises(TypeError):
            criar_pilar_revestido(
                concreto="concreto",
                aco_estrutural=aco_estrutural,
                aco_armadura=aco_armadura,
            )

    def test_tipo_invalido_material_armadura(self, concreto, aco_estrutural):
        with pytest.raises(TypeError):
            criar_pilar_revestido(
                concreto,
                aco_estrutural,
                aco_armadura="armadura",
            )

    @pytest.mark.parametrize(
        ("campo", "valor"),
        [
            ("altura_concreto", 0),
            ("largura_concreto", 0),
            ("altura_perfil", 0),
            ("largura_perfil", 0),
            ("espessura_mesa", 0),
            ("espessura_alma", 0),
            ("altura_concreto", -500),
            ("largura_concreto", -400),
            ("altura_perfil", -300),
            ("largura_perfil", -200),
            ("espessura_mesa", -12.5),
            ("espessura_alma", -8),
        ],
    )
    def test_dimensoes_invalidas(
        self, concreto, aco_estrutural, aco_armadura, campo, valor
    ):
        with pytest.raises(ValueError):
            criar_pilar_revestido(
                concreto,
                aco_estrutural,
                aco_armadura,
                **{campo: valor},
            )

    def test_perfil_nao_pode_ser_maior_que_concreto(
        self, concreto, aco_estrutural, aco_armadura
    ):
        with pytest.raises(ValueError):
            criar_pilar_revestido(
                concreto,
                aco_estrutural,
                aco_armadura,
                altura_concreto=400,
                largura_concreto=300,
                altura_perfil=420,
                largura_perfil=200,
            )

        with pytest.raises(ValueError):
            criar_pilar_revestido(
                concreto,
                aco_estrutural,
                aco_armadura,
                altura_concreto=400,
                largura_concreto=300,
                altura_perfil=300,
                largura_perfil=320,
            )

    def test_armadura_invalida_valores(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            criar_pilar_revestido(
                concreto,
                aco_estrutural,
                aco_armadura,
                diametro_armadura_longitudinal=0,
            )

    def test_diametro_armadura_longitudinal_maior_que_50(
        self, concreto, aco_estrutural, aco_armadura
    ):
        with pytest.raises(ValueError):
            criar_pilar_revestido(
                concreto,
                aco_estrutural,
                aco_armadura,
                diametro_armadura_longitudinal=60,
            )

    def test_numero_armadura_maior_que_30(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            criar_pilar_revestido(
                concreto,
                aco_estrutural,
                aco_armadura,
                numero_armadura_longitudinal=31,
            )

    def test_diametro_armadura_transversal_maior_que_50(
        self, concreto, aco_estrutural, aco_armadura
    ):
        with pytest.raises(ValueError):
            criar_pilar_revestido(
                concreto,
                aco_estrutural,
                aco_armadura,
                diametro_armadura_transversal=60,
            )

    def test_espacamento_maior_que_1000(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            criar_pilar_revestido(
                concreto,
                aco_estrutural,
                aco_armadura,
                espacamento_armadura_transversal=1200,
            )

    def test_cobrimento_negativo(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            criar_pilar_revestido(
                concreto,
                aco_estrutural,
                aco_armadura,
                cobrimento=-10,
            )


class TestLimiteEscopoRevestidoRetangular:
    def test_cobrimento_do_perfil_menor_que_minimo_normativo(
        self, concreto, aco_estrutural, aco_armadura
    ):
        with pytest.raises(ValueError):
            criar_pilar_revestido(
                concreto,
                aco_estrutural,
                aco_armadura,
                altura_concreto=360,
                largura_concreto=260,
                altura_perfil=300,
                largura_perfil=200,
            )

    def test_area_aco_muito_pequena(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            criar_pilar_revestido(
                concreto,
                aco_estrutural,
                aco_armadura,
                espessura_mesa=0.5,
                espessura_alma=0.5,
            )


class TestGeometriaRevestidoRetangular:
    def test_area_aco(self, concreto, aco_estrutural, aco_armadura):
        pilar = criar_pilar_revestido(concreto, aco_estrutural, aco_armadura)

        area_esperada = (2 * (200 * 12.5)) + (8 * (300 - 2 * 12.5))

        assert np.isclose(pilar.area_aco, area_esperada)

    def test_area_armadura(self, concreto, aco_estrutural, aco_armadura):
        pilar = criar_pilar_revestido(concreto, aco_estrutural, aco_armadura)

        area_esperada = 4 * (np.pi * (16**2) / 4)

        assert np.isclose(pilar.area_armadura, area_esperada)

    def test_area_concreto(self, concreto, aco_estrutural, aco_armadura):
        pilar = criar_pilar_revestido(concreto, aco_estrutural, aco_armadura)

        area_aco = (2 * (200 * 12.5)) + (8 * (300 - 2 * 12.5))
        area_armadura = 4 * (np.pi * (16**2) / 4)
        area_esperada = (500 * 400) - area_aco - area_armadura

        assert np.isclose(pilar.area_concreto, area_esperada)

    def test_area_total_usa_api_publica(self, concreto, aco_estrutural, aco_armadura):
        pilar = criar_pilar_revestido(concreto, aco_estrutural, aco_armadura)

        area_esperada = pilar.area_aco + pilar.area_concreto + pilar.area_armadura

        assert np.isclose(pilar.area_total(), area_esperada)


class TestPropriedadesMecanicasRevestidoRetangular:
    def test_capacidades_axiais_plasticas(self, concreto, aco_estrutural, aco_armadura):
        pilar = criar_pilar_revestido(concreto, aco_estrutural, aco_armadura)

        area_aco = (2 * (200 * 12.5)) + (8 * (300 - 2 * 12.5))
        area_armadura = 4 * (np.pi * (16**2) / 4)
        area_concreto = (500 * 400) - area_aco - area_armadura
        alpha = min(1, (40 / concreto.fck) ** (1 / 3))
        fcd1 = concreto.fcd * 0.85 * alpha

        assert np.isclose(pilar.capacidade_axial_plastico_aco(), area_aco * aco_estrutural.fy)
        assert np.isclose(pilar.capacidade_axial_plastico_armadura(), area_armadura * aco_armadura.fy)
        assert np.isclose(pilar.capacidade_axial_plastico_concreto(), area_concreto * concreto.fck)
        assert np.isclose(
            pilar.capacidade_axial_plastico_design(),
            pilar.capacidade_axial_plastico_aco_design()
            + pilar.capacidade_axial_plastico_armadura_design()
            + pilar.capacidade_axial_plastico_concreto_design(),
        )
        assert np.isclose(
            pilar.capacidade_axial_plastico_armadura_design(),
            area_armadura * aco_armadura.resistencia_design,
        )
        assert np.isclose(
            pilar.capacidade_axial_plastico_concreto_design(),
            area_concreto * fcd1,
        )
