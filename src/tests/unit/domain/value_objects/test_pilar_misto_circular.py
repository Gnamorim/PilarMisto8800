import pytest
import numpy as np
from math import isclose

from MY_PACKAGE.domain.value_objects.pilar_misto_circular import PilarCircularPreenchido
from MY_PACKAGE.domain.value_objects.ObjetoConcreto import ConcretoNormal
from MY_PACKAGE.domain.value_objects.ObjetoAco import AcoEstrutural, AcoArmadura
from MY_PACKAGE.domain.value_objects._classe_secao import Secao


# -------------------------
# Fixtures (objetos base)
# -------------------------

@pytest.fixture
def concreto():
    return ConcretoNormal(fck=40)

@pytest.fixture
def aco_estrutural():
    return AcoEstrutural(fy=345)

@pytest.fixture
def aco_armadura():
    return AcoArmadura(fy=500)


class TestValidacaoCircular:

    # -------------------------
    # Casos válidos
    # -------------------------

    def test_criacao_sem_armadura(self, concreto, aco_estrutural):
        pilar = PilarCircularPreenchido(
            diametro_tubo=300,
            espessura_tubo=10,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto,
            material_armadura=None,
            comprimento_pilar_destravado= 3000
        )

        assert pilar.material_armadura is None
        assert pilar.numero_armadura_longitudinal == 0
        assert pilar.diametro_interno == 280


    def test_criacao_com_armadura(self, concreto, aco_estrutural, aco_armadura):
        pilar = PilarCircularPreenchido(
            diametro_tubo=300,
            espessura_tubo=10,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto,
            material_armadura=aco_armadura,
            diametro_armadura_longitudinal=16,
            numero_armadura_longitudinal=6,
            diametro_armadura_transversal=8,
            espacamento_armadura_transversal=150,
            cobrimento=30,
            comprimento_pilar_destravado= 3000
        )

        assert pilar.material_armadura is not None
        assert pilar.numero_armadura_longitudinal == 6


    # -------------------------
    # Testes de erro (tipos)
    # -------------------------

    def test_tipo_invalido_diametro(self, concreto, aco_estrutural):
        with pytest.raises(TypeError):
            PilarCircularPreenchido(
                diametro_tubo="300",
                espessura_tubo=10,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
            comprimento_pilar_destravado= 3000
            )


    def test_tipo_invalido_material(self, concreto):
        with pytest.raises(TypeError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=10,
                material_aco_estrutural="aco",
                material_concreto=concreto,
            comprimento_pilar_destravado= 3000
            )


    # -------------------------
    # Testes de erro (valores físicos)
    # -------------------------

    def test_espessura_invalida(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=200,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
            comprimento_pilar_destravado= 3000
            )

    def test_espessura_zero(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=0,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
            comprimento_pilar_destravado= 3000
            )

    def test_diametro_interno_invalido(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=150,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
            comprimento_pilar_destravado= 3000
            )

    def test_diametro_negativo(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=-300,
                espessura_tubo=10,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
            comprimento_pilar_destravado= 3000
            )


    # -------------------------
    # Armadura inconsistente
    # -------------------------

    def test_armadura_invalida_valores(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=10,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                material_armadura=aco_armadura,
                diametro_armadura_longitudinal=0,
                numero_armadura_longitudinal=6,
                diametro_armadura_transversal=8,
                espacamento_armadura_transversal=150,
                cobrimento=30,
            comprimento_pilar_destravado= 3000
            )


    def test_sem_armadura_com_valores_nao_zero(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=10,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                material_armadura=None,
                diametro_armadura_longitudinal=16,
            comprimento_pilar_destravado= 3000
            )


    # -------------------------
    # Validação base - limites e tipos extremos
    # -------------------------

    def test_diametro_armadura_longitudinal_maior_que_50(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=10,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                material_armadura=aco_armadura,
                diametro_armadura_longitudinal=60,
                numero_armadura_longitudinal=4,
                diametro_armadura_transversal=8,
                espacamento_armadura_transversal=150,
                cobrimento=30,
            comprimento_pilar_destravado= 3000
            )


    def test_diametro_armadura_longitudinal_muito_pequeno(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=10,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                material_armadura=aco_armadura,
                diametro_armadura_longitudinal=4,
                numero_armadura_longitudinal=4,
                diametro_armadura_transversal=8,
                espacamento_armadura_transversal=150,
                cobrimento=30,
            comprimento_pilar_destravado= 3000
            )


    def test_numero_armadura_maior_que_30(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=10,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                material_armadura=aco_armadura,
                diametro_armadura_longitudinal=16,
                numero_armadura_longitudinal=31,
                diametro_armadura_transversal=8,
                espacamento_armadura_transversal=150,
                cobrimento=30,
            comprimento_pilar_destravado= 3000
            )


    def test_diametro_armadura_transversal_maior_que_50(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=10,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                material_armadura=aco_armadura,
                diametro_armadura_longitudinal=16,
                numero_armadura_longitudinal=4,
                diametro_armadura_transversal=60,
                espacamento_armadura_transversal=150,
                cobrimento=30,
            comprimento_pilar_destravado= 3000
            )


    def test_diametro_armadura_transversal_muito_pequeno(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=10,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                material_armadura=aco_armadura,
                diametro_armadura_longitudinal=16,
                numero_armadura_longitudinal=4,
                diametro_armadura_transversal=4,
                espacamento_armadura_transversal=150,
                cobrimento=30,
            comprimento_pilar_destravado= 3000
            )


    def test_espacamento_maior_que_1000(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=10,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                material_armadura=aco_armadura,
                diametro_armadura_longitudinal=16,
                numero_armadura_longitudinal=4,
                diametro_armadura_transversal=8,
                espacamento_armadura_transversal=1500,
                cobrimento=30,
            comprimento_pilar_destravado= 3000
            )


    def test_cobrimento_negativo(self, concreto, aco_estrutural, aco_armadura):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=10,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                material_armadura=aco_armadura,
                diametro_armadura_longitudinal=16,
                numero_armadura_longitudinal=4,
                diametro_armadura_transversal=8,
                espacamento_armadura_transversal=150,
                cobrimento=-10,
            comprimento_pilar_destravado= 3000
            )


    def test_tipo_bool_invalido(self, concreto, aco_estrutural):
        with pytest.raises(TypeError):
            PilarCircularPreenchido(
                diametro_tubo=True,
                espessura_tubo=10,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
            comprimento_pilar_destravado= 3000
            )


class TestLimiteEscopo:

    # -------------------------
    # Limite de escopo
    # -------------------------

    def test_area_aco_muito_pequena(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=0.1,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
            comprimento_pilar_destravado= 3000
            )


    def test_fator_contribuicao_muito_baixo(self, concreto, aco_estrutural):
       
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=1,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
            comprimento_pilar_destravado= 3000
            )


    def test_fator_contribuicao_muito_alto(self, concreto, aco_estrutural):
        
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=50,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
            comprimento_pilar_destravado= 3000
            )


    def test_esbeltez_fora_do_escopo(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=1000,
                espessura_tubo=1,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
            comprimento_pilar_destravado= 3000
            )


class TestGeometrico:

    # -------------------------
    # Métodos de área
    # -------------------------

    def test_area_aco(self, concreto, aco_estrutural):
        pilar = PilarCircularPreenchido(
            diametro_tubo=300,
            espessura_tubo=10,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto,
            comprimento_pilar_destravado= 3000
        )

        area = pilar.area_aco
        esperado = (np.pi * (300**2 - 280**2)) / 4

        assert np.isclose(area, esperado)


    def test_area_concreto(self, concreto, aco_estrutural, aco_armadura):
        pilar = PilarCircularPreenchido(
            diametro_tubo=300,
            espessura_tubo=10,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto,
            comprimento_pilar_destravado= 3000
        )

        pilar2 = PilarCircularPreenchido(
            diametro_tubo=300,
            espessura_tubo=10,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto,
            material_armadura=aco_armadura,
            diametro_armadura_longitudinal=16,
            numero_armadura_longitudinal=6,
            diametro_armadura_transversal=8,
            espacamento_armadura_transversal=150,
            cobrimento=30,
            comprimento_pilar_destravado= 3000
        )

        area = pilar.area_concreto
        esperado = (np.pi * (280**2)) / 4

        area2 = pilar2.area_concreto
        esperado2 = ((np.pi * (280**2)) / 4) - (6 * ((np.pi * (16**2)) / 4))

        assert np.isclose(area, esperado)
        assert np.isclose(area2, esperado2)


    def test_area_armadura(self, concreto, aco_estrutural, aco_armadura):
        pilar = PilarCircularPreenchido(
            diametro_tubo=300,
            espessura_tubo=10,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto,
            material_armadura=aco_armadura,
            diametro_armadura_longitudinal=16,
            numero_armadura_longitudinal=4,
            diametro_armadura_transversal=8,
            espacamento_armadura_transversal=150,
            cobrimento=30,
            comprimento_pilar_destravado= 3000
        )

        area = pilar.area_armadura
        esperado = (np.pi * (16**2) * 4) / 4

        assert np.isclose(area, esperado)

    def test_area_total_uses_property_api(self, concreto, aco_estrutural):
        pilar = PilarCircularPreenchido(
            diametro_tubo=300,
            espessura_tubo=10,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto,
            comprimento_pilar_destravado=3000
        )

        esperado = pilar.area_aco + pilar.area_concreto + pilar.area_armadura

        assert np.isclose(pilar.area_total(), esperado)






class TestPropriedadesMecanicas:

    def test_cfst_design_strength(self, concreto, aco_estrutural, aco_armadura):
                        
        # variable definition

        concreto1 = ConcretoNormal(40,30000)

        tube_diameter =  600 # mm
        thickness = 9.5 # mm
        cover = 25 # mm
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
            espessura_tubo= thickness,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto1,
            material_armadura=aco_armadura,
            cobrimento = cover,
            diametro_armadura_longitudinal=bar_diameter,
            numero_armadura_longitudinal=bar_number,
            diametro_armadura_transversal=stirrup,
            espacamento_armadura_transversal=150,
            comprimento_pilar_destravado= 3000
             )
        
        pilar1 = PilarCircularPreenchido(
            diametro_tubo=tube_diameter,
            espessura_tubo= thickness,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto1,
            comprimento_pilar_destravado= 3000
        )

        tol = 1e-2
        assert isclose(pilar.capacidade_axial_plastico_aco_design(), nplrds, rel_tol=tol)
        assert isclose(pilar.capacidade_axial_plastico_armadura_design(), nplrdrs, rel_tol=tol)
        assert isclose(pilar.capacidade_axial_plastico_concreto_design(), nplrdc, rel_tol=tol)
        assert isclose(pilar.capacidade_axial_plastico_design(), nplrd, rel_tol=tol)

        
        assert isclose(pilar1.capacidade_axial_plastico_aco_design(), nplrds2, rel_tol=tol)
        assert isclose(pilar1.capacidade_axial_plastico_armadura_design(), 0, rel_tol=tol)
        assert isclose(pilar1.capacidade_axial_plastico_concreto_design(), nplrdc2, rel_tol=tol)
        assert isclose(pilar1.capacidade_axial_plastico_design(), nplrd2, rel_tol=tol)

    def test_plastic_moment_z(self, concreto, aco_estrutural, aco_armadura):

        # variable definition
        concreto1 = ConcretoNormal(40,30000)

        tube_diameter =  600 # mm
        thickness = 9.5 # mm
        cover = 25 # mm
        bar_diameter = 20.0
        bar_number = 10
        stirrup = 5

        Mpl = 1.4911e9
        Mmax = 1.6867e9

        Mpl1 = 1.2489e9
        Mmax1 = 1.4826e9

        pilar = PilarCircularPreenchido(
            diametro_tubo=tube_diameter,
            espessura_tubo= thickness,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto1,
            material_armadura=aco_armadura,
            cobrimento = cover,
            diametro_armadura_longitudinal=bar_diameter,
            numero_armadura_longitudinal=bar_number,
            diametro_armadura_transversal=stirrup,
            espacamento_armadura_transversal=150,
            comprimento_pilar_destravado= 3000
             )
        
        pilar1 = PilarCircularPreenchido(
            diametro_tubo=tube_diameter,
            espessura_tubo= thickness,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto1,
            comprimento_pilar_destravado= 3000
            )

        tol = 1e-2

        assert isclose(pilar.momento_resistente_plastico_total_design_xx, Mpl, abs_tol=tol, rel_tol= tol)
        assert isclose(pilar.momento_resistente_maximo_plastico_total_design_xx, Mmax, abs_tol=tol, rel_tol= tol)

        # considering cfst1
        assert isclose(pilar1.momento_resistente_plastico_total_design_xx, Mpl1, abs_tol=tol, rel_tol= tol)
        assert isclose(pilar1.momento_resistente_maximo_plastico_total_design_xx, Mmax1, abs_tol=tol, rel_tol= tol)

    def test_plastic_moment_y(self, concreto, aco_estrutural, aco_armadura):

        # variable definition
        concreto1 = ConcretoNormal(40,30000)

        tube_diameter =  600 # mm
        thickness = 9.5 # mm
        cover = 25 # mm
        bar_diameter = 20.0
        bar_number = 10
        stirrup = 5

        Mpl = 1.4908e9
        Mmax = 1.6972e9

        Mpl1 = 1.2489e9
        Mmax1 = 1.4826e9

        pilar = PilarCircularPreenchido(
            diametro_tubo=tube_diameter,
            espessura_tubo= thickness,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto1,
            material_armadura=aco_armadura,
            cobrimento = cover,
            diametro_armadura_longitudinal=bar_diameter,
            numero_armadura_longitudinal=bar_number,
            diametro_armadura_transversal=stirrup,
            espacamento_armadura_transversal=150,
            comprimento_pilar_destravado= 3000
             )
        
        pilar1 = PilarCircularPreenchido(
            diametro_tubo=tube_diameter,
            espessura_tubo= thickness,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto1,
            comprimento_pilar_destravado= 3000
            )
        tol = 1e-2

        assert isclose(pilar.momento_resistente_plastico_total_design_yy, Mpl, abs_tol=tol, rel_tol= tol)
        assert isclose(pilar.momento_resistente_maximo_plastico_total_design_yy, Mmax, abs_tol=tol, rel_tol= tol)

        # considering cfst1
        assert isclose(pilar1.momento_resistente_plastico_total_design_yy, Mpl1, abs_tol=tol, rel_tol= tol)
        assert isclose(pilar1.momento_resistente_maximo_plastico_total_design_yy, Mmax1, abs_tol=tol, rel_tol= tol)

    def test_resistencias_flexao_secao_compacta_retornam_valores_esperados(self, concreto, aco_estrutural):
        """
        Para seções compactas, as resistências à flexão já estão implementadas
        e devem retornar os momentos plásticos calculados.
        """
        pilar = PilarCircularPreenchido(
            diametro_tubo=300,
            espessura_tubo=10,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto,
            comprimento_pilar_destravado=3000
        )

        assert pilar.capacidade_flexao_resistente_secao_nominal_xx == pilar.momento_resistente_plastico_total_xx
        assert pilar.capacidade_flexao_resistente_secao_nominal_yy == pilar.momento_resistente_plastico_total_yy
        assert pilar.capacidade_flexao_resistente_secao_design_xx == pilar.momento_resistente_plastico_total_design_xx
        assert pilar.capacidade_flexao_resistente_secao_design_yy == pilar.momento_resistente_plastico_total_design_yy

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
            comprimento_pilar_destravado=3000
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
            comprimento_pilar_destravado=3000
        )

        with pytest.raises(NotImplementedError):
            getattr(pilar, resistencia_flexao)
