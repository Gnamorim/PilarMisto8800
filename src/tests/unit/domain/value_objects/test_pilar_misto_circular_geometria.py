import numpy as np

from MY_PACKAGE.domain.value_objects.pilar_misto_circular import PilarCircularPreenchido


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
            comprimento_pilar_destravado=3000,
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
            comprimento_pilar_destravado=3000,
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
            comprimento_pilar_destravado=3000,
        )

        area = pilar.area_concreto
        esperado = (np.pi * (280**2)) / 4

        area2 = pilar2.area_concreto
        esperado2 = ((np.pi * (280**2)) / 4) - (
            6 * ((np.pi * (16**2)) / 4)
        )

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
            comprimento_pilar_destravado=3000,
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
            comprimento_pilar_destravado=3000,
        )

        esperado = pilar.area_aco + pilar.area_concreto + pilar.area_armadura

        assert np.isclose(pilar.area_total(), esperado)
