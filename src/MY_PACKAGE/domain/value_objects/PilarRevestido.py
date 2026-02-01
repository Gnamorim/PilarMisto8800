from ObjetoPilarMisto import ObjetoPilarMisto
from ObjetoConcreto import  ConcretoNormal
from ObjetoAco import AcoEstrutural, AcoArmadura

import numpy as np

class PilarRevestido(ObjetoPilarMisto):

    material_aco_estrutural:AcoEstrutural
    material_concreto: ConcretoNormal
    material_armadura: AcoArmadura

    altura_concreto:float
    largura_concreto:float
    altura_perfil:float
    largura_perfil:float
    espessura_mesa:float
    espessura_alma:float
    cx: float # não tenho nomenclatura adequada
    cy: float # não tenho nomenclatura adequada - ver imagem M1 da norma

    diametro_armadura_longitudinal:float
    numero_armadura_longitudinal:int
    diametro_armadura_transversal: float
    numero_armadura_transversal: int
    cobrimento:float

    def __init__(self,
            altura_concreto:float,
            largura_concreto:float,
            altura_perfil:float,
            largura_perfil:float,
            espessura_mesa:float,
            espessura_alma:float,
            cx: float, # não tenho nomenclatura adequada
            cy: float, # não tenho nomenclatura adequada - ver imagem M1 da norma
            material_aco_estrutural:AcoEstrutural, 
            material_concreto: ConcretoNormal,
            material_armadura: AcoArmadura, # posso incluir algo como None, para quando não tiver armadura? 
            diametro_armadura_longitudinal:float = 0.0,
            numero_armadura_longitudinal:int = 0,
            diametro_armadura_transversal: float = 0.0,
            numero_armadura_transversal: int = 0,
            cobrimento:float = 0.0
        ):

        self.altura_concreto = altura_concreto
        self.largura_concreto =largura_concreto
        self.altura_perfil = altura_perfil
        self.largura_perfil = largura_perfil       
        self.espessura_mesa = espessura_mesa
        self.espessura_alma = espessura_alma
        self.cx = cx
        self.cy = cy
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
        return ( 2 * (self.largura_perfil * self.espessura_mesa) + ( self.espessura_alma * ( self.altura_perfil - 2 * self.espessura_mesa)))
    
    def area_armadura(self):
        return ( ( np.pi * ( self.diametro_armadura_longitudinal ** 2 ) * self.numero_armadura_longitudinal ) / 4)
    
    def area_concreto(self):
        return (( self.altura_concreto * self.largura_concreto ) - self.area_armadura() - self.area_aco())
