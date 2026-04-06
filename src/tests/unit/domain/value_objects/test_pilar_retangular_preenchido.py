import pytest
import numpy as np

from MY_PACKAGE.domain.value_objects.pilar_misto_retangular import PilarRetangularPreenchido
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


def criar_pilar_retangular_preenchido(
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


class TestValidacaoRetangularPreenchido:
    def test_criacao_sem_armadura(self, concreto, aco_estrutural):
        pilar = criar_pilar_retangular_preenchido(concreto, aco_estrutural)

        assert pilar.material_armadura is None
        assert pilar.numero_armadura_longitudinal == 0
        assert pilar.altura_tubo == 300
        assert pilar.largura_tubo == 200

    def test_criacao_com_armadura(self, concreto, aco_estrutural, aco_armadura):
        pilar = criar_pilar_retangular_preenchido(
            concreto,
            aco_estrutural,
            aco_armadura=aco_armadura,
            diametro_armadura_longitudinal=16,
            numero_armadura_longitudinal=4,
            diametro_armadura_transversal=8,
            espacamento_armadura_transversal=150,
            cobrimento=30,
        )

        assert pilar.material_armadura is not None
        assert pilar.numero_armadura_longitudinal == 4
        assert pilar.diametro_armadura_longitudinal == 16

    def test_tipo_invalido_altura(self, concreto, aco_estrutural):
        with pytest.raises(TypeError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                altura_tubo="300",
            )

    def test_tipo_invalido_largura(self, concreto, aco_estrutural):
        with pytest.raises(TypeError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                largura_tubo="200",
            )

    def test_tipo_invalido_espessura(self, concreto, aco_estrutural):
        with pytest.raises(TypeError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                espessura_tubo="10",
            )

    def test_tipo_bool_invalido(self, concreto, aco_estrutural):
        with pytest.raises(TypeError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                altura_tubo=True,
            )

    def test_tipo_invalido_material(self, concreto):
        with pytest.raises(TypeError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural="aco",
            )

    @pytest.mark.parametrize(
        ("campo", "valor"),
        [
            ("altura_tubo", 0),
            ("altura_tubo", -300),
            ("largura_tubo", 0),
            ("largura_tubo", -200),
            ("espessura_tubo", 0),
            ("espessura_tubo", -10),
        ],
    )
    def test_dimensoes_invalidas(self, concreto, aco_estrutural, campo, valor):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                **{campo: valor},
            )

    def test_espessura_fisicamente_invalida(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                altura_tubo=300,
                largura_tubo=200,
                espessura_tubo=120,
            )

    def test_armadura_invalida_valores(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                aco_armadura=aco_armadura,
                diametro_armadura_longitudinal=0,
                numero_armadura_longitudinal=4,
                diametro_armadura_transversal=8,
                espacamento_armadura_transversal=150,
                cobrimento=30,
            )

    def test_sem_armadura_com_valores_nao_zero(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                diametro_armadura_longitudinal=16,
            )

    def test_diametro_armadura_longitudinal_maior_que_50(
        self, concreto, aco_estrutural, aco_armadura
    ):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                aco_armadura=aco_armadura,
                diametro_armadura_longitudinal=60,
                numero_armadura_longitudinal=4,
                diametro_armadura_transversal=8,
                espacamento_armadura_transversal=150,
                cobrimento=30,
            )

    def test_diametro_armadura_longitudinal_muito_pequeno(
        self, concreto, aco_estrutural, aco_armadura
    ):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                aco_armadura=aco_armadura,
                diametro_armadura_longitudinal=4,
                numero_armadura_longitudinal=4,
                diametro_armadura_transversal=8,
                espacamento_armadura_transversal=150,
                cobrimento=30,
            )

    def test_numero_armadura_maior_que_30(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                aco_armadura=aco_armadura,
                diametro_armadura_longitudinal=16,
                numero_armadura_longitudinal=31,
                diametro_armadura_transversal=8,
                espacamento_armadura_transversal=150,
                cobrimento=30,
            )

    def test_diametro_armadura_transversal_maior_que_50(
        self, concreto, aco_estrutural, aco_armadura
    ):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                aco_armadura=aco_armadura,
                diametro_armadura_longitudinal=16,
                numero_armadura_longitudinal=4,
                diametro_armadura_transversal=60,
                espacamento_armadura_transversal=150,
                cobrimento=30,
            )

    def test_diametro_armadura_transversal_muito_pequeno(
        self, concreto, aco_estrutural, aco_armadura
    ):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                aco_armadura=aco_armadura,
                diametro_armadura_longitudinal=16,
                numero_armadura_longitudinal=4,
                diametro_armadura_transversal=4,
                espacamento_armadura_transversal=150,
                cobrimento=30,
            )

    def test_espacamento_maior_que_1000(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                aco_armadura=aco_armadura,
                diametro_armadura_longitudinal=16,
                numero_armadura_longitudinal=4,
                diametro_armadura_transversal=8,
                espacamento_armadura_transversal=1500,
                cobrimento=30,
            )

    def test_cobrimento_negativo(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                aco_armadura=aco_armadura,
                diametro_armadura_longitudinal=16,
                numero_armadura_longitudinal=4,
                diametro_armadura_transversal=8,
                espacamento_armadura_transversal=150,
                cobrimento=-10,
            )


class TestLimiteEscopoRetangularPreenchido:
    def test_razao_largura_altura_muito_pequena(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                altura_tubo=1000,
                largura_tubo=100,
                espessura_tubo=12,
            )

    def test_razao_largura_altura_muito_grande(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                altura_tubo=100,
                largura_tubo=1000,
                espessura_tubo=12,
            )

    def test_area_aco_muito_pequena(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                altura_tubo=300,
                largura_tubo=200,
                espessura_tubo=0.1,
            )

    def test_fator_contribuicao_muito_baixo(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                altura_tubo=300,
                largura_tubo=200,
                espessura_tubo=1,
            )

    def test_fator_contribuicao_muito_alto(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                altura_tubo=300,
                largura_tubo=200,
                espessura_tubo=45,
            )

    def test_esbeltez_fora_do_escopo(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                altura_tubo=600,
                largura_tubo=300,
                espessura_tubo=1,
                comprimento_pilar_destravado=12000,
            )


class TestGeometriaRetangularPreenchido:
    def test_area_aco(self, concreto, aco_estrutural):
        pilar = criar_pilar_retangular_preenchido(concreto, aco_estrutural)

        area_esperada = (300 * 200) - ((200 - 2 * 10) * (300 - 2 * 10))

        assert np.isclose(pilar.area_aco, area_esperada)

    def test_area_concreto(self, concreto, aco_estrutural, aco_armadura):
        pilar_sem_armadura = criar_pilar_retangular_preenchido(concreto, aco_estrutural)
        pilar_com_armadura = criar_pilar_retangular_preenchido(
            concreto,
            aco_estrutural,
            aco_armadura=aco_armadura,
            diametro_armadura_longitudinal=16,
            numero_armadura_longitudinal=4,
            diametro_armadura_transversal=8,
            espacamento_armadura_transversal=150,
            cobrimento=30,
        )

        area_interna = (200 - 2 * 10) * (300 - 2 * 10)
        area_armadura = 4 * (np.pi * (16**2) / 4)

        assert np.isclose(pilar_sem_armadura.area_concreto, area_interna)
        assert np.isclose(pilar_com_armadura.area_concreto, area_interna - area_armadura)

    def test_area_armadura(self, concreto, aco_estrutural, aco_armadura):
        pilar = criar_pilar_retangular_preenchido(
            concreto,
            aco_estrutural,
            aco_armadura=aco_armadura,
            diametro_armadura_longitudinal=16,
            numero_armadura_longitudinal=4,
            diametro_armadura_transversal=8,
            espacamento_armadura_transversal=150,
            cobrimento=30,
        )

        area_esperada = 4 * (np.pi * (16**2) / 4)

        assert np.isclose(pilar.area_armadura, area_esperada)

    def test_area_total_usa_api_publica(self, concreto, aco_estrutural):
        pilar = criar_pilar_retangular_preenchido(concreto, aco_estrutural)

        area_esperada = pilar.area_aco + pilar.area_concreto + pilar.area_armadura

        assert np.isclose(pilar.area_total(), area_esperada)


class TestPropriedadesMecanicasRetangularPreenchido:
    def test_capacidades_axiais_plasticas_sem_armadura(self, concreto, aco_estrutural):
        pilar = criar_pilar_retangular_preenchido(concreto, aco_estrutural)

        area_aco = (300 * 200) - ((200 - 2 * 10) * (300 - 2 * 10))
        area_concreto = (200 - 2 * 10) * (300 - 2 * 10)
        fcd1 = concreto.fcd * 0.85

        assert np.isclose(pilar.capacidade_axial_plastico_aco(), area_aco * aco_estrutural.fy)
        assert np.isclose(pilar.capacidade_axial_plastico_armadura(), 0.0)
        assert np.isclose(pilar.capacidade_axial_plastico_concreto(), area_concreto * concreto.fck)
        assert np.isclose(
            pilar.capacidade_axial_plastico(),
            pilar.capacidade_axial_plastico_aco()
            + pilar.capacidade_axial_plastico_armadura()
            + pilar.capacidade_axial_plastico_concreto(),
        )
        assert np.isclose(
            pilar.capacidade_axial_plastico_design(),
            pilar.capacidade_axial_plastico_aco_design()
            + pilar.capacidade_axial_plastico_armadura_design()
            + pilar.capacidade_axial_plastico_concreto_design(),
        )
        assert np.isclose(
            pilar.capacidade_axial_plastico_concreto_design(),
            area_concreto * fcd1,
        )

    def test_capacidades_axiais_plasticas_com_armadura(
        self, concreto, aco_estrutural, aco_armadura
    ):
        pilar = criar_pilar_retangular_preenchido(
            concreto,
            aco_estrutural,
            aco_armadura=aco_armadura,
            diametro_armadura_longitudinal=16,
            numero_armadura_longitudinal=4,
            diametro_armadura_transversal=8,
            espacamento_armadura_transversal=150,
            cobrimento=30,
        )

        area_armadura = 4 * (np.pi * (16**2) / 4)
        capacidade_armadura_esperada = (
            area_armadura
            * concreto.fck
            * (aco_armadura.modulo_elasticidade / concreto.modulo_elasticidade_inicial)
        )
        capacidade_armadura_design_esperada = (
            area_armadura
            * (concreto.fcd * 0.85)
            * (aco_armadura.modulo_elasticidade / concreto.modulo_elasticidade_inicial)
        )

        assert np.isclose(pilar.capacidade_axial_plastico_armadura(), capacidade_armadura_esperada)
        assert np.isclose(
            pilar.capacidade_axial_plastico_armadura_design(),
            capacidade_armadura_design_esperada,
        )
