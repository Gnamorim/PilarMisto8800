import numpy as np


class TestGeometriaRetangularPreenchido:
    def test_area_aco(self, concreto, aco_estrutural, criar_pilar_retangular_preenchido):
        pilar = criar_pilar_retangular_preenchido(concreto, aco_estrutural)

        area_esperada = (300 * 200) - ((200 - 2 * 10) * (300 - 2 * 10))

        assert np.isclose(pilar.area_aco, area_esperada)

    def test_area_concreto(
        self, concreto, aco_estrutural, aco_armadura, criar_pilar_retangular_preenchido
    ):
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

    def test_area_armadura(
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

        area_esperada = 4 * (np.pi * (16**2) / 4)

        assert np.isclose(pilar.area_armadura, area_esperada)

    def test_area_total_usa_api_publica(
        self, concreto, aco_estrutural, criar_pilar_retangular_preenchido
    ):
        pilar = criar_pilar_retangular_preenchido(concreto, aco_estrutural)

        area_esperada = pilar.area_aco + pilar.area_concreto + pilar.area_armadura

        assert np.isclose(pilar.area_total(), area_esperada)
