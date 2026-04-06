import pytest
from math import isclose

from MY_PACKAGE.domain.value_objects.pilar_misto_circular import PilarCircularPreenchido
from MY_PACKAGE.domain.value_objects.ObjetoConcreto import ConcretoNormal
from MY_PACKAGE.domain.value_objects._classe_secao import Secao


class TestPropriedadesMecanicas:

    def test_cfst_design_strength(self, concreto, aco_estrutural, aco_armadura):

        # variable definition

        concreto1 = ConcretoNormal(40, 30000)

        tube_diameter = 600  # mm
        thickness = 9.5  # mm
        cover = 25  # mm
        bar_diameter = 20.0
        bar_number = 10
        stirrup = 5
        nplrds = 5.5274e6
        nplrdrs = 5.969e5
        nplrdc = 7.1108e6
        nplrd = 1.33204e7
        nplrdc2 = 7.1961e6
        nplrds2 = 5.5274e6
        nplrd2 = nplrdc2 + nplrds2

        pilar = PilarCircularPreenchido(
            diametro_tubo=tube_diameter,
            espessura_tubo=thickness,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto1,
            material_armadura=aco_armadura,
            cobrimento=cover,
            diametro_armadura_longitudinal=bar_diameter,
            numero_armadura_longitudinal=bar_number,
            diametro_armadura_transversal=stirrup,
            espacamento_armadura_transversal=150,
            comprimento_pilar_destravado=3000,
        )

        pilar1 = PilarCircularPreenchido(
            diametro_tubo=tube_diameter,
            espessura_tubo=thickness,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto1,
            comprimento_pilar_destravado=3000,
        )

        tol = 1e-2
        assert isclose(pilar.capacidade_axial_plastico_aco_design(), nplrds, rel_tol=tol)
        assert isclose(
            pilar.capacidade_axial_plastico_armadura_design(),
            nplrdrs,
            rel_tol=tol,
        )
        assert isclose(
            pilar.capacidade_axial_plastico_concreto_design(),
            nplrdc,
            rel_tol=tol,
        )
        assert isclose(pilar.capacidade_axial_plastico_design(), nplrd, rel_tol=tol)

        assert isclose(
            pilar1.capacidade_axial_plastico_aco_design(),
            nplrds2,
            rel_tol=tol,
        )
        assert isclose(pilar1.capacidade_axial_plastico_armadura_design(), 0, rel_tol=tol)
        assert isclose(
            pilar1.capacidade_axial_plastico_concreto_design(),
            nplrdc2,
            rel_tol=tol,
        )
        assert isclose(pilar1.capacidade_axial_plastico_design(), nplrd2, rel_tol=tol)

    def test_plastic_moment_z(self, concreto, aco_estrutural, aco_armadura):

        # variable definition
        concreto1 = ConcretoNormal(40, 30000)

        tube_diameter = 600  # mm
        thickness = 9.5  # mm
        cover = 25  # mm
        bar_diameter = 20.0
        bar_number = 10
        stirrup = 5

        Mpl = 1.4911e9
        Mmax = 1.6867e9

        Mpl1 = 1.2489e9
        Mmax1 = 1.4826e9

        pilar = PilarCircularPreenchido(
            diametro_tubo=tube_diameter,
            espessura_tubo=thickness,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto1,
            material_armadura=aco_armadura,
            cobrimento=cover,
            diametro_armadura_longitudinal=bar_diameter,
            numero_armadura_longitudinal=bar_number,
            diametro_armadura_transversal=stirrup,
            espacamento_armadura_transversal=150,
            comprimento_pilar_destravado=3000,
        )

        pilar1 = PilarCircularPreenchido(
            diametro_tubo=tube_diameter,
            espessura_tubo=thickness,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto1,
            comprimento_pilar_destravado=3000,
        )

        tol = 1e-2

        assert isclose(
            pilar.momento_resistente_plastico_total_design_xx,
            Mpl,
            abs_tol=tol,
            rel_tol=tol,
        )
        assert isclose(
            pilar.momento_resistente_maximo_plastico_total_design_xx,
            Mmax,
            abs_tol=tol,
            rel_tol=tol,
        )

        # considering cfst1
        assert isclose(
            pilar1.momento_resistente_plastico_total_design_xx,
            Mpl1,
            abs_tol=tol,
            rel_tol=tol,
        )
        assert isclose(
            pilar1.momento_resistente_maximo_plastico_total_design_xx,
            Mmax1,
            abs_tol=tol,
            rel_tol=tol,
        )

    def test_plastic_moment_y(self, concreto, aco_estrutural, aco_armadura):

        # variable definition
        concreto1 = ConcretoNormal(40, 30000)

        tube_diameter = 600  # mm
        thickness = 9.5  # mm
        cover = 25  # mm
        bar_diameter = 20.0
        bar_number = 10
        stirrup = 5

        Mpl = 1.4908e9
        Mmax = 1.6972e9

        Mpl1 = 1.2489e9
        Mmax1 = 1.4826e9

        pilar = PilarCircularPreenchido(
            diametro_tubo=tube_diameter,
            espessura_tubo=thickness,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto1,
            material_armadura=aco_armadura,
            cobrimento=cover,
            diametro_armadura_longitudinal=bar_diameter,
            numero_armadura_longitudinal=bar_number,
            diametro_armadura_transversal=stirrup,
            espacamento_armadura_transversal=150,
            comprimento_pilar_destravado=3000,
        )

        pilar1 = PilarCircularPreenchido(
            diametro_tubo=tube_diameter,
            espessura_tubo=thickness,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto1,
            comprimento_pilar_destravado=3000,
        )
        tol = 1e-2

        assert isclose(
            pilar.momento_resistente_plastico_total_design_yy,
            Mpl,
            abs_tol=tol,
            rel_tol=tol,
        )
        assert isclose(
            pilar.momento_resistente_maximo_plastico_total_design_yy,
            Mmax,
            abs_tol=tol,
            rel_tol=tol,
        )

        # considering cfst1
        assert isclose(
            pilar1.momento_resistente_plastico_total_design_yy,
            Mpl1,
            abs_tol=tol,
            rel_tol=tol,
        )
        assert isclose(
            pilar1.momento_resistente_maximo_plastico_total_design_yy,
            Mmax1,
            abs_tol=tol,
            rel_tol=tol,
        )

    def test_resistencias_flexao_secao_compacta_retornam_valores_esperados(
        self, concreto, aco_estrutural
    ):
        """
        Para seções compactas, as resistências à flexão já estão implementadas
        e devem retornar os momentos plásticos calculados.
        """
        pilar = PilarCircularPreenchido(
            diametro_tubo=300,
            espessura_tubo=10,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto,
            comprimento_pilar_destravado=3000,
        )

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
        "resistencia_flexao",
        [
            "capacidade_flexao_resistente_secao_nominal_xx",
            "capacidade_flexao_resistente_secao_nominal_yy",
            "capacidade_flexao_resistente_secao_design_xx",
            "capacidade_flexao_resistente_secao_design_yy",
        ],
    )
    def test_resistencias_flexao_secao_nao_compacta_lancam_not_implemented(
        self, concreto, aco_estrutural, resistencia_flexao
    ):
        """
        Para seções não compactas à flexão, as fórmulas ainda não estão
        implementadas e a API deve falhar explicitamente com NotImplementedError.
        """
        pilar = PilarCircularPreenchido(
            diametro_tubo=600,
            espessura_tubo=9.5,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto,
            comprimento_pilar_destravado=3000,
        )

        assert pilar.esbeltez_flexao == Secao.NAO_COMPACTO
        with pytest.raises(NotImplementedError):
            getattr(pilar, resistencia_flexao)

    @pytest.mark.parametrize(
        "resistencia_flexao",
        [
            "capacidade_flexao_resistente_secao_nominal_xx",
            "capacidade_flexao_resistente_secao_nominal_yy",
            "capacidade_flexao_resistente_secao_design_xx",
            "capacidade_flexao_resistente_secao_design_yy",
        ],
    )
    def test_resistencias_flexao_secao_esbelta_lancam_not_implemented(
        self, monkeypatch, concreto, aco_estrutural, resistencia_flexao
    ):
        """
        Para seções esbeltas à flexão, as fórmulas ainda não estão implementadas;
        o monkeypatch força esse estado para testar o comportamento da API.
        """
        monkeypatch.setattr(
            PilarCircularPreenchido,
            "esbeltez_flexao",
            property(lambda self: Secao.ESBELTO),
        )
        pilar = PilarCircularPreenchido(
            diametro_tubo=300,
            espessura_tubo=10,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto,
            comprimento_pilar_destravado=3000,
        )

        with pytest.raises(NotImplementedError):
            getattr(pilar, resistencia_flexao)
