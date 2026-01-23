from enum import Enum
from abc import ABC, abstractmethod

class LeiConstitutivaAco(Enum):

    # criado para implementação posterior (seção genérica com integração)
    PLASTICOPERFEITO = 1


class ObjetoAco(ABC):

    @abstractmethod
    def _validate(self):
        pass

    @abstractmethod
    def _limite_escopo(self):
        pass

    @abstractmethod
    def _calcular_fyd(self):
        pass

class AcoEstrutural(ObjetoAco):

    fy: float
    modulo_elasticidade: float
    lei_constitutiva: LeiConstitutivaAco
    gamma: float

    def __init__(self,fy: float, modulo_elasticidade:float = 200000, lei_constitutiva: LeiConstitutivaAco = LeiConstitutivaAco.PLASTICOPERFEITO, gamma: float = 1.1):
        self.fy = fy
        self.modulo_elasticidade = modulo_elasticidade
        self.lei_constitutiva = lei_constitutiva
        self.gamma = gamma
        self._validate()
        self._limite_escopo()
        self.resistencia_design = self._calcular_fyd()

    def _validate(self):
        if not hasattr(self, "fy"):
            raise AttributeError("Attribute 'fy' is missing.")
        if not isinstance(self.fy,(float, int)) or isinstance(self.fy, bool):
            raise TypeError('fy must be a float or an integer')
        
        if not hasattr(self, "modulo_elasticidade"):
            raise AttributeError("Attribute 'modulo_elasticidade' is missing.")
        if not isinstance(self.modulo_elasticidade,(float, int)) or isinstance(self.modulo_elasticidade, bool):
            raise TypeError('modulo_elasticidade must be a float or an integer')
        
        if not isinstance(self.lei_constitutiva, LeiConstitutivaAco):
            raise TypeError(f"Operacao deve ser do tipo LeiConstitutivaAco, recebido {type(self.lei_constitutiva)}")
        
        if not hasattr(self, "gamma"):
            raise AttributeError("Attribute 'gamma' is missing.")
        if not isinstance(self.gamma,float) or isinstance(self.gamma, bool):
            raise TypeError('Gamma must be a float')
        
    def _limite_escopo(self):
        pass

    def _calcular_fyd(self):
        return self.fy / self.gamma
    

class AcoArmadura(ObjetoAco):

    fy: float
    modulo_elasticidade: float
    lei_constitutiva: LeiConstitutivaAco
    gamma: float

    def __init__(self,fy: float, modulo_elasticidade:float = 210000, lei_constitutiva: LeiConstitutivaAco = LeiConstitutivaAco.PLASTICOPERFEITO, gamma: float = 1.15):
        self.fy = fy
        self.modulo_elasticidade = modulo_elasticidade
        self.lei_constitutiva = lei_constitutiva
        self.gamma = gamma
        self._validate()
        self._limite_escopo()
        self.resistencia_design = self._calcular_fyd()

    def _validate(self):
        if not hasattr(self, "fy"):
            raise AttributeError("Attribute 'fy' is missing.")
        if not isinstance(self.fy,(float, int)) or isinstance(self.fy, bool):
            raise TypeError('fy must be a float or an integer')
        
        if not hasattr(self, "modulo_elasticidade"):
            raise AttributeError("Attribute 'modulo_elasticidade' is missing.")
        if not isinstance(self.modulo_elasticidade,(float, int)) or isinstance(self.modulo_elasticidade, bool):
            raise TypeError('modulo_elasticidade must be a float or an integer')
        
        if not isinstance(self.lei_constitutiva, LeiConstitutivaAco):
            raise TypeError(f"Operacao deve ser do tipo LeiConstitutivaAco, recebido {type(self.lei_constitutiva)}")
        
        if not hasattr(self, "gamma"):
            raise AttributeError("Attribute 'gamma' is missing.")
        if not isinstance(self.gamma,float) or isinstance(self.gamma, bool):
            raise TypeError('Gamma must be a float')
        
    def _limite_escopo(self):
        pass

    def _calcular_fyd(self):
        return self.fy / self.gamma
        



    