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

        # estas informações só são necessárias para flexão, não devem ser um problema        
        self.linha_neutra_plastica_xx, self.area_linha_neutra_plastica_xx = (
            self._propriedades_linha_neutra_plastica_xx()
        )

        self.linha_neutra_plastica_yy, self.area_linha_neutra_plastica_yy = (
            self._propriedades_linha_neutra_plastica_yy()
        )
        
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

        if self.numero_armadura_longitudinal % 2 != 0:
            raise ValueError("numero_armadura_longitudinal deve ser 0 ou par")
        
        if self.numero_armadura_longitudinal == 2:
            raise ValueError("numero_armadura_longitudinal deve ser 0 ou pelo menos 4")

        if self.altura_tubo <= 0:
            raise ValueError("altura_tubo deve ser positivo")

        if self.largura_tubo <= 0:
            raise ValueError("largura_tubo deve ser positivo")

        if self.espessura_tubo <= 0:
            raise ValueError("espessura_tubo deve ser positiva")

        

    def _limite_escopo(self):
        super()._limite_escopo()

        razao = self.largura_tubo / self.altura_tubo

        if not ( 0.2 <= razao <= 5.0 ):
            raise ValueError("a razão entre largura_tubo e altura_tubo deve estar entre 0.2 e 5")

        estados = [
            self.esbeltez_compressao,
            self.esbeltez_flexao_XX,
            self.esbeltez_flexao_YY,
        ]

        if Secao.FORA_ESCOPO in estados:
            raise ValueError("Esbeltez do tubo fora do limite normativo")

    @staticmethod
    def _pior_secao(*estados: Secao) -> Secao:
        severidade = {
            Secao.COMPACTO: 0,
            Secao.NAO_COMPACTO: 1,
            Secao.ESBELTO: 2,
            Secao.FORA_ESCOPO: 3,
        }
        return max(estados, key=severidade.__getitem__)


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
    def esbeltez_perfil(self):
        return self.esbeltez_perfil_compressao

    @property
    def esbeltez_perfil_compressao(self):
       
       largura = max(self.largura_tubo, self.altura_tubo)
       
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
        
        return self._pior_secao(a, b)
        
    
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
        
        return self._pior_secao(a, b)

    @property
    def esbeltez_flexao(self):
        return self._pior_secao(self.esbeltez_flexao_XX, self.esbeltez_flexao_YY)

    # Momentos de inercia

    def _distribuicao_armaduras(self):
        d = self.cobrimento + self.diametro_armadura_transversal + (self.diametro_armadura_longitudinal / 2)

        x_max = (self.largura_tubo - (self.espessura_tubo * 2)) / 2 - d
        y_max = (self.altura_tubo - (self.espessura_tubo * 2)) / 2 - d

        if self.numero_armadura_longitudinal == 0:
            return []

        coords = [
        (-x_max, -y_max),
        ( x_max, -y_max),
        ( x_max,  y_max),
        (-x_max,  y_max),
        ]
        
        restantes = self.numero_armadura_longitudinal - 4
        if restantes == 0:
            return coords

         # distribui o restante entre faces horizontais e verticais
        # tentando privilegiar o maior lado
        if self.largura_tubo >= self.altura_tubo:
            n_horiz = restantes // 2 + restantes % 4
            n_vert = restantes - n_horiz
        else:
            n_vert = restantes // 2 + restantes % 4
            n_horiz = restantes - n_vert

        # garante número par em cada par de faces
        if n_horiz % 2 != 0:
            n_horiz -= 1
            n_vert += 1

        if n_vert % 2 != 0:
            n_vert -= 1
            n_horiz += 1

        # topo e base
        barras_por_face_h = n_horiz // 2
        if barras_por_face_h > 0:
            for i in range(1, barras_por_face_h + 1):
                x = -x_max + i * (2 * x_max) / (barras_por_face_h + 1)
                coords.append((x,  y_max))
                coords.append((x, -y_max))

        # esquerda e direita
        barras_por_face_v = n_vert // 2
        if barras_por_face_v > 0:
            for i in range(1, barras_por_face_v + 1):
                y = -y_max + i * (2 * y_max) / (barras_por_face_v + 1)
                coords.append(( x_max, y))
                coords.append((-x_max, y))

        return coords    
    
    @property
    def momento_inercia_aco_x(self):
        result = (
            (self.largura_tubo * (self.altura_tubo ** 3) / 12)
            - ((self.largura_tubo - 2 * self.espessura_tubo ) 
               * ((self.altura_tubo - 2*self.espessura_tubo) ** 3) / 12)
        )
        return result

    @property
    def momento_inercia_armadura_x(self):
        if self.numero_armadura_longitudinal == 0:
            return 0
        
        iz = np.pi * ( self.diametro_armadura_longitudinal ** 4 ) / 64
        iz_tot = 0.0

        area = ( np.pi * ( self.diametro_armadura_longitudinal ** 2 ) / 4)

        lista_posicao = self._distribuicao_armaduras()

        for posicao in lista_posicao:

            a = area * (posicao[1] ** 2)

            iz_tot = iz_tot + iz + a

        return iz_tot
        
    

    @property
    def momento_inercia_concreto_x(self):
        result = (
             (self.largura_tubo - 2 * self.espessura_tubo ) 
               * ((self.altura_tubo - 2*self.espessura_tubo) ** 3) / 12
        )
        return result - self.momento_inercia_armadura_x

    @property
    def momento_inercia_aco_y(self):
        result = (
            (self.altura_tubo * (self.largura_tubo ** 3) / 12)
            - ((self.altura_tubo - 2 * self.espessura_tubo ) 
               * ((self.largura_tubo - 2*self.espessura_tubo) ** 3) / 12)
        )
        return result

    @property
    def momento_inercia_armadura_y(self):
        if self.numero_armadura_longitudinal == 0:
            return 0
        
        iz = np.pi * ( self.diametro_armadura_longitudinal ** 4 ) / 64
        iz_tot = 0.0

        area = ( np.pi * ( self.diametro_armadura_longitudinal ** 2 ) / 4)

        lista_posicao = self._distribuicao_armaduras()

        for posicao in lista_posicao:

            a = area * (posicao[0] ** 2)
            
            iz_tot = iz_tot + iz + a

        return iz_tot

    @property
    def momento_inercia_concreto_y(self):
        result = (
             ((self.largura_tubo - 2 * self.espessura_tubo ) ** 3)
               * (self.altura_tubo - 2*self.espessura_tubo) / 12
        )
        return result - self.momento_inercia_armadura_y

    # Modulo resistente plastico

    # eixo xx

    @property
    def modulo_resistente_plastico_aco_x(self):
        largura_interna = self.largura_tubo - 2 * self.espessura_tubo
        altura_interna = self.altura_tubo - 2 * self.espessura_tubo

        return (
            self.largura_tubo * (self.altura_tubo ** 2) / 4
            - largura_interna * (altura_interna ** 2) / 4
        )

    @property
    def modulo_resistente_plastico_armadura_x(self):
        if self.numero_armadura_longitudinal == 0:
            return 0
        
        area = (np.pi / 4) * (self.diametro_armadura_longitudinal ** 2)
        return sum(area * abs(posicao[1]) for posicao in self._distribuicao_armaduras())

    @property
    def modulo_resistente_plastico_concreto_x(self):
        largura_interna = self.largura_tubo - 2 * self.espessura_tubo
        altura_interna = self.altura_tubo - 2 * self.espessura_tubo

        return (
            largura_interna * (altura_interna ** 2) / 4
            - self.modulo_resistente_plastico_armadura_x
        )

    # eixo yy

    @property
    def modulo_resistente_plastico_aco_y(self):
        largura_interna = self.largura_tubo - 2 * self.espessura_tubo
        altura_interna = self.altura_tubo - 2 * self.espessura_tubo

        return (
            self.altura_tubo * (self.largura_tubo ** 2) / 4
            - altura_interna * (largura_interna ** 2) / 4
        )

    @property
    def modulo_resistente_plastico_armadura_y(self):
        if self.numero_armadura_longitudinal == 0:
            return 0
        
        area = (np.pi / 4) * (self.diametro_armadura_longitudinal ** 2)
        return sum(area * abs(posicao[0]) for posicao in self._distribuicao_armaduras())


    @property
    def modulo_resistente_plastico_concreto_y(self):
        largura_interna = self.largura_tubo - 2 * self.espessura_tubo
        altura_interna = self.altura_tubo - 2 * self.espessura_tubo

        return (
            altura_interna * (largura_interna ** 2) / 4
            - self.modulo_resistente_plastico_armadura_y
        )

    # propriedades da linha neutra plastica

    def _propriedades_linha_neutra_plastica_xx(self):
        Asn = 0

        if self.numero_armadura_longitudinal == 0:

            hn =(
                (self.area_concreto * self.fcd1)
                / (2 * self.largura_tubo * self.fcd1 + 4 * self.espessura_tubo 
                   * (2 * self.material_aco_estrutural.resistencia_design - self.fcd1))
                )

            return hn, Asn

        for i in range(5):

            hn =(
                (self.area_concreto * self.fcd1 - Asn * (2 * self.material_armadura.resistencia_design - self.fcd1)) 
                / (2 * self.largura_tubo * self.fcd1 + 4 * self.espessura_tubo 
                   * (2 * self.material_aco_estrutural.resistencia_design - self.fcd1))
                )

            Asn1 = sum(
                (np.pi / 4) * (self.diametro_armadura_longitudinal ** 2) 
                for posicao in self._distribuicao_armaduras() if abs(posicao[1]) <= hn
                )

            if abs(Asn1 - Asn) < 0.1:
                return hn, Asn1

            Asn = Asn1
        return hn, Asn
    
    def _propriedades_linha_neutra_plastica_yy(self):
        Asn = 0
        
        if self.numero_armadura_longitudinal == 0:

            hn =(
                (self.area_concreto * self.fcd1)
                / (2 * self.altura_tubo * self.fcd1 + 4 * self.espessura_tubo 
                   * (2 * self.material_aco_estrutural.resistencia_design - self.fcd1))
                )

            return hn, Asn

        for i in range(5):

            hn =(
                (self.area_concreto * self.fcd1 - Asn * (2 * self.material_armadura.resistencia_design - self.fcd1)) 
                / (2 * self.altura_tubo * self.fcd1 + 4 * self.espessura_tubo 
                   * (2 * self.material_aco_estrutural.resistencia_design - self.fcd1))
                )

            Asn1 = sum(
                (np.pi / 4) * (self.diametro_armadura_longitudinal ** 2) 
                for posicao in self._distribuicao_armaduras() if abs(posicao[0]) <= hn
                )

            if abs(Asn1 - Asn) < 0.1:
                return hn, Asn1

            Asn = Asn1
        return hn, Asn
    
    @property
    def modulo_resistente_plastico_armadura_x_lnp(self):
        if self.numero_armadura_longitudinal == 0:
            return 0

        return sum(
            (np.pi / 4) * (self.diametro_armadura_longitudinal ** 2) * abs(posicao[1])
            for posicao in self._distribuicao_armaduras() if abs(posicao[1]) <= self.linha_neutra_plastica_xx
            )

    @property   
    def modulo_resistente_plastico_armadura_y_lnp(self):
        if self.numero_armadura_longitudinal == 0:
            return 0

        return sum(
            (np.pi / 4) * (self.diametro_armadura_longitudinal ** 2) * abs(posicao[0])
            for posicao in self._distribuicao_armaduras() if abs(posicao[0]) <= self.linha_neutra_plastica_xx
            )

    @property
    def modulo_resistente_plastico_concreto_x_lnp(self):
        return (
            (self.largura_tubo - 2 * self.espessura_tubo) 
            * (self.linha_neutra_plastica_xx ** 2) 
            - self.modulo_resistente_plastico_armadura_x_lnp
            )

    @property
    def modulo_resistente_plastico_concreto_y_lnp(self):
        return (
            (self.altura_tubo - 2 * self.espessura_tubo) 
            * (self.linha_neutra_plastica_yy ** 2) 
            - self.modulo_resistente_plastico_armadura_y_lnp
            )

    @property
    def modulo_resistente_plastico_aco_x_lnp(self):
        return (
            self.largura_tubo * (self.linha_neutra_plastica_xx ** 2) 
            - self.modulo_resistente_plastico_armadura_x_lnp 
            - self.modulo_resistente_plastico_concreto_x_lnp
            )

    @property
    def modulo_resistente_plastico_aco_y_lnp(self):
        return (
            self.altura_tubo * (self.linha_neutra_plastica_yy ** 2) 
            - self.modulo_resistente_plastico_armadura_y_lnp 
            - self.modulo_resistente_plastico_concreto_y_lnp
            )



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

    @property
    def capacidade_axial_resistente_secao_nominal(self):
        """
        Considera o efeito da esbeltez local no comportamento axial do pilar circular
        """

        
        match self.esbeltez_compressao:
            case Secao.COMPACTO:
                return self.capacidade_axial_plastico()

            case Secao.NAO_COMPACTO:

                Nyrd = ((self.material_aco_estrutural.fy * self.area_aco) 
                + 0.7 * self.material_concreto.fck * (self.area_concreto + self.area_armadura 
                * (self.material_armadura.modulo_elasticidade / self.material_concreto.modulo_elasticidade_inicial)))

                termo1 = self.capacidade_axial_plastico() - Nyrd

                termo2 = (( self.esbeltez_perfil - self.esbeltez_perfil_limite_compressao ) 
                          / ( self.esbeltez_perfil_residual_compressao - self.esbeltez_perfil_limite_compressao ) ** 2)

                return (self.capacidade_axial_plastico() - (termo1)*(termo2))

            case Secao.ESBELTO:
                
                sigma_cr = (
                    (9 * self.material_concreto.modulo_elasticidade_secante)
                    / ((self.esbeltez_perfil ** 2) * 1)
                )

                return ((sigma_cr * self.area_aco) 
                        + 0.7 * self.material_concreto.fck 
                        * (self.area_concreto + self.area_armadura 
                            * (self.material_armadura.modulo_elasticidade / self.material_concreto.modulo_elasticidade_inicial)))

            case _:
                raise ValueError("Seção não suportada")

    @property
    def capacidade_axial_resistente_secao_design(self):
        """
        Considera o efeito da esbeltez local no comportamento axial do pilar circular para design
        """

        
        match self.esbeltez_compressao:
            case Secao.COMPACTO:
                return self.capacidade_axial_plastico()

            case Secao.NAO_COMPACTO:

                Nyrd = ((self.material_aco_estrutural.fy * self.area_aco) 
                + 0.7 * self.material_concreto.fck * (self.area_concreto + self.area_armadura 
                * (self.material_armadura.modulo_elasticidade / self.material_concreto.modulo_elasticidade_inicial)))

                termo1 = self.capacidade_axial_plastico() - Nyrd

                termo2 = (( self.esbeltez_perfil - self.esbeltez_perfil_limite_compressao ) 
                          / ( self.esbeltez_perfil_residual_compressao - self.esbeltez_perfil_limite_compressao ) ** 2)

                return (self.capacidade_axial_plastico() - (termo1)*(termo2))

            case Secao.ESBELTO:
                
                sigma_cr = (
                    (9 * self.material_concreto.modulo_elasticidade_secante)
                    / ((self.esbeltez_perfil ** 2) * 1.1)
                )

                return ((sigma_cr * self.area_aco) 
                        + 0.7 * self.material_concreto.fck 
                        * (self.area_concreto + self.area_armadura 
                            * (self.material_armadura.modulo_elasticidade / self.material_concreto.modulo_elasticidade_inicial)))

            case _:
                raise ValueError("Seção não suportada")
    
    # --- Capacidades de flexão --- 

    @property
    def capacidade_flexao_resistente_secao_nominal_xx(self):        

        """
        Considera o efeito da esbeltez local no comportamento axial do pilar circular
        """

        Mpl = self.momento_resistente_plastico_total_xx
        
        match self.esbeltez_flexao_XX:
            case Secao.COMPACTO:

                Mrd = Mpl

                return Mrd

            case Secao.NAO_COMPACTO:

                # Merd = 1

                # termo1 = ((self.esbeltez_flexao - self.esbeltez_perfil_limite_flexao)
                #           / (self.esbeltez_perfil_residual_flexao-self.esbeltez_perfil_limite_flexao))

                # Mrd = Mpl - (Mpl-Merd) * termo1

                # return Mrd
                raise NotImplementedError

            case Secao.ESBELTO:
                
                # Mrd = ?

                # return Mrd
                raise NotImplementedError

            case _:
                raise ValueError("Seção não suportada")

    @property
    def capacidade_flexao_resistente_secao_nominal_yy(self):        

        """
        Considera o efeito da esbeltez local no comportamento axial do pilar circular
        """

        Mpl = self.momento_resistente_plastico_total_yy
        
        match self.esbeltez_flexao_YY:
            case Secao.COMPACTO:

                Mrd = Mpl

                return Mrd

            case Secao.NAO_COMPACTO:

                # Merd = 1

                # termo1 = ((self.esbeltez_flexao - self.esbeltez_perfil_limite_flexao)
                #           / (self.esbeltez_perfil_residual_flexao-self.esbeltez_perfil_limite_flexao))

                # Mrd = Mpl - (Mpl-Merd) * termo1

                # return Mrd
                raise NotImplementedError

            case Secao.ESBELTO:
                
                # Mrd = ?

                # return Mrd
                raise NotImplementedError

            case _:
                raise ValueError("Seção não suportada")


    @property
    def capacidade_flexao_resistente_secao_design_xx(self):        

        """
        Considera o efeito da esbeltez local no comportamento axial do pilar circular
        """

        Mpl = self.momento_resistente_plastico_total_design_xx
        
        match self.esbeltez_flexao_XX:
            case Secao.COMPACTO:

                Mrd = Mpl

                return Mrd

            case Secao.NAO_COMPACTO:

                # Merd = 1

                # termo1 = ((self.esbeltez_flexao - self.esbeltez_perfil_limite_flexao)
                #           / (self.esbeltez_perfil_residual_flexao-self.esbeltez_perfil_limite_flexao))

                # Mrd = Mpl - (Mpl-Merd) * termo1

                # return Mrd
                raise NotImplementedError

            case Secao.ESBELTO:
                
                # Mrd = ?

                # return Mrd
                raise NotImplementedError

            case _:
                raise ValueError("Seção não suportada")

    @property
    def capacidade_flexao_resistente_secao_design_yy(self):        

        """
        Considera o efeito da esbeltez local no comportamento axial do pilar circular
        """

        Mpl = self.momento_resistente_plastico_total_design_yy
        
        match self.esbeltez_flexao_YY:
            case Secao.COMPACTO:

                Mrd = Mpl

                return Mrd

            case Secao.NAO_COMPACTO:

                # Merd = 1

                # termo1 = ((self.esbeltez_flexao - self.esbeltez_perfil_limite_flexao)
                #           / (self.esbeltez_perfil_residual_flexao-self.esbeltez_perfil_limite_flexao))

                # Mrd = Mpl - (Mpl-Merd) * termo1

                # return Mrd
                raise NotImplementedError

            case Secao.ESBELTO:
                
                # Mrd = ?

                # return Mrd
                raise NotImplementedError

            case _:
                raise ValueError("Seção não suportada")
