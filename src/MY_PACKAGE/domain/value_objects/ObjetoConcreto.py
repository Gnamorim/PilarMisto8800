from enum import Enum
from abc import ABC, abstractmethod


# CLASSE DE DEFINICAO DO TIPO DE AGREGADO - Necessário para calculo do EC
class TipoAgregado(Enum):
    BASALTO = 1.2
    DIABASIO = 1.2
    GRANITO = 1.0
    GNAISSE = 1.0
    CALCARIO = 0.9
    ARENITO = 0.7

# CONTRATO DE CLASSE DE OBJETO

class ObjetoConcreto(ABC):
    """
    Essa e a classe abstrata que define o comportamento do concreto.

    Ela calcula a capacidade resistente de design e a validacao da classe,
    enquanto define contrato de escopo.    
    """
    
    fck: float
    modulo_elasticidade: float
    tipo_agregado: TipoAgregado
    gamma: float
    
    def __init__(
            self, 
            fck:float, 
            modulo_elasticidade:float=0.0, 
            tipo_agregado: TipoAgregado = TipoAgregado.BASALTO, 
            gamma: float = 1.4
        ):
        """
        Inicializa a Classe, automaticamente aplicando a validação e a limitacao
        de escopo do tipo de concreto considerado.

        Calcula tambem o fcd e salva em um variavel acessivel
        """

        self.fck = fck
        self._modulo_elasticidade = modulo_elasticidade
        self.tipo_agregado = tipo_agregado
        self.gamma = gamma
        self._validate()
        self._limite_escopo()
        self.fcd = self._calcular_fcd()

    def _validate(self):
        """
        Valida os parametros de entrada da classe, impedindo a criacao
        caso os tipos nao correspondam aos esperados pela classe

        Type Enforcing.
        """
        
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

    @abstractmethod    
    def _limite_escopo(self):
        pass

    def _calcular_fcd(self):
        return self.fck / self.gamma

class ConcretoNormal(ObjetoConcreto):
    
    fck: float
    modulo_elasticidade: float
    tipo_agregado: TipoAgregado
    gamma: float
    

    def __init__(
            self, 
            fck:float, 
            modulo_elasticidade:float=0.0, 
            tipo_agregado: TipoAgregado = TipoAgregado.BASALTO, 
            gamma: float = 1.4
            ):
        
        super().__init__(fck, modulo_elasticidade, tipo_agregado,gamma)
        self.modulo_elasticidade_inicial = self._calcular_modulo_elasticidade_inicial()
        self.modulo_elasticidade_secante = self._calcular_modulo_elasticidade_secante()

        
    def _limite_escopo(self):
        """
        Verifica se o concreto esta dentro do limite normativo para a classe concreta
        """

        # limite de resistencia do concreto normal
        lower_limit = 20
        upper_limit = 50
        
        if not (lower_limit <= self.fck <= upper_limit):
            raise AttributeError(f"Attribute 'fck' must be between {lower_limit} MPa and {upper_limit} MPa to be acceptable")
        
        limite_superior_Ec = 45000
        limite_inferior_Ec = 20000
    
        Ec = self._modulo_elasticidade

        if not (Ec == 0.0 or (limite_inferior_Ec <= Ec <= limite_superior_Ec)):
            raise AttributeError(
                f"Attribute 'modulo_elasticidade' must be 0.0 or between {limite_inferior_Ec} MPa and {limite_superior_Ec} MPa"
            )


    def _calcular_modulo_elasticidade_inicial(self):
        """Calcula o Eci"""
        if self._modulo_elasticidade == 0.0:
            Ec = self.tipo_agregado.value * 5600 * (self.fck) ** 0.5
            return Ec 
        else:
            return self._modulo_elasticidade
        
    def _calcular_modulo_elasticidade_secante(self):
        """Calcula o Ecs"""

        # --- da NBR 8800 ---
        return 0.85 * self.modulo_elasticidade_inicial 

        # --- Da NBR 6118 --- 
        # alfa_i = 0.8 + 0.2 * (self.fck / 80)
        # if alfa_i <= 1.0:
        #     return alfa_i * self.modulo_elasticidade_inicial
        # else:
        #     return self.modulo_elasticidade_inicial