from MY_PACKAGE.domain.value_objects.ObjetoAco import LeiConstitutivaAco, AcoEstrutural, AcoArmadura
from math import isclose
import pytest

class TestObjetoAcoEstrutural:

    def test_inicializacao(self):

        fy1 = 250
        fy2 = 300
        Ey = 210000
        gamma = 1.2

        aco1 = AcoEstrutural(fy1)
        aco2 = AcoEstrutural(fy2,Ey, gamma=gamma)

        assert aco1.fy == fy1
        assert aco1.modulo_elasticidade == 200000
        assert aco1.lei_constitutiva == LeiConstitutivaAco.PLASTICOPERFEITO
        assert aco1.gamma == 1.1

        assert aco2.fy == fy2
        assert aco2.modulo_elasticidade == Ey
        assert aco2.lei_constitutiva == LeiConstitutivaAco.PLASTICOPERFEITO
        assert aco2.gamma == 1.2


    def test_validate_fy(self):
        fy1 = 'a'

        with pytest.raises(TypeError, match= 'fy must be a float or an integer'):
            AcoEstrutural(fy1)

    def test_validate_modulo_elasticidade(self):
        fy1 = 200
        Ey = 'a'

        with pytest.raises(TypeError, match= 'modulo_elasticidade must be a float or an integer'):
            AcoEstrutural(fy1, Ey)

    def test_validate_lei_constitutiva(self):
        fy1 = 200
        lei = 'a'

        with pytest.raises(TypeError, match= f"Operacao deve ser do tipo LeiConstitutivaAco, recebido {type(lei)}"):
            AcoEstrutural(fy1, lei_constitutiva=lei)

    def test_validate_gamma(self):
        fy1 = 200
        gamma = 'a'   

        with pytest.raises(TypeError, match= 'Gamma must be a float'):
             AcoEstrutural(fy1, gamma = gamma)

    def test_limite_escopo(self):
        pass

    def test_resistencia_design(self):
        fy1 = 250
        fy2 = 300
        Ey = 210000
        gamma = 1.2

        fd1 = fy1/1.1
        fd2 = fy2/gamma

        aco1 = AcoEstrutural(fy1)
        aco2 = AcoEstrutural(fy2,Ey, gamma=gamma)

        tol = 1e-2
        assert isclose(aco1.resistencia_design, fd1, rel_tol = tol)
        assert isclose(aco2.resistencia_design, fd2, rel_tol = tol)


class TestObjetoAcoArmadura():

    def test_inicializacao(self):

        fy1 = 500
        fy2 = 600
        Ey = 220000
        gamma = 1.2

        aco1 = AcoArmadura(fy1)
        aco2 = AcoArmadura(fy2,Ey, gamma=gamma)

        assert aco1.fy == fy1
        assert aco1.modulo_elasticidade == 210000
        assert aco1.lei_constitutiva == LeiConstitutivaAco.PLASTICOPERFEITO
        assert aco1.gamma == 1.15

        assert aco2.fy == fy2
        assert aco2.modulo_elasticidade == Ey
        assert aco2.lei_constitutiva == LeiConstitutivaAco.PLASTICOPERFEITO
        assert aco2.gamma == 1.2


    def test_validate_fy(self):
        fy1 = 'a'

        with pytest.raises(TypeError, match= 'fy must be a float or an integer'):
            AcoArmadura(fy1)

    def test_validate_modulo_elasticidade(self):
        fy1 = 500
        Ey = 'a'

        with pytest.raises(TypeError, match= 'modulo_elasticidade must be a float or an integer'):
            AcoArmadura(fy1, Ey)

    def test_validate_lei_constitutiva(self):
        fy1 = 500
        lei = 'a'

        with pytest.raises(TypeError, match= f"Operacao deve ser do tipo LeiConstitutivaAco, recebido {type(lei)}"):
            AcoArmadura(fy1, lei_constitutiva=lei)

    def test_validate_gamma(self):
        fy1 = 500
        gamma = 'a'   

        with pytest.raises(TypeError, match= 'Gamma must be a float'):
             AcoArmadura(fy1, gamma = gamma)

    def test_limite_escopo(self):
        pass

    def test_resistencia_design(self):
        fy1 = 500
        fy2 = 600
        Ey = 210000
        gamma = 1.2

        fd1 = fy1/1.15
        fd2 = fy2/gamma

        aco1 = AcoArmadura(fy1)
        aco2 = AcoArmadura(fy2,Ey, gamma=gamma)

        tol = 1e-2
        assert isclose(aco1.resistencia_design, fd1, rel_tol = tol)
        assert isclose(aco2.resistencia_design, fd2, rel_tol = tol)