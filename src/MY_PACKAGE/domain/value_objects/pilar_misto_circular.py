from MY_PACKAGE.domain.value_objects.ObjetoPilarMisto import ObjetoPilarMisto
from MY_PACKAGE.domain.value_objects.ObjetoConcreto import  ConcretoNormal
from MY_PACKAGE.domain.value_objects.ObjetoAco import AcoEstrutural, AcoArmadura
from MY_PACKAGE.domain.value_objects._classe_secao import Secao

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
        
        if Secao.FORA_ESCOPO in (self.esbeltez_compressao, self.esbeltez_flexao):
            raise ValueError(" esbeltez do tubo fora do limite normativo")

    
    # -------------------------------------
    # Propriedades mecânicas e Geométricas
    # -------------------------------------

    @property
    def fcd1(self):
        return self.material_concreto.fcd * 0.95 * 1


    # --- Informações Geométricas

    # Areas 

    def area_aco(self):
        return ( ( np.pi * ( (self.diametro_tubo ** 2) - (self.diametro_interno ** 2 ) ) ) / 4)
    
    def area_armadura(self):
        return ( ( np.pi * ( self.diametro_armadura_longitudinal ** 2 ) * self.numero_armadura_longitudinal ) / 4)
    
    def area_concreto(self):
        return ( ( np.pi * ( self.diametro_interno ** 2 ) ) / 4) - self.area_armadura()
    

    # Esbeltez do perfil

    @property
    def esbeltez_perfil(self):
        return self.diametro_tubo / self.espessura_tubo
    
    @property
    def esbeltez_perfil_limite_compressao(self):
        return 0.15 * self.area_aco() / self.material_aco_estrutural.fy

    @property
    def esbeltez_perfil_residual_compressao(self):
        return 0.19 * self.area_aco() / self.material_aco_estrutural.fy

    @property
    def esbeltez_perfil_limite_flexao(self):
        return 0.09 * self.area_aco() / self.material_aco_estrutural.fy

    @property
    def esbeltez_perfil_residual_flexao(self):
        return 0.31 * self.area_aco() / self.material_aco_estrutural.fy
    
    
    @property
    def esbeltez_compressao(self):
        if self.esbeltez_perfil <= self.esbeltez_perfil_limite_compressao:
            return Secao.COMPACTO
        
        elif self.esbeltez_perfil <= self.esbeltez_perfil_residual_compressao:
            return Secao.NAO_COMPACTO
        
        elif self.esbeltez_perfil <= self.esbeltez_perfil_residual_flexao:
            return Secao.ESBELTO
        
        else:
            return Secao.FORA_ESCOPO

    @property    
    def esbeltez_flexao(self):
        if self.esbeltez_perfil <= self.esbeltez_perfil_limite_flexao:
            return Secao.COMPACTO
        
        elif self.esbeltez_perfil <= self.esbeltez_perfil_residual_flexao:
            return Secao.NAO_COMPACTO
        
        else:
            return Secao.FORA_ESCOPO

    # Momentos de inercia

    @property
    def raio_armadura(self):
        """ calcula a distancia do centro ao CG da armadura"""

        return ((
            self.diametro_interno - (2 * self.cobrimento
            ) - self.diametro_armadura_longitudinal - (2 * self.diametro_armadura_transversal)
            ) / 2)

    @property
    def theta_armadura(self):
        """ calcula a angulação entre armaduras - auxiliar de momento de inercia"""

        if self.numero_armadura_longitudinal == 0:
            return 0
        return ( 2 * np.pi ) / self.numero_armadura_longitudinal
    
   

    # Eixo x - Horizontal
    
    def momento_inercia_aco_x(self):
        return ( np.pi / 64 ) * (( self.diametro_tubo ** 4 ) - ( self.diametro_interno ** 4 )) 
    
    def momento_inercia_armadura_x(self):
        
        """
        calcula o momento de inercia de armaduras em formato circular
        
        """
        
        if self.numero_armadura_longitudinal <= 0:
            return 0.0

        iz = np.pi * ( self.diametro_armadura_longitudinal ** 4 ) / 64
        iz_tot = 0.0

        for i in range(0, self.numero_armadura_longitudinal):

            a = np.pi * (( self.diametro_armadura_longitudinal ** 2 ) / 4 ) * (( self.raio_armadura * ( np.abs( np.sin( i * self.theta_armadura )))) ** 2 )

            iz_tot = iz_tot + iz + a

        return iz_tot
    
    def momento_inercia_concreto_x(self):
        return ( ( np.pi * ( self.diametro_interno ** 4 ) ) / 64 ) - self.momento_inercia_armadura_x()

   
    def momento_inercia_aco_y(self):
        return ( np.pi / 64 ) * (( self.diametro_tubo ** 4 ) - ( self.diametro_interno ** 4 ))
    
    def momento_inercia_armadura_y(self):
        """
        calcula o momento de inercia de armaduras em formato circular
        
        """
        
        if self.numero_armadura_longitudinal <= 0:
            return 0.0

        iz = np.pi * ( self.diametro_armadura_longitudinal ** 4 ) / 64
        iz_tot = 0.0

        for i in range(0, self.numero_armadura_longitudinal):

            a = np.pi * (( self.diametro_armadura_longitudinal ** 2 ) / 4 ) * (( self.raio_armadura * ( np.abs( np.cos( i * self.theta_armadura )))) ** 2 )

            iz_tot = iz_tot + iz + a

        return iz_tot   

    
    def momento_inercia_concreto_y(self):
        return ( ( np.pi * ( self.diametro_interno ** 4 ) ) / 64 ) - self.momento_inercia_armadura_y()
    
    
    # Modulo resistente plástico

    # def modulo_resistente_plastico_aco_x(self):
    #     pass

    # def modulo_resistente_plastico_concreto_x(self):
    #     pass

    # def modulo_resistente_plastico_armadura_x(self):
    #     pass

    # def modulo_resistente_plastico_aco_y(self):
    #     pass

    # def modulo_resistente_plastico_concreto_y(self):
    #     pass

    # def modulo_resistente_plastico_armadura_y(self):
    #     pass


    






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
        

