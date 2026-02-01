from ObjetoPilarMisto import ObjetoPilarMisto
from ObjetoConcreto import  ConcretoNormal
from ObjetoAco import AcoEstrutural, AcoArmadura

import numpy as np

class PilarRetangularPreenchido(ObjetoPilarMisto):

    material_aco_estrutural:AcoEstrutural
    material_concreto: ConcretoNormal
    material_armadura: AcoArmadura

    altura_tubo:float
    largura_tubo:float
    espessura_tubo:float
    
    diametro_armadura_longitudinal:float
    numero_armadura_longitudinal:int
    diametro_armadura_transversal: float
    numero_armadura_transversal: int
    cobrimento:float

    def __init__(self,
            altura_tubo:float,
            largura_tubo: float,
            espessura_tubo:float,
            material_aco_estrutural:AcoEstrutural, 
            material_concreto: ConcretoNormal,
            material_armadura: AcoArmadura, # posso incluir algo como None, para quando não tiver armadura? 
            diametro_armadura_longitudinal:float = 0.0,
            numero_armadura_longitudinal:int = 0,
            diametro_armadura_transversal: float = 0.0,
            numero_armadura_transversal: int = 0,
            cobrimento:float = 0.0
        ):

        self.altura_tubo = altura_tubo
        self.largura_tubo = largura_tubo
        self.espessura_tubo = espessura_tubo
        self.material_aco_estrutural = material_aco_estrutural
        self.material_concreto = material_concreto
        self.material_armadura = material_armadura
        self.diametro_armadura_longitudinal = diametro_armadura_longitudinal
        self.numero_armadura_longitudinal = numero_armadura_longitudinal
        self.diametro_armadura_transversal = diametro_armadura_transversal
        self.numero_armadura_transversal = numero_armadura_transversal
        self.cobrimento = cobrimento
        self._validate()
        

    def _validate(self):
        pass

    def _limite_escopo(self):
        pass

    def area_aco(self):
        return ( self.altura_tubo * self.largura_tubo - (( self.largura_tubo - 2 * self.espessura_tubo )*( self.altura_tubo - 2*self.espessura_tubo)))
    
    def area_armadura(self):
        return ( ( np.pi * ( self.diametro_armadura_longitudinal ** 2 ) * self.numero_armadura_longitudinal ) / 4)
    
    def area_concreto(self):
        return ((( self.largura_tubo - 2 * self.espessura_tubo )*( self.altura_tubo - 2*self.espessura_tubo)) - self.area_armadura())
