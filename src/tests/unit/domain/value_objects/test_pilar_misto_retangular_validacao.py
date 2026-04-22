import pytest


class TestValidacaoRetangularPreenchido:
    def test_criacao_sem_armadura(
        self, concreto, aco_estrutural, criar_pilar_retangular_preenchido
    ):
        pilar = criar_pilar_retangular_preenchido(concreto, aco_estrutural)

        assert pilar.material_armadura is None
        assert pilar.numero_armadura_longitudinal == 0
        assert pilar.altura_tubo == 300
        assert pilar.largura_tubo == 200

    def test_criacao_com_armadura(
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

        assert pilar.material_armadura is not None
        assert pilar.numero_armadura_longitudinal == 4
        assert pilar.diametro_armadura_longitudinal == 16

    def test_tipo_invalido_altura(
        self, concreto, aco_estrutural, criar_pilar_retangular_preenchido
    ):
        with pytest.raises(TypeError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                altura_tubo="300",
            )

    def test_tipo_invalido_largura(
        self, concreto, aco_estrutural, criar_pilar_retangular_preenchido
    ):
        with pytest.raises(TypeError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                largura_tubo="200",
            )

    def test_tipo_invalido_espessura(
        self, concreto, aco_estrutural, criar_pilar_retangular_preenchido
    ):
        with pytest.raises(TypeError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                espessura_tubo="10",
            )

    def test_tipo_bool_invalido(
        self, concreto, aco_estrutural, criar_pilar_retangular_preenchido
    ):
        with pytest.raises(TypeError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                altura_tubo=True,
            )

    def test_tipo_invalido_material(self, concreto, criar_pilar_retangular_preenchido):
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
    def test_dimensoes_invalidas(
        self, concreto, aco_estrutural, campo, valor, criar_pilar_retangular_preenchido
    ):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                **{campo: valor},
            )

    def test_espessura_fisicamente_invalida(
        self, concreto, aco_estrutural, criar_pilar_retangular_preenchido
    ):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                altura_tubo=300,
                largura_tubo=200,
                espessura_tubo=120,
            )

    def test_armadura_invalida_valores(
        self, concreto, aco_estrutural, aco_armadura, criar_pilar_retangular_preenchido
    ):
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

    def test_sem_armadura_com_valores_nao_zero(
        self, concreto, aco_estrutural, criar_pilar_retangular_preenchido
    ):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                diametro_armadura_longitudinal=16,
            )

    def test_diametro_armadura_longitudinal_maior_que_50(
        self, concreto, aco_estrutural, aco_armadura, criar_pilar_retangular_preenchido
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
        self, concreto, aco_estrutural, aco_armadura, criar_pilar_retangular_preenchido
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

    def test_numero_armadura_maior_que_30(
        self, concreto, aco_estrutural, aco_armadura, criar_pilar_retangular_preenchido
    ):
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
        self, concreto, aco_estrutural, aco_armadura, criar_pilar_retangular_preenchido
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
        self, concreto, aco_estrutural, aco_armadura, criar_pilar_retangular_preenchido
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

    def test_espacamento_maior_que_1000(
        self, concreto, aco_estrutural, aco_armadura, criar_pilar_retangular_preenchido
    ):
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

    def test_cobrimento_negativo(
        self, concreto, aco_estrutural, aco_armadura, criar_pilar_retangular_preenchido
    ):
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
    def test_razao_largura_altura_muito_pequena(
        self,
        concreto,
        aco_estrutural,
        aco_armadura,
        criar_pilar_retangular_preenchido,
    ):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                aco_armadura=aco_armadura,
                altura_tubo=1000,
                largura_tubo=100,
                espessura_tubo=12,
                diametro_armadura_longitudinal=16,
                numero_armadura_longitudinal=4,
                diametro_armadura_transversal=8,
                espacamento_armadura_transversal=150,
                cobrimento=30,
            )

    def test_razao_largura_altura_muito_grande(
        self,
        concreto,
        aco_estrutural,
        aco_armadura,
        criar_pilar_retangular_preenchido,
    ):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                aco_armadura=aco_armadura,
                altura_tubo=100,
                largura_tubo=1000,
                espessura_tubo=12,
                diametro_armadura_longitudinal=16,
                numero_armadura_longitudinal=4,
                diametro_armadura_transversal=8,
                espacamento_armadura_transversal=150,
                cobrimento=30,
            )

    def test_area_aco_muito_pequena(
        self, concreto, aco_estrutural, criar_pilar_retangular_preenchido
    ):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                altura_tubo=300,
                largura_tubo=200,
                espessura_tubo=0.1,
            )

    def test_fator_contribuicao_muito_baixo(
        self, concreto, aco_estrutural, criar_pilar_retangular_preenchido
    ):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                altura_tubo=300,
                largura_tubo=200,
                espessura_tubo=1,
            )

    def test_fator_contribuicao_muito_alto(
        self, concreto, aco_estrutural, criar_pilar_retangular_preenchido
    ):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                altura_tubo=300,
                largura_tubo=200,
                espessura_tubo=45,
            )

    def test_esbeltez_fora_do_escopo(
        self, concreto, aco_estrutural, criar_pilar_retangular_preenchido
    ):
        with pytest.raises(ValueError):
            criar_pilar_retangular_preenchido(
                concreto,
                aco_estrutural,
                altura_tubo=600,
                largura_tubo=300,
                espessura_tubo=1,
                comprimento_pilar_destravado=12000,
            )
