from MY_PACKAGE.domain.value_objects.ObjetoConcreto import TipoAgregado, ConcretoNormal
from math import isclose
import pytest

class TestObjetoConcreto:

    def test_inicializacao(self):

        # definicao das variaveis
            
        fck1 = 50
        fck2 = 30
        Ec = 30000
        agregado = TipoAgregado.GRANITO
        gamma = 1.2

        # criacao das instancias

        concreto1 = ConcretoNormal(fck=fck1)
        concreto2 = ConcretoNormal(
                                fck=fck2, 
                                modulo_elasticidade=Ec, 
                                tipo_agregado = agregado,
                                gamma = gamma
                                )

        # processo de verificacao de compatibilidade das variaveis

        assert concreto1.fck == fck1
        assert concreto1._modulo_elasticidade == 0.0
        assert concreto1.tipo_agregado == TipoAgregado.BASALTO
        assert concreto1.gamma == 1.4

        assert concreto2.fck == fck2
        assert concreto2._modulo_elasticidade == Ec
        assert concreto2.tipo_agregado == agregado
        assert concreto2.gamma == gamma

    def test_validate_concreto(self):
        fck1 = 'a'

        with pytest.raises(TypeError, match= 'fck must be a float or an integer'):
            ConcretoNormal(fck=fck1)

    def test_validate_TipoAgregado(self):
        fck1 = 30
        tipo_agregado = 'a'

        with pytest.raises(TypeError, match= f"Operacao deve ser do tipo TipoAgregado, recebido {type(tipo_agregado)}"):
            ConcretoNormal(
                        fck=fck1, 
                        tipo_agregado=tipo_agregado
                    )

    def test_validate_modulo_elasticidade(self):
        fck1 = 30
        Ec = 'a'

        with pytest.raises(TypeError, match= 'modulo_elasticidade must be a float or an integer'):
            ConcretoNormal(
                        fck=fck1, 
                        modulo_elasticidade=Ec
                    )

    def test_validate_gamma(self):
        fck1 = 30
        gamma = 'a'   

        with pytest.raises(TypeError, match= 'Gamma must be a float'):
            ConcretoNormal(
                    fck=fck1, 
                    gamma = gamma
                )


    def test_limite_escopo(self):
        
        # valores dentro do limite de escopo
        fck0 = 20
        fck3 = 50

 
        c = ConcretoNormal(fck=fck0)
        assert isinstance(c,ConcretoNormal)
        assert c.fck == fck0

        c = ConcretoNormal(fck=fck3)
        assert isinstance(c,ConcretoNormal)
        assert c.fck == fck3

        # valores fora do limite de escopo

        fck1 = 51
        fck2 = 19

        with pytest.raises(AttributeError, match= "Attribute 'fck' must be between 20 MPa and 50 MPa to be acceptable"):
            ConcretoNormal(fck=fck1)
        
        with pytest.raises(AttributeError, match= "Attribute 'fck' must be between 20 MPa and 50 MPa to be acceptable"):
            ConcretoNormal(fck=fck2)

    def test_fcd(self):

        # definicao de variaveis
               
        fck1 = 50
        fck2 = 30
        Ec = 30000
        agregado = TipoAgregado.GRANITO
        gamma = 1.2

        fcd1 = 50/1.4
        fcd2 = 30/1.2

        # inicializacao das instancias

        concreto1 = ConcretoNormal(fck=fck1)
        concreto2 = ConcretoNormal(
                                fck=fck2, 
                                modulo_elasticidade=Ec, 
                                tipo_agregado = agregado, 
                                gamma = gamma
                            ) 

        # processo de verificacao de compatibilidade das variaveis
        
        assert concreto1.fcd == fcd1
        assert concreto2.fcd == fcd2

    def test_calcular_modulo_elasticidade_inicial(self):

        # definicao de variaveis

        fck1 = 50
        fck2 = 30
        Ec = 30000
        agregado = TipoAgregado.GRANITO
        gamma = 1.2

        # valores esperados

        Ec_esperado = TipoAgregado.BASALTO.value * 5600 * (fck1) ** 0.5

        # inicializacao das instancias

        concreto1 = ConcretoNormal(fck=fck1)
        concreto2 = ConcretoNormal(
                                fck=fck2, 
                                modulo_elasticidade=Ec, 
                                tipo_agregado = agregado, 
                                gamma = gamma
                            )

        # processo de verificacao de compatibilidade das variaveis

        assert concreto1.modulo_elasticidade_inicial == Ec_esperado
        assert concreto2.modulo_elasticidade_inicial == Ec

    def test_calcular_modulo_elasticidade_secante(self):
        
        # definicao de variaveis
        
        fck1 = 50
        fck2 = 30
        Ec = 30000
        agregado = TipoAgregado.GRANITO
        gamma = 1.2

        # valores esperados

        # NBR 6118
        # Ecs1 =  0.925 * TipoAgregado.BASALTO.value * 5600 * (fck1) ** 0.5
        # Ecs2 =  0.875 * Ec
        # Ecs3 = 0.875 * agregado.value * 5600 * (fck2) ** 0.5

        # NBR 8800
        Ecs1 =  0.85 * TipoAgregado.BASALTO.value * 5600 * (fck1) ** 0.5
        Ecs2 =  0.85 * Ec
        Ecs3 = 0.85 * agregado.value * 5600 * (fck2) ** 0.5

        # inicializacao das instancias

        concreto1 = ConcretoNormal(fck=fck1)
        concreto2 = ConcretoNormal(
                                fck=fck2, 
                                modulo_elasticidade=Ec, 
                                tipo_agregado = agregado, 
                                gamma = gamma
                            )
        
        concreto3 = ConcretoNormal(
                                fck=fck2, 
                                tipo_agregado = agregado, 
                                gamma = gamma
                            )

        # processo de verificacao de compatibilidade das variaveis

        tol = 1e-2
        assert isclose(concreto1.modulo_elasticidade_secante, Ecs1, rel_tol = tol)
        assert isclose(concreto2.modulo_elasticidade_secante, Ecs2, rel_tol = tol)
        assert isclose(concreto3.modulo_elasticidade_secante, Ecs3, rel_tol = tol)

