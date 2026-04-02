from MY_PACKAGE.domain.value_objects.ObjetoPilarMisto import ObjetoPilarMisto
from MY_PACKAGE.domain.value_objects.ObjetoConcreto import  ConcretoNormal
from MY_PACKAGE.domain.value_objects.ObjetoAco import AcoEstrutural, AcoArmadura

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


    diametro_armadura_longitudinal:float
    numero_armadura_longitudinal:int
    diametro_armadura_transversal: float
    espacamento_armadura_transversal: int
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
            material_armadura: AcoArmadura,
            
            diametro_armadura_longitudinal:float = 0.0,
            numero_armadura_longitudinal:int = 0,
            diametro_armadura_transversal: float = 0.0,
            espacamento_armadura_transversal: int = 0,
            cobrimento:float = 0.0
        ):

        self.altura_concreto = altura_concreto
        self.largura_concreto =largura_concreto
        self.altura_perfil = altura_perfil
        self.largura_perfil = largura_perfil
        self.espessura_mesa = espessura_mesa
        self.espessura_alma = espessura_alma
        self.cx = (self.largura_concreto - self.largura_perfil) /2
        self.cy = (self.altura_concreto - self.altura_perfil) /2

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



    # -----------------------------------------------
    #
    # Funções de validação e limitação de escopo
    #
    # -----------------------------------------------


    def _validate(self):
        """
        Valida os parâmetros do pilar circular preenchido.
        """
        
        super()._validate()  # ← chama validação da classe base

        # Geometria do tubo

        # for attr in ["diametro_tubo", "espessura_tubo"]:
        #     val = getattr(self, attr)
        #     if not isinstance(val, (int, float)) or isinstance(val, bool):
        #         raise TypeError(f"{attr} deve ser numérico")

       
        # if self.diametro_tubo <= 0:
        #     raise ValueError("diametro_tubo deve ser positivo")

        # if self.espessura_tubo <= 0:
        #     raise ValueError("espessura_tubo deve ser positiva")

        # if self.diametro_interno <= 0:
        #     raise ValueError("diametro_interno inválido (espessura muito grande)")

        # if self.espessura_tubo >= self.diametro_tubo / 2:
        #     raise ValueError("espessura_tubo fisicamente inválida")



    def _limite_escopo(self):
        super()._limite_escopo()

        limite = min(self.largura_perfil, 40)

        if self.cx < limite or self.cy < limite:
            raise ValueError("cobrimento do perfil menor que o minimo normativo")


    # -------------------------------------
    # Propriedades mecânicas e Geométricas
    # -------------------------------------

        
    @property
    def fcd1(self):
        alpha = ((40/self.material_concreto.fck)**(1/3)) 
        if alpha >= 1:
            alpha = 1
        return self.material_concreto.fcd * 0.85 * alpha

    @property
    def alpha_c(self):
        result = min(0.7,(
            0.25 + 3*(
                (self.area_aco + self.area_armadura) 
                / (self.area_aco + self.area_armadura + self.area_concreto)
            )
            )
        )
     
        return result

    # --- Informações Geométricas --- 
    def area_aco(self):
        return ( 2 * (self.largura_perfil * self.espessura_mesa) + ( self.espessura_alma * ( self.altura_perfil - 2 * self.espessura_mesa)))
                
    def area_armadura(self):
        return (( np.pi * ( self.diametro_armadura_longitudinal ** 2 ) * self.numero_armadura_longitudinal ) / 4)
    
    def area_concreto(self):
        return (( self.altura_concreto * self.largura_concreto ) - self.area_armadura() - self.area_aco())
    


    # --- Capacidades axiais ---
    # com exceção da armadura, os calculos estão implementados no ObjetoPilarMisto

    # Armadura
    def capacidade_axial_plastico_armadura(self):
        if self.material_armadura:
            return self.area_armadura() * self.material_armadura.fy
        else:
            return 0.0

    def capacidade_axial_plastico_armadura_design(self):
        if self.material_armadura:
            return self.area_armadura() * self.material_armadura.resistencia_design
        else:
            return 0.0
        
