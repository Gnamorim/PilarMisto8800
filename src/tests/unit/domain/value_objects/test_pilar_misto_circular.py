import pytest
import numpy as np

from MY_PACKAGE.domain.value_objects.pilar_misto_circular import PilarCircularPreenchido
from MY_PACKAGE.domain.value_objects.ObjetoConcreto import ConcretoNormal
from MY_PACKAGE.domain.value_objects.ObjetoAco import AcoEstrutural, AcoArmadura


# -------------------------
# Fixtures (objetos base)
# -------------------------

@pytest.fixture
def concreto():
    return ConcretoNormal(fck=30)

@pytest.fixture
def aco_estrutural():
    return AcoEstrutural(fy=355)

@pytest.fixture
def aco_armadura():
    return AcoArmadura(fy=500)


class TestPilarCircularPreenchido:

   # -------------------------
    # Casos válidos
    # -------------------------

    def test_criacao_sem_armadura(self, concreto, aco_estrutural):
        pilar = PilarCircularPreenchido(
            diametro_tubo=300,
            espessura_tubo=10,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto,
            material_armadura=None
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
            cobrimento=30
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
                material_concreto=concreto
            )


    def test_tipo_invalido_material(self, concreto):
        with pytest.raises(TypeError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=10,
                material_aco_estrutural="aco",
                material_concreto=concreto
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
                material_concreto=concreto
            )


    def test_diametro_negativo(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=-300,
                espessura_tubo=10,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto
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
                cobrimento=30
            )


    def test_sem_armadura_com_valores_nao_zero(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=10,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                material_armadura=None,
                diametro_armadura_longitudinal=16
            )


    # -------------------------
    # Métodos de área
    # -------------------------

    def test_area_aco(self, concreto, aco_estrutural):
        pilar = PilarCircularPreenchido(
            diametro_tubo=300,
            espessura_tubo=10,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto
        )

        area = pilar.area_aco()
        esperado = (np.pi * (300**2 - 280**2)) / 4

        assert np.isclose(area, esperado)


    def test_area_concreto(self, concreto, aco_estrutural, aco_armadura):
        pilar = PilarCircularPreenchido(
            diametro_tubo=300,
            espessura_tubo=10,
            material_aco_estrutural=aco_estrutural,
            material_concreto=concreto
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
            cobrimento=30
        )

        area = pilar.area_concreto()
        esperado = (np.pi * (280**2)) / 4

        area2 = pilar2.area_concreto()
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
            cobrimento=30
        )

        area = pilar.area_armadura()
        esperado = (np.pi * (16**2) * 4) / 4

        assert np.isclose(area, esperado)