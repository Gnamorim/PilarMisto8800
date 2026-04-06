import pytest

from MY_PACKAGE.domain.value_objects.pilar_misto_circular import PilarCircularPreenchido


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
            comprimento_pilar_destravado=3000,
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
            comprimento_pilar_destravado=3000,
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
                comprimento_pilar_destravado=3000,
            )

    def test_tipo_invalido_material(self, concreto):
        with pytest.raises(TypeError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=10,
                material_aco_estrutural="aco",
                material_concreto=concreto,
                comprimento_pilar_destravado=3000,
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
                comprimento_pilar_destravado=3000,
            )

    def test_espessura_zero(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=0,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                comprimento_pilar_destravado=3000,
            )

    def test_diametro_interno_invalido(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=150,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                comprimento_pilar_destravado=3000,
            )

    def test_diametro_negativo(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=-300,
                espessura_tubo=10,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                comprimento_pilar_destravado=3000,
            )

    # -------------------------
    # Armadura inconsistente
    # -------------------------

    def test_armadura_invalida_valores(
        self, concreto, aco_estrutural, aco_armadura
    ):
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
                comprimento_pilar_destravado=3000,
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
                comprimento_pilar_destravado=3000,
            )

    # -------------------------
    # Validação base - limites e tipos extremos
    # -------------------------

    def test_diametro_armadura_longitudinal_maior_que_50(
        self, concreto, aco_estrutural, aco_armadura
    ):
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
                comprimento_pilar_destravado=3000,
            )

    def test_diametro_armadura_longitudinal_muito_pequeno(
        self, concreto, aco_estrutural, aco_armadura
    ):
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
                comprimento_pilar_destravado=3000,
            )

    def test_numero_armadura_maior_que_30(
        self, concreto, aco_estrutural, aco_armadura
    ):
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
                comprimento_pilar_destravado=3000,
            )

    def test_diametro_armadura_transversal_maior_que_50(
        self, concreto, aco_estrutural, aco_armadura
    ):
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
                comprimento_pilar_destravado=3000,
            )

    def test_diametro_armadura_transversal_muito_pequeno(
        self, concreto, aco_estrutural, aco_armadura
    ):
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
                comprimento_pilar_destravado=3000,
            )

    def test_espacamento_maior_que_1000(
        self, concreto, aco_estrutural, aco_armadura
    ):
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
                comprimento_pilar_destravado=3000,
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
                comprimento_pilar_destravado=3000,
            )

    def test_tipo_bool_invalido(self, concreto, aco_estrutural):
        with pytest.raises(TypeError):
            PilarCircularPreenchido(
                diametro_tubo=True,
                espessura_tubo=10,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                comprimento_pilar_destravado=3000,
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
                comprimento_pilar_destravado=3000,
            )

    def test_fator_contribuicao_muito_baixo(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=1,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                comprimento_pilar_destravado=3000,
            )

    def test_fator_contribuicao_muito_alto(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=300,
                espessura_tubo=50,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                comprimento_pilar_destravado=3000,
            )

    def test_esbeltez_fora_do_escopo(self, concreto, aco_estrutural):
        with pytest.raises(ValueError):
            PilarCircularPreenchido(
                diametro_tubo=1000,
                espessura_tubo=1,
                material_aco_estrutural=aco_estrutural,
                material_concreto=concreto,
                comprimento_pilar_destravado=3000,
            )
