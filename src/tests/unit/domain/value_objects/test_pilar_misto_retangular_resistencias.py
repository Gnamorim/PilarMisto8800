import numpy as np
import pytest

from MY_PACKAGE.domain.value_objects._classe_secao import Secao
from MY_PACKAGE.domain.value_objects.pilar_misto_retangular import (
    PilarRetangularPreenchido,
)


class TestPropriedadesMecanicasRetangularPreenchido:
    def test_capacidades_axiais_plasticas_sem_armadura(
        self, concreto, aco_estrutural, criar_pilar_retangular_preenchido
    ):
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
        self, concreto, aco_estrutural, aco_armadura, criar_pilar_retangular_preenchido
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

    def test_esbeltezes_flexao_compactas_por_padrao(
        self, concreto, aco_estrutural, criar_pilar_retangular_preenchido
    ):
        pilar = criar_pilar_retangular_preenchido(concreto, aco_estrutural)

        assert pilar.esbeltez_flexao_XX == Secao.COMPACTO
        assert pilar.esbeltez_flexao_YY == Secao.COMPACTO
        assert pilar.esbeltez_flexao == Secao.COMPACTO

    def test_esbeltez_flexao_global_nao_compacta_usando_pior_caso(
        self,
        concreto,
        aco_estrutural,
        aco_armadura,
        criar_pilar_retangular_preenchido,
    ):
        pilar = criar_pilar_retangular_preenchido(
            concreto,
            aco_estrutural,
            aco_armadura=aco_armadura,
            largura_tubo=600,
            espessura_tubo=10,
            diametro_armadura_longitudinal=16,
            numero_armadura_longitudinal=4,
            diametro_armadura_transversal=8,
            espacamento_armadura_transversal=150,
            cobrimento=30,
        )

        assert pilar.esbeltez_flexao_XX == Secao.COMPACTO
        assert pilar.esbeltez_flexao_YY == Secao.NAO_COMPACTO
        assert pilar.esbeltez_flexao == Secao.NAO_COMPACTO

    def test_esbeltez_flexao_global_pega_pior_caso_esbelto(
        self,
        concreto,
        aco_estrutural,
        aco_armadura,
        criar_pilar_retangular_preenchido,
    ):
        pilar = criar_pilar_retangular_preenchido(
            concreto,
            aco_estrutural,
            aco_armadura=aco_armadura,
            altura_tubo=200,
            largura_tubo=1000,
            espessura_tubo=10,
            diametro_armadura_longitudinal=16,
            numero_armadura_longitudinal=4,
            diametro_armadura_transversal=8,
            espacamento_armadura_transversal=150,
            cobrimento=30,
        )

        assert pilar.esbeltez_flexao_XX == Secao.NAO_COMPACTO
        assert pilar.esbeltez_flexao_YY == Secao.ESBELTO
        assert pilar.esbeltez_flexao == Secao.ESBELTO

    def test_resistencias_flexao_secao_compacta_retornam_valores_esperados(
        self, concreto, aco_estrutural, criar_pilar_retangular_preenchido
    ):
        pilar = criar_pilar_retangular_preenchido(concreto, aco_estrutural)

        assert (
            pilar.capacidade_flexao_resistente_secao_nominal_xx
            == pilar.momento_resistente_plastico_total_xx
        )
        assert (
            pilar.capacidade_flexao_resistente_secao_nominal_yy
            == pilar.momento_resistente_plastico_total_yy
        )
        assert (
            pilar.capacidade_flexao_resistente_secao_design_xx
            == pilar.momento_resistente_plastico_total_design_xx
        )
        assert (
            pilar.capacidade_flexao_resistente_secao_design_yy
            == pilar.momento_resistente_plastico_total_design_yy
        )

    @pytest.mark.parametrize(
        ("eixo", "resistencia_flexao"),
        [
            ("esbeltez_flexao_XX", "capacidade_flexao_resistente_secao_nominal_xx"),
            ("esbeltez_flexao_YY", "capacidade_flexao_resistente_secao_nominal_yy"),
            ("esbeltez_flexao_XX", "capacidade_flexao_resistente_secao_design_xx"),
            ("esbeltez_flexao_YY", "capacidade_flexao_resistente_secao_design_yy"),
        ],
    )
    def test_resistencias_flexao_secao_nao_compacta_lancam_not_implemented(
        self,
        monkeypatch,
        concreto,
        aco_estrutural,
        criar_pilar_retangular_preenchido,
        eixo,
        resistencia_flexao,
    ):
        monkeypatch.setattr(
            PilarRetangularPreenchido,
            eixo,
            property(lambda self: Secao.NAO_COMPACTO),
        )
        pilar = criar_pilar_retangular_preenchido(concreto, aco_estrutural)

        with pytest.raises(NotImplementedError):
            getattr(pilar, resistencia_flexao)

    @pytest.mark.parametrize(
        ("eixo", "resistencia_flexao"),
        [
            ("esbeltez_flexao_XX", "capacidade_flexao_resistente_secao_nominal_xx"),
            ("esbeltez_flexao_YY", "capacidade_flexao_resistente_secao_nominal_yy"),
            ("esbeltez_flexao_XX", "capacidade_flexao_resistente_secao_design_xx"),
            ("esbeltez_flexao_YY", "capacidade_flexao_resistente_secao_design_yy"),
        ],
    )
    def test_resistencias_flexao_secao_esbelta_lancam_not_implemented(
        self,
        monkeypatch,
        concreto,
        aco_estrutural,
        criar_pilar_retangular_preenchido,
        eixo,
        resistencia_flexao,
    ):
        monkeypatch.setattr(
            PilarRetangularPreenchido,
            eixo,
            property(lambda self: Secao.ESBELTO),
        )
        pilar = criar_pilar_retangular_preenchido(concreto, aco_estrutural)

        with pytest.raises(NotImplementedError):
            getattr(pilar, resistencia_flexao)
