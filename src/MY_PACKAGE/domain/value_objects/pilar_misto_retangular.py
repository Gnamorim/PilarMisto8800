from MY_PACKAGE.domain.value_objects.ObjetoPilarMisto import ObjetoPilarMisto
from MY_PACKAGE.domain.value_objects.ObjetoConcreto import  ConcretoNormal
from MY_PACKAGE.domain.value_objects.ObjetoAco import AcoEstrutural, AcoArmadura
from MY_PACKAGE.domain.value_objects._classe_secao import Secao

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
    comprimento_pilar_destravado: float

    def __init__(self,
            altura_tubo:float,
            largura_tubo: float,
            espessura_tubo:float,
            comprimento_pilar_destravado: float,
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
            cobrimento,
            comprimento_pilar_destravado
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

        for attr in ["altura_tubo", "largura_tubo", "espessura_tubo"]:
            val = getattr(self, attr)
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                raise TypeError(f"{attr} deve ser numérico")

       
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

        razao = self.largura_tubo / self.altura_tubo

        if not ( 0.2 <= razao <= 5.0 ):
            raise ValueError("a razão entre largura_tubo e altura_tubo deve estar entre 0.2 e 5")

        # Junta todos os resultados em uma lista única
        estados = [
            self.esbeltez_compressao,
            *self.esbeltez_flexao_XX,
            *self.esbeltez_flexao_YY,
        ]

        if Secao.FORA_ESCOPO in estados:
            raise ValueError("Esbeltez do tubo fora do limite normativo")


    # -------------------------------------
    # Propriedades mecânicas e Geométricas
    # -------------------------------------


    @property
    def fcd1(self):
        return self.material_concreto.fcd * 0.85 * 1

    @property
    def alpha_c(self):
        result = min(0.9,(
            0.45 + 3*(
                (self.area_aco + self.area_armadura) 
                / (self.area_aco + self.area_armadura + self.area_concreto)
            )
            )
        )
     
        return result
    
    @property
    def coeficiente_fluencia(self):
        return 0.6

    # --- Informações Geométricas --- 

    # Areas 

    @property
    def area_aco(self):
        return ( self.altura_tubo * self.largura_tubo - (( self.largura_tubo - 2 * self.espessura_tubo )*( self.altura_tubo - 2*self.espessura_tubo)))
    
    @property
    def area_armadura(self):
        return ( ( np.pi * ( self.diametro_armadura_longitudinal ** 2 ) * self.numero_armadura_longitudinal ) / 4)
    
    @property
    def area_concreto(self):
        return ((( self.largura_tubo - 2 * self.espessura_tubo )*( self.altura_tubo - 2*self.espessura_tubo)) - self.area_armadura)
    

    # Esbeltez do perfil

    @property
    def esbeltez_perfil_compressão(self):
       
       largura = min(self.largura_tubo, self.altura_tubo)
       
       return largura / self.espessura_tubo
    
    @property
    def esbeltez_perfil_paralelo_XX(self):
       return self.largura_tubo / self.espessura_tubo
    
    @property
    def esbeltez_perfil_paralelo_YY(self):
       return self.espessura_tubo / self.espessura_tubo
    
    @property
    def esbeltez_perfil_limite_compressao(self):
        return 2.26 * (self.material_aco_estrutural.modulo_elasticidade / self.material_aco_estrutural.fy) ** 0.5

    @property
    def esbeltez_perfil_residual_compressao(self):
        return 3.0 * (self.material_aco_estrutural.modulo_elasticidade / self.material_aco_estrutural.fy) ** 0.5

    @property
    def esbeltez_perfil_limite_flexao_alma(self):
        return 3.00 * (self.material_aco_estrutural.modulo_elasticidade / self.material_aco_estrutural.fy) ** 0.5

    @property
    def esbeltez_perfil_residual_flexao_alma(self):
        return 5.70 * (self.material_aco_estrutural.modulo_elasticidade / self.material_aco_estrutural.fy) ** 0.5
    
    @property
    def esbeltez_perfil_limite_flexao_mesa(self):
        return 2.26 * (self.material_aco_estrutural.modulo_elasticidade / self.material_aco_estrutural.fy) ** 0.5

    @property
    def esbeltez_perfil_residual_flexao_mesa(self):
        return 3.0 * (self.material_aco_estrutural.modulo_elasticidade / self.material_aco_estrutural.fy) ** 0.5
    
    @property
    def esbeltez_perfil_limite_superior(self):
        return 5.0 * (self.material_aco_estrutural.modulo_elasticidade / self.material_aco_estrutural.fy) ** 0.5
    
    
    @property
    def esbeltez_compressao(self):
        if self.esbeltez_perfil <= self.esbeltez_perfil_limite_compressao:
            return Secao.COMPACTO
        
        elif self.esbeltez_perfil <= self.esbeltez_perfil_residual_compressao:
            return Secao.NAO_COMPACTO
        
        elif self.esbeltez_perfil <= self.esbeltez_perfil_limite_superior:
            return Secao.ESBELTO
        
        else:
            return Secao.FORA_ESCOPO

    @property    
    def esbeltez_flexao_XX(self):
        if self.esbeltez_perfil_paralelo_XX <= self.esbeltez_perfil_limite_flexao_alma:
            a = Secao.COMPACTO
        
        elif self.esbeltez_perfil_paralelo_XX <= self.esbeltez_perfil_residual_flexao_alma:
            a = Secao.NAO_COMPACTO
        
        else:
            a = Secao.FORA_ESCOPO
        
        if self.esbeltez_perfil_paralelo_YY <= self.esbeltez_perfil_limite_flexao_mesa:
            b = Secao.COMPACTO
        
        elif self.esbeltez_perfil_paralelo_YY <= self.esbeltez_perfil_residual_flexao_mesa:
            b = Secao.NAO_COMPACTO
        
        elif self.esbeltez_perfil_paralelo_YY <= self.esbeltez_perfil_limite_superior:
            b = Secao.ESBELTO
        
        else:
            b = Secao.FORA_ESCOPO
        
        return [a,b]
        
    
    @property    
    def esbeltez_flexao_YY(self):
        if self.esbeltez_perfil_paralelo_YY <= self.esbeltez_perfil_limite_flexao_alma:
            a = Secao.COMPACTO
        
        elif self.esbeltez_perfil_paralelo_YY <= self.esbeltez_perfil_residual_flexao_alma:
            a = Secao.NAO_COMPACTO
        
        else:
            a = Secao.FORA_ESCOPO
        
        if self.esbeltez_perfil_paralelo_XX <= self.esbeltez_perfil_limite_flexao_mesa:
            b = Secao.COMPACTO
        
        elif self.esbeltez_perfil_paralelo_XX <= self.esbeltez_perfil_residual_flexao_mesa:
            b = Secao.NAO_COMPACTO
        
        elif self.esbeltez_perfil_paralelo_XX <= self.esbeltez_perfil_limite_superior:
            b = Secao.ESBELTO
        
        else:
            b = Secao.FORA_ESCOPO
        
        return [a,b]



    # --- Capacidades axiais ---
    # com exceção da armadura, os calculos estão implementados no ObjetoPilarMisto
    
    # Armadura
    def capacidade_axial_plastico_armadura(self):
        if self.material_armadura:
            return self.area_armadura * self.material_concreto.fck * (self.material_armadura.modulo_elasticidade/self.material_concreto.modulo_elasticidade_inicial)
        else:
            return 0.0

    def capacidade_axial_plastico_armadura_design(self):
        if self.material_armadura:
            return self.area_armadura * self.fcd1 * (self.material_armadura.modulo_elasticidade/self.material_concreto.modulo_elasticidade_inicial)
        else:
            return 0.0
