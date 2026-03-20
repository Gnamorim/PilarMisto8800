from enum import Enum
from abc import ABC, abstractmethod

class LeiConstitutivaAco(Enum):

    # criado para implementação posterior (seção genérica com integração)
    PLASTICOPERFEITO = 1


class ObjetoAco(ABC):

    def __init__(self, fy: float, modulo_elasticidade: float, lei_constitutiva: LeiConstitutivaAco, gamma: int):
        self.fy = fy
        self.modulo_elasticidade = modulo_elasticidade
        self.lei_constitutiva = lei_constitutiva
        self.gamma = gamma

    def _validate(self):
        """
        Valida os parametros de entrada da classe, impedindo a criacao
        caso os tipos nao correspondam aos esperados pela classe

        Type Enforcing.
        """
        
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

    @abstractmethod
    def _limite_escopo(self):
        pass

    
    def _calcular_fyd(self):
        return (self.fy / self.gamma)

class AcoEstrutural(ObjetoAco):

    fy: float
    modulo_elasticidade: float
    lei_constitutiva: LeiConstitutivaAco
    gamma: float
    resistencia_design: float

    def __init__(self,fy: float, modulo_elasticidade:float = 200000, lei_constitutiva: LeiConstitutivaAco = LeiConstitutivaAco.PLASTICOPERFEITO, gamma: float = 1.1):
        super().__init__(fy, modulo_elasticidade, lei_constitutiva, gamma)
        self._validate()
        self._limite_escopo()
        self.resistencia_design = self._calcular_fyd()
  
    def _limite_escopo(self):
        """
        Verifica se o aco esta dentro dos limites da NBR 8800
        """

        limite_superior_fy = 450
        limite_inferior_fy = 250
        limite_superior_Es = 250000
        limite_inferior_Es = 170000

        if not (limite_inferior_fy <= self.fy <= limite_superior_fy):
            raise AttributeError(f"Attribute 'fy' must be between {limite_inferior_fy} MPa and {limite_superior_fy} MPa to be acceptable")
        
        if not (self.modulo_elasticidade == 0.0 or limite_inferior_Es <= self.modulo_elasticidade <= limite_superior_Es):
            raise AttributeError(f"Attribute 'modulo_elasticidade' must be between {limite_inferior_Es} MPa and {limite_superior_Es} MPa to be acceptable")

  

class AcoArmadura(ObjetoAco):

    fy: float
    modulo_elasticidade: float
    lei_constitutiva: LeiConstitutivaAco
    gamma: float
    resistencia_design: float

    def __init__(self,fy: float, modulo_elasticidade:float = 210000, lei_constitutiva: LeiConstitutivaAco = LeiConstitutivaAco.PLASTICOPERFEITO, gamma: float = 1.15):
        super().__init__(fy, modulo_elasticidade, lei_constitutiva, gamma)
        self._validate()
        self._limite_escopo()
        self.resistencia_design = self._calcular_fyd()


        
    def _limite_escopo(self):
        """
        Verifica se o aco esta dentro dos limites da NBR 6118
        """

        limite_superior_fy = 600
        limite_inferior_fy = 250
        limite_superior_Es = 250000
        limite_inferior_Es = 170000

        if not (limite_inferior_fy <= self.fy <= limite_superior_fy):
            raise AttributeError(f"Attribute 'fy' must be between {limite_inferior_fy} MPa and {limite_superior_fy} MPa to be acceptable")
        
        if not (limite_inferior_Es <= self.modulo_elasticidade <= limite_superior_Es):
            raise AttributeError(f"Attribute 'modulo_elasticidade' must be between {limite_inferior_Es} MPa and {limite_superior_Es} MPa to be acceptable")
   