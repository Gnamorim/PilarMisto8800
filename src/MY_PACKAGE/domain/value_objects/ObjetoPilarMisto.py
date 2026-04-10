from abc import ABC, abstractmethod
from math import pi

from MY_PACKAGE.domain.value_objects.ObjetoConcreto import  ConcretoNormal
from MY_PACKAGE.domain.value_objects.ObjetoAco import AcoEstrutural, AcoArmadura

class ObjetoPilarMisto(ABC):

    """
    Esta é uma classe abstrata base, que carrega todos os métodos compartilhados entre os pilares mistos
    Também estabelece contratos entre os nomes de propriedades e metodos necessários a todas as implementações concretas

    Usado para o Service de flexo-compressão.
    """

    #  inicializaco das variaves existentes em todos os modelos
    def __init__(
            self,
            material_aco_estrutural:AcoEstrutural,
            material_concreto: ConcretoNormal,
            material_armadura: AcoArmadura,
            diametro_armadura_longitudinal:float,
            numero_armadura_longitudinal:int,
            diametro_armadura_transversal: float,
            espacamento_armadura_transversal: float,
            cobrimento:float,
            comprimento_pilar_destravado: float
            
        ):

        self.material_aco_estrutural = material_aco_estrutural
        self.material_concreto = material_concreto
        self.material_armadura = material_armadura
        self.diametro_armadura_longitudinal = diametro_armadura_longitudinal
        self.numero_armadura_longitudinal = numero_armadura_longitudinal
        self.diametro_armadura_transversal = diametro_armadura_transversal
        self.espacamento_armadura_transversal = espacamento_armadura_transversal
        self.cobrimento = cobrimento
        self.comprimento_pilar_destravado = comprimento_pilar_destravado

        

    # FUNÇÕES DE VALIDAÇÃO

    @abstractmethod
    def _validate(self):
        """
        Validação base comum a todos os pilares.
        """

        # Tipos básicos

        if not isinstance(self.material_aco_estrutural, AcoEstrutural):
            raise TypeError("material_aco_estrutural deve ser AcoEstrutural")

        if not isinstance(self.material_concreto, ConcretoNormal):
            raise TypeError("material_concreto deve ser ConcretoNormal")

        if self.material_armadura is not None and not isinstance(self.material_armadura, AcoArmadura):
            raise TypeError("material_armadura deve ser AcoArmadura ou None")
        

        # Tipos

        if not isinstance(self.diametro_armadura_longitudinal, (int, float)) or isinstance(self.diametro_armadura_longitudinal, bool):
            raise TypeError("diametro_armadura_longitudinal deve ser numérico")

        if not isinstance(self.diametro_armadura_transversal, (int, float)) or isinstance(self.diametro_armadura_transversal, bool):
            raise TypeError("diametro_armadura_transversal deve ser numérico")

        if not isinstance(self.numero_armadura_longitudinal, int):
            raise TypeError("numero_armadura_longitudinal deve ser inteiro")

        if not isinstance(
            self.espacamento_armadura_transversal, (int, float)
            ) or isinstance(self.espacamento_armadura_transversal, bool):
            
            raise TypeError("espacamento_armadura_transversal deve ser numérico")

        if not isinstance(self.cobrimento, (int, float)) or isinstance(self.cobrimento, bool):
            raise TypeError("cobrimento deve ser numérico")


        # -------------------------
        # Consistência da armadura
        # -------------------------

        if self.material_armadura is None:
            if any([
                self.diametro_armadura_longitudinal != 0,
                self.numero_armadura_longitudinal != 0,
                self.diametro_armadura_transversal != 0,
                self.espacamento_armadura_transversal != 0,
                self.cobrimento != 0
            ]):
                raise ValueError(
                    "Sem armadura → todos os parâmetros de armadura devem ser zero"
                )

        else:
            # Se existe armadura → valores devem ser positivos
            if self.diametro_armadura_longitudinal <= 0:
                raise ValueError("diametro_armadura_longitudinal deve ser > 0")

            if self.numero_armadura_longitudinal <= 0:
                raise ValueError("numero_armadura_longitudinal deve ser > 0")

            if self.diametro_armadura_transversal <= 0:
                raise ValueError("diametro_armadura_transversal deve ser > 0")

            if self.espacamento_armadura_transversal <= 0:
                raise ValueError("espacamento_armadura_transversal deve ser > 0")

            if self.cobrimento <= 0:
                raise ValueError("cobrimento deve ser > 0")
        
      
        # Valores físicos - limites construtivos - REFINAR

        if self.diametro_armadura_longitudinal > 50:
            raise ValueError("diametro_armadura_longitudinal deve <= 50 mm")
        
        if self.material_armadura is not None:
            if self.diametro_armadura_longitudinal < 5:
                raise ValueError("diametro_armadura_longitudinal muito pequeno")

        if self.numero_armadura_longitudinal > 30:
            raise ValueError("numero_armadura_longitudinal deve ser <= 30")  # upper number aleatorio - definir algo que faca mais sentido

        if self.diametro_armadura_transversal > 50:
            raise ValueError("diametro_armadura_transversal deve ser <= 50 mm")
        
        if self.material_armadura is not None:
            if self.diametro_armadura_transversal < 5:
                raise ValueError("diametro_armadura_transversal muito pequeno")

        if self.espacamento_armadura_transversal > 1000:
            raise ValueError("espacamento_armadura_transversal deve ser <= 1000 mm") # upper number aleatorio - definir algo que faca mais sentido

        if self.cobrimento < 0:
            raise ValueError("cobrimento deve ser positivo")
        
    @property
    @abstractmethod
    def fcd1(self):
        pass


    @abstractmethod
    def _limite_escopo(self):
        """
        Avalia o pilar dentro do escopo do metodo simplificado da norma. Comum a todos os pilares
        """
        
        # --- area perfil >1% da area total ---
        area_aco = self.area_aco
        area_concreto = self.area_concreto
        area_armadura = self.area_armadura 

        area_total = area_aco + area_concreto + area_armadura

        razao_perfil = area_aco / area_total

        if razao_perfil < 0.01:
            raise ValueError("Area de aço inferior ao mínimo de 1% da area total")
        
        # --- fator de contribuição entre 0.1 e 0.9

        NaplRd = self.capacidade_axial_plastico_aco_design()
        NplRd = self.capacidade_axial_plastico_design()

        fator_contribuicao = NaplRd/NplRd

        if not (0.1 <= fator_contribuicao <= 0.9):
            raise ValueError("fator de contribuição fora do limite normativo")
        
        # --- esbeltez reduzida inferior a 2.0 ---

        if self.indice_esbeltez_reduzido > 2.0:
            raise ValueError("Esbeltez reduzida do pilar esta fora do limite normativo")


        

    # PROPRIEDADES GEOMETRICAS

    # area
     
    @property
    @abstractmethod
    def area_aco(self):
        pass

    @property
    @abstractmethod
    def area_concreto(self):
        pass

    @property
    @abstractmethod
    def area_armadura(self):
        pass

    def area_total(self):
        """
        Calcula a area total da seção tranversal do pilar
        """
        return self.area_concreto + self.area_aco + self.area_armadura 

    # momento de inercia

    @property
    @abstractmethod
    def momento_inercia_aco_x(self):
        pass

    @property
    @abstractmethod
    def momento_inercia_concreto_x(self):
        pass
    
    @property
    @abstractmethod
    def momento_inercia_armadura_x(self):
        pass

    @property
    @abstractmethod
    def momento_inercia_aco_y(self):
        pass

    @property
    @abstractmethod
    def momento_inercia_concreto_y(self):
        pass
    
    @property
    @abstractmethod
    def momento_inercia_armadura_y(self):
        pass    

    @property
    @abstractmethod
    def esbeltez_perfil(self):
        pass

    # modulo resistente plastico

    @property
    @abstractmethod
    def modulo_resistente_plastico_aco_x(self):
        pass

    @property
    @abstractmethod
    def modulo_resistente_plastico_concreto_x(self):
        pass

    @property
    @abstractmethod
    def modulo_resistente_plastico_armadura_x(self):
        pass

    @property
    @abstractmethod
    def modulo_resistente_plastico_aco_y(self):
        pass

    @property
    @abstractmethod
    def modulo_resistente_plastico_concreto_y(self):
        pass

    @property
    @abstractmethod
    def modulo_resistente_plastico_armadura_y(self):
        pass

    
    @property
    @abstractmethod
    def modulo_resistente_plastico_aco_x_lnp(self):
        pass

    @property
    @abstractmethod
    def modulo_resistente_plastico_concreto_x_lnp(self):
        pass

    @property
    @abstractmethod
    def modulo_resistente_plastico_armadura_x_lnp(self):
        pass

    @property
    @abstractmethod
    def modulo_resistente_plastico_aco_y_lnp(self):
        pass

    @property
    @abstractmethod
    def modulo_resistente_plastico_concreto_y_lnp(self):
        pass

    @property
    @abstractmethod
    def modulo_resistente_plastico_armadura_y_lnp(self):
        pass

    # -------------------------------
    # Rijezas efetivas
    # -------------------------------

    # axial

    @property
    def rigidez_axial_aco(self):
        """Calcula a rigidez axial do aço estrutural"""
        return (self.area_aco * self.material_aco_estrutural.modulo_elasticidade)

    @property
    def rigidez_axial_concreto(self):
        """Calcula a rigidez axial do concreto"""
        return (self.area_concreto * self.material_concreto.modulo_elasticidade_secante)
    
    @property
    def rigidez_axial_armadura(self):
        """ Calcula a rigidez axial da armadura"""
        return (self.area_armadura * self.material_armadura.modulo_elasticidade)
    
    @property
    def rigidez_axial_equivalente(self):
        """
        Calcula a rigidez axial equivalente do pilar (EA)e
        """
        return (self.rigidez_axial_aco + self.rigidez_axial_armadura + self.rigidez_axial_concreto)
    
    # flexão

    @property
    @abstractmethod
    def alpha_c(self):
        pass

    @property
    @abstractmethod
    def coeficiente_fluencia(self):
        pass

    @property
    def rigidez_flexao_equivalente_x(self):
        """
        Calcula a rigidez equivalente a flexão (EI)e em relação ao eixo X
        """
        aco = (self.momento_inercia_aco_x * self.material_aco_estrutural.modulo_elasticidade)
        if self.material_armadura is not None:
            armadura = (self.momento_inercia_armadura_x * self.material_armadura.modulo_elasticidade)
        else:
            armadura = 0
        concreto = self.alpha_c * (self.momento_inercia_concreto_x * self.material_concreto.modulo_elasticidade_secante)

        return (concreto + aco + armadura)
    
    @property
    def rigidez_flexao_equivalente_y(self):
        """
        Calcula a rigidez equivalente a flexão (EI)e em relação ao eixo Y
        """
        aco = (self.momento_inercia_aco_y * self.material_aco_estrutural.modulo_elasticidade)
        if self.material_armadura is not None:
            armadura = (self.momento_inercia_armadura_y * self.material_armadura.modulo_elasticidade)
        else: 
            armadura = 0
        concreto = self.alpha_c * (self.momento_inercia_concreto_y * self.material_concreto.modulo_elasticidade_secante)

        return (concreto + aco + armadura)
    
    @property
    @abstractmethod
    def esbeltez_compressao(self):
        pass

    @property
    @abstractmethod
    def esbeltez_flexao(self):
        pass
    


    # -------------------------------
    # CAPACIDADES RESISTENTES 
    # -------------------------------

    # --- Capacidades axiais ---

    # Armadura
    @abstractmethod
    def capacidade_axial_plastico_armadura(self):
        pass

    @abstractmethod
    def capacidade_axial_plastico_armadura_design(self):
        pass


    # Aco
    def capacidade_axial_plastico_aco(self):
        """
        Calcula a capacidade axial plastica nominal do aço na seção transversal
        """
        return self.area_aco * self.material_aco_estrutural.fy
    
    def capacidade_axial_plastico_aco_design(self):
        """
        Calcula a capacidade axial plastica de design do aço na seção transversal
        """
        return self.area_aco * self.material_aco_estrutural.resistencia_design


    # concreto
    def capacidade_axial_plastico_concreto(self):
        """
        Calcula a capacidade axial plastica nominal do concreto na seção transversal
        """
        return self.area_concreto * self.material_concreto.fck
    
    def capacidade_axial_plastico_concreto_design(self):
        """
        Calcula a capacidade axial plastica de design do concreto na seção transversal
        """
        return self.area_concreto * self.fcd1
    

    # seção transversal
    def capacidade_axial_plastico(self):
        """
        Calcula a capacidade axial plastica nominal da seção transversal
        """
        return (self.capacidade_axial_plastico_aco() + self.capacidade_axial_plastico_armadura() + self.capacidade_axial_plastico_concreto())
    
    def capacidade_axial_plastico_design(self):
        """
        Calcula a capacidade axial plastica de design da seção transversal
        """
        return (self.capacidade_axial_plastico_aco_design() + self.capacidade_axial_plastico_armadura_design() + self.capacidade_axial_plastico_concreto_design())
    
    @property
    @abstractmethod
    def capacidade_axial_resistente_secao_nominal(self):
        pass

    @property
    @abstractmethod
    def capacidade_axial_resistente_secao_design(self):
        pass

    # --- Capacidade resistente do pilar ---

    @property
    def _carga_flambagem_elastica_x(self):
        """
        Calcula a carga de flexão elastica para o eixo X
        Ne = min(pi^2 * (EI)e,x / (L^2))
        """
        return ((pi ** 2) * self.rigidez_flexao_equivalente_x / (self.comprimento_pilar_destravado ** 2))
    
    @property
    def _carga_flambagem_elastica_y(self):
        """
        Calcula a carga de flexão elastica para o eixo Y
        Ne = min(pi^2 * (EI)e,y / (L^2))
        """
        return ((pi ** 2) * self.rigidez_flexao_equivalente_y / (self.comprimento_pilar_destravado ** 2))

    @property
    def carga_flambagem_elastica(self):
        """
        Calcula a carga de flexão elastica para ambos os eixos, saindo com a menor
        Ne = min(pi^2 * (EI)e,i / (L^2))
        """
        ne_x = self._carga_flambagem_elastica_x
        ne_y = self._carga_flambagem_elastica_y

        return min(ne_x, ne_y)

    @property
    def indice_esbeltez_reduzido(self):
        """
        Calcula a esbeltez reduzida do pilar (M.3.2)
        (Np,R / Ne )^0.5
        """
        return ((self.capacidade_axial_resistente_secao_nominal / self.carga_flambagem_elastica) ** 0.5)
    
    @property
    def indice_esbeltez_reduzido_limite(self):
        """
        Limite para consideração dos efeitos de retração e fluencia do concreto (M.3.3)
        """

        return (
            (90 / pi) * ((self.capacidade_axial_resistente_secao_nominal / self.rigidez_axial_equivalente) ** 0.5)
        )

    @property
    def _incluir_momento_adicional(self):
        """
        Confere se é necessario incluir momento adicional devido a efeitos de fluencia e retração (Item M.3.3)
        """

        if self.indice_esbeltez_reduzido <= self.indice_esbeltez_reduzido_limite:
            return False
        else:
            return True
        
    @property
    def fator_reducao(self):

        """
        Calcula o fator de redução, conforme 5.3.3 na NBR 8800:2024
        """
        if self.indice_esbeltez_reduzido <= 1.5:
            result = 0.68 ** (self.indice_esbeltez_reduzido ** 2)
        else:
            result = (0.877 / (self.indice_esbeltez_reduzido ** 2))

        return result
    
    @property
    def capacidade_axial_resistente_pilar_nominal(self):
        """ 
        Calcula a capacidade axial resistente do pilar considerando capacidade nominal da seção (M.3.1)
        NR = X * Np,R
        """
        return (self.fator_reducao * self.capacidade_axial_resistente_secao_nominal)
    
    @property
    def capacidade_axial_resistente_pilar_design(self):
        """ 
        Calcula a capacidade axial resistente do pilar considerando capacidade de design da seção (M.3.1)
        NRd = X * Np,Rd
        """
        return (self.fator_reducao * self.capacidade_axial_resistente_secao_design)

    # --- Capacidades de Flexão ---
    # nominal

    @property
    def momento_resistente_plastico_aco_xx(self):
        """
        Calcula a capacidade resistente a flexão nominal no eixo X (M.5.5) do perfil de aço
        Mpl,a,R = fy* (Za - Zan)
        """
        return self.material_aco_estrutural.fy * (self.modulo_resistente_plastico_aco_x - self.modulo_resistente_plastico_aco_x_lnp)

    @property
    def momento_resistente_plastico_aco_yy(self):
        """
        Calcula a capacidade resistente a flexão nominal no eixo Y (M.5.5) do perfil de aço
        Mpl,a,R = fy* (Za - Zan)
        """
        return self.material_aco_estrutural.fy * (self.modulo_resistente_plastico_aco_y - self.modulo_resistente_plastico_aco_y_lnp)

    @property
    def momento_resistente_plastico_concreto_xx(self):
        """
        Calcula a capacidade resistente a flexão nominal no eixo X (M.5.5) da seção de concreto
        Mpl,c,R = 0.5 * fck* (Zc - Zcn)
        """
        return 0.5 * self.material_concreto.fck * (self.modulo_resistente_plastico_concreto_x - self.modulo_resistente_plastico_concreto_x_lnp)

    @property
    def momento_resistente_plastico_concreto_yy(self):
        """
        Calcula a capacidade resistente a flexão nominal no eixo Y (M.5.5) da seção de concreto
        Mpl,c,R = 0.5 * fck* (Zc - Zcn)
        """
        return 0.5 * self.material_concreto.fck * (self.modulo_resistente_plastico_concreto_y - self.modulo_resistente_plastico_concreto_y_lnp)

    @property
    def momento_resistente_plastico_armadura_xx(self):
        """
        Calcula a capacidade resistente a flexão nominal no eixo X (M.5.5) das armaduras da seção
        Mpl,s,R = fys* (Zs - Zsn)
        """
        if not self.material_armadura:
            return 0

        return self.material_armadura.fy * (self.modulo_resistente_plastico_armadura_x - self.modulo_resistente_plastico_armadura_x_lnp)

    @property
    def momento_resistente_plastico_armadura_yy(self):
        """
        Calcula a capacidade resistente a flexão nominal no eixo Y (M.5.5) das armaduras da seção
        Mpl,s,R = fys* (Zs - Zsn)
        """
        if not self.material_armadura:
            return 0

        return self.material_armadura.fy * (self.modulo_resistente_plastico_armadura_y - self.modulo_resistente_plastico_armadura_y_lnp)

    @property
    def momento_resistente_plastico_total_xx(self):
        """
        Calcula a capacidade resistente a flexão nominal no eixo X (M.5.5)
        Mpl,R = Mpl,a,R + Mpl,c,R + Mpl,s,R
        """
        return (self.momento_resistente_plastico_aco_xx + self.momento_resistente_plastico_concreto_xx + self.momento_resistente_plastico_armadura_xx)

    @property
    def momento_resistente_plastico_total_yy(self):
        """
        Calcula a capacidade resistente a flexão nominal no eixo Y (M.5.5)
        Mpl,R = Mpl,a,R + Mpl,c,R + Mpl,s,R
        """
        return (self.momento_resistente_plastico_aco_yy + self.momento_resistente_plastico_concreto_yy + self.momento_resistente_plastico_armadura_yy)
    

    # de calculo

    @property
    def momento_resistente_plastico_aco_design_xx(self):
        """
        Calcula a capacidade resistente a flexão de design no eixo X (M.5.5) do perfil de aço
        Mpl,a,R = fyd* (Za - Zan)
        """
        return self.material_aco_estrutural.resistencia_design * (self.modulo_resistente_plastico_aco_x - self.modulo_resistente_plastico_aco_x_lnp)

    @property
    def momento_resistente_plastico_aco_design_yy(self):
        """
        Calcula a capacidade resistente a flexão de design no eixo Y (M.5.5) do perfil de aço
        Mpl,a,R = fyd* (Za - Zan)
        """
        return self.material_aco_estrutural.resistencia_design * (self.modulo_resistente_plastico_aco_y - self.modulo_resistente_plastico_aco_y_lnp)

    @property
    def momento_resistente_plastico_concreto_design_xx(self):
        """
        Calcula a capacidade resistente a flexão de design no eixo X (M.5.5) da seção de concreto
        Mpl,c,Rd = 0.5 * fcd1* (Zc - Zcn)
        """ 
        return 0.5 * self.fcd1 * (self.modulo_resistente_plastico_concreto_x - self.modulo_resistente_plastico_concreto_x_lnp)

    @property
    def momento_resistente_plastico_concreto_design_yy(self):
        """
        Calcula a capacidade resistente a flexão de design no eixo Y (M.5.5) da seção de concreto
        Mpl,c,Rd = 0.5 * fcd1* (Zc - Zcn)
        """         
        return 0.5 * self.fcd1 * (self.modulo_resistente_plastico_concreto_y - self.modulo_resistente_plastico_concreto_y_lnp)

    @property
    def momento_resistente_plastico_armadura_design_xx(self):
        """
        Calcula a capacidade resistente a flexão de design no eixo X (M.5.5) das armaduras da seção
        Mpl,s,Rd = fsd* (Zs - Zsn)
        """
        if not self.material_armadura:
            return 0

        return self.material_armadura.resistencia_design * (self.modulo_resistente_plastico_armadura_x - self.modulo_resistente_plastico_armadura_x_lnp)

    @property
    def momento_resistente_plastico_armadura_design_yy(self):
        """
        Calcula a capacidade resistente a flexão de design no eixo Y (M.5.5) das armaduras da seção
        Mpl,s,Rd = fsd* (Zs - Zsn)
        """
        if not self.material_armadura:
            return 0

        return self.material_armadura.resistencia_design * (self.modulo_resistente_plastico_armadura_y - self.modulo_resistente_plastico_armadura_y_lnp)

    @property
    def momento_resistente_plastico_total_design_xx(self):
        """
        Calcula a capacidade resistente a flexão de design no eixo X (M.5.5)
        Mpl,Rd = Mpl,a,Rd + Mpl,c,Rd + Mpl,s,Rd
        """
        return (self.momento_resistente_plastico_aco_design_xx + self.momento_resistente_plastico_concreto_design_xx + self.momento_resistente_plastico_armadura_design_xx)

    @property
    def momento_resistente_plastico_total_design_yy(self):
        """
        Calcula a capacidade resistente a flexão de design no eixo Y (M.5.5)
        Mpl,Rd = Mpl,a,Rd + Mpl,c,Rd + Mpl,s,Rd
        """
        return (self.momento_resistente_plastico_aco_design_yy + self.momento_resistente_plastico_concreto_design_yy + self.momento_resistente_plastico_armadura_design_yy)
    

    # --- Capacidades de flexão máxima ---
    # nominal

    @property
    def momento_resistente_maximo_plastico_aco_xx(self):
        """
        Calcula a capacidade resistente máxima a flexão nominal no eixo X (M.5.5) do perfil de aço
        Mmax,a,R = fy* (Za)
        """
        return self.material_aco_estrutural.fy * (self.modulo_resistente_plastico_aco_x )

    @property
    def momento_resistente_maximo_plastico_aco_yy(self):
        """
        Calcula a capacidade resistente máxima a flexão nominal no eixo Y (M.5.5) do perfil de aço
        Mmax,a,R = fy* (Za)
        """
        return self.material_aco_estrutural.fy * (self.modulo_resistente_plastico_aco_y )

    @property
    def momento_resistente_maximo_plastico_concreto_xx(self):
        """
        Calcula a capacidade resistente máxima a flexão nominal no eixo X (M.5.5) do concreto na seção
        Mmax,c,R = 0.5 * fck * (Zc)
        """
        return 0.5 * self.material_concreto.fck * (self.modulo_resistente_plastico_concreto_x)

    @property
    def momento_resistente_maximo_plastico_concreto_yy(self):
        """
        Calcula a capacidade resistente máxima a flexão nominal no eixo Y (M.5.5) do concreto na seção
        Mmax,c,R = 0.5 * fck * (Zc)
        """
        return 0.5 * self.material_concreto.fck * (self.modulo_resistente_plastico_concreto_y)

    @property
    def momento_resistente_maximo_plastico_armadura_xx(self):
        """
        Calcula a capacidade resistente máxima a flexão nominal no eixo X (M.5.5) da armadura na seção
        Mmax,s,R = fys * (Zs)
        """
        if not self.material_armadura:
            return 0

        return self.material_armadura.fy * (self.modulo_resistente_plastico_armadura_x )

    @property
    def momento_resistente_maximo_plastico_armadura_yy(self):
        """
        Calcula a capacidade resistente máxima a flexão nominal no eixo Y (M.5.5) da armadura na seção
        Mmax,s,R = fys * (Zs)
        """
        if not self.material_armadura:
            return 0

        return self.material_armadura.fy * (self.modulo_resistente_plastico_armadura_y )

    @property
    def momento_resistente_maximo_plastico_total_xx(self):
        """
        Calcula a capacidade resistente máxima a flexão nominal no eixo X (M.5.5)
        Mmax,R = Mmax,a,R + Mmax,c,R + Mmax,s,R
        """
        return (self.momento_resistente_maximo_plastico_aco_xx + self.momento_resistente_maximo_plastico_concreto_xx + self.momento_resistente_maximo_plastico_armadura_xx)

    @property
    def momento_resistente_maximo_plastico_total_yy(self):
        """
        Calcula a capacidade resistente máxima a flexão nominal no eixo Y (M.5.5)
        Mmax,R = Mmax,a,R + Mmax,c,R + Mmax,s,R
        """
        return (self.momento_resistente_maximo_plastico_aco_yy + self.momento_resistente_maximo_plastico_concreto_yy + self.momento_resistente_maximo_plastico_armadura_yy)
    

    # de calculo

    @property
    def momento_resistente_maximo_plastico_aco_design_xx(self):
        """
        Calcula a capacidade resistente máxima a flexão de design no eixo X (M.5.5) do perfil de aço
        Mmax,a,Rd = fyd * (Za)
        """
        return self.material_aco_estrutural.resistencia_design * (self.modulo_resistente_plastico_aco_x)

    @property
    def momento_resistente_maximo_plastico_aco_design_yy(self):
        """
        Calcula a capacidade resistente máxima a flexão de design no eixo Y (M.5.5) do perfil de aço
        Mmax,a,Rd = fyd * (Za)
        """
        return self.material_aco_estrutural.resistencia_design * (self.modulo_resistente_plastico_aco_y)

    @property
    def momento_resistente_maximo_plastico_concreto_design_xx(self): 
        """
        Calcula a capacidade resistente máxima a flexão de design no eixo X (M.5.5) do concreto na seção
        Mmax,c,Rd = 0.5 * fcd1 * (Zc)
        """
        return 0.5 * self.fcd1 * (self.modulo_resistente_plastico_concreto_x)

    @property
    def momento_resistente_maximo_plastico_concreto_design_yy(self):
        """
        Calcula a capacidade resistente máxima a flexão de design no eixo Y (M.5.5) do concreto na seção
        Mmax,c,Rd = 0.5 * fcd1 * (Zc)
        """  
        return 0.5 * self.fcd1 * (self.modulo_resistente_plastico_concreto_y)

    @property
    def momento_resistente_maximo_plastico_armadura_design_xx(self):
        """
        Calcula a capacidade resistente máxima a flexão de design no eixo X (M.5.5) da armadura na seção
        Mmax,s,Rd = fsd * (Zs)
        """
        if not self.material_armadura:
            return 0

        return self.material_armadura.resistencia_design * (self.modulo_resistente_plastico_armadura_x)

    @property
    def momento_resistente_maximo_plastico_armadura_design_yy(self):
        """
        Calcula a capacidade resistente máxima a flexão de design no eixo Y (M.5.5) da armadura na seção
        Mmax,s,Rd = fsd * (Zs)
        """
        if not self.material_armadura:
            return 0

        return self.material_armadura.resistencia_design * (self.modulo_resistente_plastico_armadura_y)

    @property
    def momento_resistente_maximo_plastico_total_design_xx(self):
        """
        Calcula a capacidade resistente máxima a flexão de design no eixo X (M.5.5)
        Mmax,Rd = Mmax,a,Rd + Mmax,c,Rd + Mmax,s,Rd
        """
        return (self.momento_resistente_maximo_plastico_aco_design_xx + self.momento_resistente_maximo_plastico_concreto_design_xx + self.momento_resistente_maximo_plastico_armadura_design_xx)

    @property
    def momento_resistente_maximo_plastico_total_design_yy(self):
        """
        Calcula a capacidade resistente máxima a flexão de design no eixo Y (M.5.5)
        Mmax,Rd = Mmax,a,Rd + Mmax,c,Rd + Mmax,s,Rd
        """
        return (self.momento_resistente_maximo_plastico_aco_design_yy + self.momento_resistente_maximo_plastico_concreto_design_yy + self.momento_resistente_maximo_plastico_armadura_design_yy)


    @property
    @abstractmethod
    def capacidade_flexao_resistente_secao_nominal_xx(self):
        pass

    @property
    @abstractmethod
    def capacidade_flexao_resistente_secao_nominal_yy(self):
        pass

    @property
    @abstractmethod
    def capacidade_flexao_resistente_secao_design_xx(self):
        pass

    @property
    @abstractmethod
    def capacidade_flexao_resistente_secao_design_yy(self):
        pass
    
            


    
