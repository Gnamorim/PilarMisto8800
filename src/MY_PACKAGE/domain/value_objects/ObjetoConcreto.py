from enum import Enum

class TipoAgregado(Enum):
    BASALTO = 1.2
    DIABASIO = 1.2
    GRANITO = 1.0
    GNAISSE = 1.0
    CALCARIO = 0.9
    ARENITO = 0.7


class ConcretoNormal():
    
    fck: float
    modulo_elasticidade: float
    tipo_agregado: TipoAgregado
    gamma: float
    

    def __init__(self, fck:float, modulo_elasticidade:float=0.0, tipo_agregado: TipoAgregado = TipoAgregado.BASALTO, gamma: float = 1.4):
        self.fck = fck
        self._modulo_elasticidade = modulo_elasticidade
        self.tipo_agregado = tipo_agregado
        self.gamma = gamma
        self._validate()
        self._limite_escopo()
        self.fcd = self._calcular_fcd()
        self.modulo_elasticidade_inicial = self._calcular_modulo_elasticidade_inicial()
        self.modulo_elasticidade_secante = self._calcular_modulo_elasticidade_secante()


    def _validate(self):
        if not hasattr(self, "fck"):
            raise AttributeError("Attribute 'fck' is missing.")
        if not isinstance(self.fck,(float, int)) or isinstance(self.fck, bool):
            raise TypeError('fck must be a float or an integer')
        
        if not isinstance(self.tipo_agregado, TipoAgregado):
            raise TypeError(f"Operacao deve ser do tipo TipoAgregado, recebido {type(self.tipo_agregado)}")
        
        if not hasattr(self, "_modulo_elasticidade"):
            raise AttributeError("Attribute 'modulo_elasticidade' is missing.")
        if not isinstance(self._modulo_elasticidade,(float, int)) or isinstance(self._modulo_elasticidade, bool):
            raise TypeError('modulo_elasticidade must be a float or an integer')
        
        if not hasattr(self, "gamma"):
            raise AttributeError("Attribute 'gamma' is missing.")
        if not isinstance(self.gamma,float) or isinstance(self.gamma, bool):
            raise TypeError('Gamma must be a float')
        
    def _limite_escopo(self):
        pass

    def _calcular_fcd(self):
        return self.fck / self.gamma
    
    def _calcular_modulo_elasticidade_inicial(self):
        if self._modulo_elasticidade == 0.0:
            Ec = self.tipo_agregado.value * 5600 * (self.fck) ** 0.5
            return Ec 
        else:
            return self._modulo_elasticidade
        
    def _calcular_modulo_elasticidade_secante(self):
        alfa_i = 0.8 + 0.2 * (self.fck / 80)
        if alfa_i <= 1.0:
            return alfa_i * self.modulo_elasticidade_inicial
        else:
            return self.modulo_elasticidade_inicial