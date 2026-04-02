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
    comprimento_pilar_destravado: float

    def __init__(self,
            diametro_tubo:float,
            espessura_tubo:float,
            comprimento_pilar_destravado: float,
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
            cobrimento,
            comprimento_pilar_destravado
            )
        
        self._validate()

        self._limite_escopo()
        
        hnz, Asnz = self._propriedades_linha_neutra_plastica_xx()
        hny, Asny = self._propriedades_linha_neutra_plastica_yy()
        self.linha_neutra_plastica_xx = hnz
        self.area_linha_neutra_plastica_xx = Asnz
        self.linha_neutra_plastica_yy = hny
        self.area_linha_neutra_plastica_yy = Asny


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
        return 0.15 * self.material_aco_estrutural.modulo_elasticidade / self.material_aco_estrutural.fy

    @property
    def esbeltez_perfil_residual_compressao(self):
        return 0.19 * self.material_aco_estrutural.modulo_elasticidade / self.material_aco_estrutural.fy

    @property
    def esbeltez_perfil_limite_flexao(self):
        return 0.09 * self.material_aco_estrutural.modulo_elasticidade / self.material_aco_estrutural.fy

    @property
    def esbeltez_perfil_residual_flexao(self):
        return 0.31 * self.material_aco_estrutural.modulo_elasticidade / self.material_aco_estrutural.fy
    
    
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
    
    # eixo xx
    @property
    def modulo_resistente_plastico_aco_x(self):
        return (1 / 6) * ((self.diametro_tubo ** 3) - (self.diametro_interno ** 3))

    @property
    def modulo_resistente_plastico_armadura_x(self):
        if self.numero_armadura_longitudinal == 0:
            return 0
        return sum( abs((np.pi / 4) * (self.diametro_armadura_longitudinal ** 2) * np.sin(n *self.theta_armadura) * self.raio_armadura) for n in range(0,self.numero_armadura_longitudinal))
    
    @property
    def modulo_resistente_plastico_concreto_x(self):
        return ((self.diametro_interno ** 3) / 4) - (2 / 3) * (((self.diametro_tubo / 2) - self.espessura_tubo) ** 3) - self.modulo_resistente_plastico_armadura_x

    # eixo yy

    @property
    def modulo_resistente_plastico_aco_y(self):
        return (1 / 6) * ((self.diametro_tubo ** 3) - (self.diametro_interno ** 3))

    @property
    def modulo_resistente_plastico_armadura_y(self):
        if self.numero_armadura_longitudinal == 0:
            return 0
        return sum( abs((np.pi / 4) * (self.diametro_armadura_longitudinal ** 2) * np.cos(n *self.theta_armadura) * self.raio_armadura) for n in range(0,self.numero_armadura_longitudinal))

    @property
    def modulo_resistente_plastico_concreto_y(self):
        return ((self.diametro_interno ** 3) / 4) - (2 / 3) * (((self.diametro_tubo / 2) - self.espessura_tubo) ** 3) - self.modulo_resistente_plastico_armadura_y    


    # propriedades da linha neutra plastica

    def _propriedades_linha_neutra_plastica_xx(self):
        Asn = 0

        if self.numero_armadura_longitudinal == 0:

            hn =((self.area_concreto() * self.fcd1 ) / (2 * self.diametro_tubo * self.fcd1 + 4 * self.espessura_tubo * (2 * self.material_aco_estrutural.resistencia_design - self.fcd1)))

            return hn, Asn

        for i in range(5):

            hn =((self.area_concreto() * self.fcd1 - Asn * (2 * self.material_armadura.resistencia_design - self.fcd1)) / (2 * self.diametro_tubo * self.fcd1 + 4 * self.espessura_tubo * (2 * self.material_aco_estrutural.resistencia_design - self.fcd1)))

            Asn1 = sum((np.pi / 4) * (self.diametro_armadura_longitudinal ** 2) for n in range(0,self.numero_armadura_longitudinal) if abs(np.sin(n * self.theta_armadura) * self.raio_armadura) <= hn)

            if abs(Asn1 - Asn) < 0.1:
                return hn, Asn1

            Asn = Asn1
        return hn, Asn
    
    def _propriedades_linha_neutra_plastica_yy(self):
        Asn = 0

        if self.numero_armadura_longitudinal == 0:

            hn =((self.area_concreto() * self.fcd1) / (2 * self.diametro_tubo * self.fcd1 + 4 * self.espessura_tubo * (2 * self.material_aco_estrutural.resistencia_design - self.fcd1)))

            return hn, Asn

        for i in range(5):

            hn =((self.area_concreto() * self.fcd1 - Asn * (2 * self.material_armadura.resistencia_design - self.fcd1)) / (2 * self.diametro_tubo * self.fcd1 + 4 * self.espessura_tubo * (2 * self.material_aco_estrutural.resistencia_design - self.fcd1)))

            Asn1 = sum((np.pi / 4) * (self.diametro_armadura_longitudinal ** 2) for n in range(0,self.numero_armadura_longitudinal) if abs(np.cos(n * self.theta_armadura) * self.raio_armadura) <= hn)

            if abs(Asn1 - Asn) < 0.1:
                return hn, Asn1

            Asn = Asn1
        return hn, Asn


    @property   
    def modulo_resistente_plastico_armadura_x_lnp(self):
        if self.numero_armadura_longitudinal == 0:
            return 0

        return sum((np.pi / 4) * (self.diametro_armadura_longitudinal ** 2) * abs(np.sin(n * self.theta_armadura) * self.raio_armadura) for n in range(0,self.numero_armadura_longitudinal) if abs(np.sin(n * self.theta_armadura) * self.raio_armadura) <= self.linha_neutra_plastica_xx)

    @property   
    def modulo_resistente_plastico_armadura_y_lnp(self):
        if self.numero_armadura_longitudinal == 0:
            return 0

        return sum((np.pi / 4) * (self.diametro_armadura_longitudinal ** 2) * abs(np.cos(n * self.theta_armadura) * self.raio_armadura) for n in range(0,self.numero_armadura_longitudinal) if abs(np.cos(n * self.theta_armadura) * self.raio_armadura) <= self.linha_neutra_plastica_yy)

    @property   
    def modulo_resistente_plastico_concreto_x_lnp(self):
        return self.diametro_interno * (self.linha_neutra_plastica_xx ** 2) - self.modulo_resistente_plastico_armadura_x_lnp

    @property   
    def modulo_resistente_plastico_concreto_y_lnp(self):
        return self.diametro_interno * (self.linha_neutra_plastica_yy ** 2) - self.modulo_resistente_plastico_armadura_y_lnp

    @property   
    def modulo_resistente_plastico_aco_x_lnp(self):
        return self.diametro_tubo * (self.linha_neutra_plastica_xx ** 2) - self.modulo_resistente_plastico_concreto_x_lnp - self.modulo_resistente_plastico_armadura_x_lnp

    @property
    def modulo_resistente_plastico_aco_y_lnp(self):
        return self.diametro_tubo * (self.linha_neutra_plastica_yy ** 2) - self.modulo_resistente_plastico_concreto_y_lnp - self.modulo_resistente_plastico_armadura_y_lnp




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


    # --- Capacidades axiais considerando esbeltez local ---

    @property
    def capacidade_axial_resistente_secao_nominal(self):

        """
        Considera o efeito da esbeltez local no comportamento axial do pilar circular
        """

        
        match self.esbeltez_compressao:
            case Secao.COMPACTO:
                return self.capacidade_axial_plastico

            case Secao.NAO_COMPACTO:

                Nyrd = ((self.material_aco_estrutural.fy * self.area_aco()) 
                + 0.7 * self.material_concreto.fck * (self.area_concreto() + self.area_armadura() 
                * (self.material_armadura.modulo_elasticidade / self.material_concreto.modulo_elasticidade_inicial)))

                termo1 = self.capacidade_axial_plastico - Nyrd

                termo2 = (( self.esbeltez_perfil - self.esbeltez_perfil_limite_compressao ) 
                          / ( self.esbeltez_perfil_residual_compressao - self.esbeltez_perfil_limite_compressao ) ** 2)

                return (self.capacidade_axial_plastico - (termo1)*(termo2))

            case Secao.ESBELTO:
                
                sigma_cr = (0.72 * self.material_aco_estrutural.fy 
                    / ((self.esbeltez_perfil * self.material_aco_estrutural.fy 
                        / self.material_aco_estrutural.modulo_elasticidade) ** 0.2))

                return ((sigma_cr * self.area_aco()) 
                        + 0.7 * self.material_concreto.fck 
                        * (self.area_concreto() + self.area_armadura() 
                            * (self.material_armadura.modulo_elasticidade / self.material_concreto.modulo_elasticidade_inicial)))

            case _:
                raise ValueError("Seção não suportada")

    @property
    def capacidade_axial_resistente_secao_design(self):

        """
        Considera o efeito da esbeltez local no comportamento axial do pilar circular
        """

        
        match self.esbeltez_compressao:
            case Secao.COMPACTO:
                return self.capacidade_axial_plastico_design

            case Secao.NAO_COMPACTO:

                Nyrd = ((self.material_aco_estrutural.resistencia_design * self.area_aco()) 
                + 0.7 * self.material_concreto.fcd * (self.area_concreto() + self.area_armadura() 
                * (self.material_armadura.modulo_elasticidade / self.material_concreto.modulo_elasticidade_inicial)))

                termo1 = self.capacidade_axial_plastico_design - Nyrd

                termo2 = (( self.esbeltez_perfil - self.esbeltez_perfil_limite_compressao ) 
                          / ( self.esbeltez_perfil_residual_compressao - self.esbeltez_perfil_limite_compressao ) ** 2)

                return (self.capacidade_axial_plastico_design - (termo1)*(termo2))

            case Secao.ESBELTO:
                
                sigma_cr = (0.72 * self.material_aco_estrutural.resistencia_design 
                    / ((self.esbeltez_perfil * self.material_aco_estrutural.resistencia_design 
                        / self.material_aco_estrutural.modulo_elasticidade) ** 0.2))

                return ((sigma_cr * self.area_aco()) 
                        + 0.7 * self.material_concreto.fcd 
                        * (self.area_concreto() + self.area_armadura() 
                            * (self.material_armadura.modulo_elasticidade / self.material_concreto.modulo_elasticidade_inicial)))

            case _:
                raise ValueError("Seção não suportada")



    
    # --- Capacidades de flexão --- 

    def capacidade_flexao_resistente_secao_nominal_xx(self):        

        """
        Considera o efeito da esbeltez local no comportamento axial do pilar circular
        """

        Mpl = self.momento_resistente_plastico_total_xx
        
        match self.esbeltez_flexao:
            case Secao.COMPACTO:

                Mrd = Mpl

                return Mrd

            case Secao.NAO_COMPACTO:

                # Merd = 1

                # termo1 = ((self.esbeltez_flexao - self.esbeltez_perfil_limite_flexao)
                #           / (self.esbeltez_perfil_residual_flexao-self.esbeltez_perfil_limite_flexao))

                # Mrd = Mpl - (Mpl-Merd) * termo1

                # return Mrd
                return ("Pilar não-compacto à flexão - Não implementado")

            case Secao.ESBELTO:
                
                # Mrd = ?

                # return Mrd
                return ("Pilar esbelto à flexão - Não implementado")

            case _:
                raise ValueError("Seção não suportada")

    def capacidade_flexao_resistente_secao_nominal_yy(self):        

        """
        Considera o efeito da esbeltez local no comportamento axial do pilar circular
        """

        Mpl = self.momento_resistente_plastico_total_yy
        
        match self.esbeltez_flexao:
            case Secao.COMPACTO:

                Mrd = Mpl

                return Mrd

            case Secao.NAO_COMPACTO:

                # Merd = 1

                # termo1 = ((self.esbeltez_flexao - self.esbeltez_perfil_limite_flexao)
                #           / (self.esbeltez_perfil_residual_flexao-self.esbeltez_perfil_limite_flexao))

                # Mrd = Mpl - (Mpl-Merd) * termo1

                # return Mrd
                return ("Pilar não-compacto à flexão - Não implementado")

            case Secao.ESBELTO:
                
                # Mrd = ?

                # return Mrd
                return ("Pilar esbelto à flexão - Não implementado")

            case _:
                raise ValueError("Seção não suportada")


    def capacidade_flexao_resistente_secao_design_xx(self):        

        """
        Considera o efeito da esbeltez local no comportamento axial do pilar circular
        """

        Mpl = self.momento_resistente_plastico_total_design_xx
        
        match self.esbeltez_flexao:
            case Secao.COMPACTO:

                Mrd = Mpl

                return Mrd

            case Secao.NAO_COMPACTO:

                # Merd = 1

                # termo1 = ((self.esbeltez_flexao - self.esbeltez_perfil_limite_flexao)
                #           / (self.esbeltez_perfil_residual_flexao-self.esbeltez_perfil_limite_flexao))

                # Mrd = Mpl - (Mpl-Merd) * termo1

                # return Mrd
                return ("Pilar não-compacto à flexão - Não implementado")

            case Secao.ESBELTO:
                
                # Mrd = ?

                # return Mrd
                return ("Pilar esbelto à flexão - Não implementado")

            case _:
                raise ValueError("Seção não suportada")

    def capacidade_flexao_resistente_secao_design_yy(self):        

        """
        Considera o efeito da esbeltez local no comportamento axial do pilar circular
        """

        Mpl = self.momento_resistente_plastico_total_design_yy
        
        match self.esbeltez_flexao:
            case Secao.COMPACTO:

                Mrd = Mpl

                return Mrd

            case Secao.NAO_COMPACTO:

                # Merd = 1

                # termo1 = ((self.esbeltez_flexao - self.esbeltez_perfil_limite_flexao)
                #           / (self.esbeltez_perfil_residual_flexao-self.esbeltez_perfil_limite_flexao))

                # Mrd = Mpl - (Mpl-Merd) * termo1

                # return Mrd
                return ("Pilar não-compacto à flexão - Não implementado")

            case Secao.ESBELTO:
                
                # Mrd = ?

                # return Mrd
                return ("Pilar esbelto à flexão - Não implementado")

            case _:
                raise ValueError("Seção não suportada")