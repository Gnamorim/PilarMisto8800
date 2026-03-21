from MY_PACKAGE.domain.value_objects.ObjetoPilarMisto import ObjetoPilarMisto
from MY_PACKAGE.domain.value_objects.ObjetoConcreto import  ConcretoNormal
from MY_PACKAGE.domain.value_objects.ObjetoAco import AcoEstrutural, AcoArmadura

import numpy as np

class PilarRetangularPreenchido(ObjetoPilarMisto):

    altura_tubo:float
    largura_tubo:float
    espessura_tubo:float

    material_aco_estrutural:AcoEstrutural
    material_concreto: ConcretoNormal
    material_armadura: AcoArmadura | None

    diametro_armadura_longitudinal:float
    numero_armadura_longitudinal:int
    diametro_armadura_transversal: float
    espacamento_armadura_transversal: float
    cobrimento:float

    def __init__(self,
            altura_tubo:float,
            largura_tubo: float,
            espessura_tubo:float,
            material_aco_estrutural:AcoEstrutural, 
            material_concreto: ConcretoNormal,
            material_armadura: AcoArmadura | None = None,
            diametro_armadura_longitudinal:float = 0.0,
            numero_armadura_longitudinal:int = 0,
            diametro_armadura_transversal: float = 0.0,
            espacamento_armadura_transversal: float = 0.0,
            cobrimento:float = 0.0
        ):

        self.altura_tubo = altura_tubo
        self.largura_tubo = largura_tubo
        self.espessura_tubo = espessura_tubo

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
        super()._limite_escopo()


    # -------------------------------------
    # Propriedades mecânicas e Geométricas
    # -------------------------------------


    @property
    def fcd1(self):
        return self.material_concreto.fcd * 0.85 * 1


    # --- Informações Geométricas --- 
    def area_aco(self):
        return ( self.altura_tubo * self.largura_tubo - (( self.largura_tubo - 2 * self.espessura_tubo )*( self.altura_tubo - 2*self.espessura_tubo)))
    
    def area_armadura(self):
        return ( ( np.pi * ( self.diametro_armadura_longitudinal ** 2 ) * self.numero_armadura_longitudinal ) / 4)
    
    def area_concreto(self):
        return ((( self.largura_tubo - 2 * self.espessura_tubo )*( self.altura_tubo - 2*self.espessura_tubo)) - self.area_armadura())
    
    

    # --- Capacidades axiais ---
    # com exceção da armadura, os calculos estão implementados no ObjetoPilarMisto
    
    # Armadura
    def capacidade_axial_plastico_armadura(self):
        if self.material_armadura:
            return self.area_armadura() * self.material_concreto.fck * (self.material_armadura.modulo_elasticidade/self.material_concreto.modulo_elasticidade_inicial)
        else:
            return 0.0

    def capacidade_axial_plastico_armadura_design(self):
        if self.material_armadura:
            return self.area_armadura() * self.fcd1 * (self.material_armadura.modulo_elasticidade/self.material_concreto.modulo_elasticidade_inicial)
        else:
            return 0.0
