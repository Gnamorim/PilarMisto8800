from MY_PACKAGE.domain.value_objects.ObjetoPilarMisto import ObjetoPilarMisto
from MY_PACKAGE.domain.value_objects.ObjetoConcreto import  ConcretoNormal
from MY_PACKAGE.domain.value_objects.ObjetoAco import AcoEstrutural, AcoArmadura

import numpy as np

class PilarCircularPreenchido(ObjetoPilarMisto):

    material_aco_estrutural:AcoEstrutural
    material_concreto: ConcretoNormal
    material_armadura: AcoArmadura | None

    diametro_tubo:float
    espessura_tubo:float
    diametro_interno: float

    diametro_armadura_longitudinal:float
    numero_armadura_longitudinal:int
    diametro_armadura_transversal: float
    espacamento_armadura_transversal: float
    cobrimento:float

    def __init__(self,
            diametro_tubo:float,
            espessura_tubo:float,
            material_aco_estrutural:AcoEstrutural, 
            material_concreto: ConcretoNormal,
            material_armadura: AcoArmadura | None = None, # posso incluir algo como None, para quando não tiver armadura? 
            diametro_armadura_longitudinal:float = 0.0,
            numero_armadura_longitudinal:int = 0,
            diametro_armadura_transversal: float = 0.0,
            espacamento_armadura_transversal: float = 0.0,
            cobrimento:float = 0.0
        ):

        self.diametro_tubo = diametro_tubo
        self.espessura_tubo = espessura_tubo
        self.diametro_interno = diametro_tubo - 2 * espessura_tubo

        if material_armadura is None:
            diametro_armadura_longitudinal = 0.0
            numero_armadura_longitudinal = 0
            diametro_armadura_transversal = 0.0
            espacamento_armadura_transversal = 0
            cobrimento = 0.0 

        super().__init__(
            material_aco_estrutural, 
            material_concreto,
            material_armadura,
            diametro_armadura_longitudinal,
            numero_armadura_longitudinal,
            diametro_armadura_transversal,
            espacamento_armadura_transversal,
            cobrimento
            )
        
        self._validate()
        self._limite_escopo()
        
    def _validate(self):
        """
        Valida os parâmetros do pilar circular preenchido.
        """
        
        super()._validate()  # ← chama validação da classe base

        # Geometria do tubo

        for attr in ["diametro_tubo", "espessura_tubo"]:
            val = getattr(self, attr)
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                raise TypeError(f"{attr} deve ser numérico")

       
        if self.diametro_tubo <= 0:
            raise ValueError("diametro_tubo deve ser positivo")

        if self.espessura_tubo <= 0:
            raise ValueError("espessura_tubo deve ser positiva")

        if self.diametro_interno <= 0:
            raise ValueError("diametro_interno inválido (espessura muito grande)")

        if self.espessura_tubo >= self.diametro_tubo / 2:
            raise ValueError("espessura_tubo fisicamente inválida")


    def _limite_escopo(self):
        pass

    def area_aco(self):
        return ( ( np.pi * ( (self.diametro_tubo ** 2) - (self.diametro_interno ** 2 ) ) ) / 4)
    
    def area_armadura(self):
        return ( ( np.pi * ( self.diametro_armadura_longitudinal ** 2 ) * self.numero_armadura_longitudinal ) / 4)
    
    def area_concreto(self):
        return ( ( np.pi * ( self.diametro_interno ** 2 ) ) / 4) - self.area_armadura()
