from abc import ABC, abstractmethod
from math import pi

from MY_PACKAGE.domain.value_objects.ObjetoConcreto import  ConcretoNormal
from MY_PACKAGE.domain.value_objects.ObjetoAco import AcoEstrutural, AcoArmadura

class ObjetoPilarMisto(ABC):

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
        
      
        # Valores físicos - limites construtivos -REFINAR

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
        
        # --- area perfil >1% da area total ---
        area_aco = self.area_aco()
        area_concreto = self.area_concreto()
        area_armadura = self.area_armadura() 

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
     
    @abstractmethod
    def area_aco(self):
        pass

    @abstractmethod
    def area_concreto(self):
        pass

    @abstractmethod
    def area_armadura(self):
        pass

    def area_total(self):
        return self.area_concreto() + self.area_aco() + self.area_armadura() 

    # momento de inercia

    @abstractmethod
    def momento_inercia_aco_x(self):
        pass

    @abstractmethod
    def momento_inercia_concreto_x(self):
        pass
    
    @abstractmethod
    def momento_inercia_armadura_x(self):
        pass

    @abstractmethod
    def momento_inercia_aco_y(self):
        pass

    @abstractmethod
    def momento_inercia_concreto_y(self):
        pass
    
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
        return (self.area_aco * self.material_aco_estrutural.modulo_elasticidade)

    @property
    def rigidez_axial_concreto(self):
        return (self.area_concreto * self.material_concreto.modulo_elasticidade_secante)
    
    @property
    def rigidez_axial_armadura(self):
        return (self.area_armadura * self.material_armadura.modulo_elasticidade)
    
    @property
    def rigidez_axial_equivalente(self):
        return (self.rigidez_axial_aco + self.rigidez_axial_armadura + self.rigidez_axial_concreto)
    
    # flexão

    @property
    @abstractmethod
    def alpha_c(self):
        pass

    @property
    def rigidez_flexao_equivalente_x(self):
        aco = (self.momento_inercia_aco_x * self.material_aco_estrutural.modulo_elasticidade)
        armadura = (self.momento_inercia_armadura_x * self.material_armadura.modulo_elasticidade)
        concreto = self.alpha_c * (self.momento_inercia_concreto_x * self.material_concreto.modulo_elasticidade_secante)

        return (concreto + aco + armadura)
    
    @property
    def rigidez_flexao_equivalente_y(self):
        aco = (self.momento_inercia_aco_y * self.material_aco_estrutural.modulo_elasticidade)
        armadura = (self.momento_inercia_armadura_y * self.material_armadura.modulo_elasticidade)
        concreto = self.alpha_c * (self.momento_inercia_concreto_y * self.material_concreto.modulo_elasticidade_secante)

        return (concreto + aco + armadura)
    


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
        return self.area_aco() * self.material_aco_estrutural.fy
    
    def capacidade_axial_plastico_aco_design(self):
        return self.area_aco() * self.material_aco_estrutural.resistencia_design


    # concreto
    def capacidade_axial_plastico_concreto(self):
        return self.area_concreto() * self.material_concreto.fck
    
    def capacidade_axial_plastico_concreto_design(self):
        return self.area_concreto() * self.fcd1
    

    # seção transversal
    def capacidade_axial_plastico(self):
        return (self.capacidade_axial_plastico_aco() + self.capacidade_axial_plastico_armadura() + self.capacidade_axial_plastico_concreto())
    
    def capacidade_axial_plastico_design(self):
        return (self.capacidade_axial_plastico_aco_design() + self.capacidade_axial_plastico_armadura_design() + self.capacidade_axial_plastico_concreto_design())
    
    @property
    @abstractmethod
    def capacidade_axial_resistente_secao_nominal(self):
        pass

    @property
    @abstractmethod
    def capacidade_axial_resistente_secao_design(self):
        pass

    @property
    def carga_flambagem_elastica(self):
        ne_x = ((pi ** 2) * self.rigidez_flexao_equivalente_x / (self.comprimento_pilar_destravado ** 2))
        ne_y = ((pi ** 2) * self.rigidez_flexao_equivalente_y / (self.comprimento_pilar_destravado ** 2))

        return min(ne_x, ne_y)

    @property
    def indice_esbeltez_reduzido(self):
        
        return ((self.capacidade_axial_resistente_secao_nominal / self.carga_flambagem_elastica) ** 0.5)
    
    @property
    def indice_esbeltez_reduzido_limite(self):
        return (
            (90 / pi) * ((self.capacidade_axial_resistente_secao_nominal / self.rigidez_axial_equivalente) ** 0.5)
        )

    @property
    def incluir_momento_adicional(self):
        """
        Confere se é necessario incluir momento adicional devido a efeitos de fluencia e retração (Item M.3.3)
        """

        if self.indice_esbeltez_reduzido <= self.indice_esbeltez_reduzido_limite:
            return False
        else:
            return True

    # --- Capacidades de Flexão ---
    # nominal

    @property
    def momento_resistente_plastico_aco_xx(self):
        return self.material_aco_estrutural.fy * (self.modulo_resistente_plastico_aco_x - self.modulo_resistente_plastico_aco_x_lnp)

    @property
    def momento_resistente_plastico_aco_yy(self):
        return self.material_aco_estrutural.fy * (self.modulo_resistente_plastico_aco_y - self.modulo_resistente_plastico_aco_y_lnp)

    @property
    def momento_resistente_plastico_concreto_xx(self):
        return 0.5 * self.material_concreto.fck * (self.modulo_resistente_plastico_concreto_x - self.modulo_resistente_plastico_concreto_x_lnp)

    @property
    def momento_resistente_plastico_concreto_yy(self):
        return 0.5 * self.material_concreto.fck * (self.modulo_resistente_plastico_concreto_y - self.modulo_resistente_plastico_concreto_y_lnp)

    @property
    def momento_resistente_plastico_armadura_xx(self):
        if not self.material_armadura:
            return 0

        return self.material_armadura.fy * (self.modulo_resistente_plastico_armadura_x - self.modulo_resistente_plastico_armadura_x_lnp)

    @property
    def momento_resistente_plastico_armadura_yy(self):
        if not self.material_armadura:
            return 0

        return self.material_armadura.fy * (self.modulo_resistente_plastico_armadura_y - self.modulo_resistente_plastico_armadura_y_lnp)

    @property
    def momento_resistente_plastico_total_xx(self):
        return (self.momento_resistente_plastico_aco_xx + self.momento_resistente_plastico_concreto_xx + self.momento_resistente_plastico_armadura_xx)

    @property
    def momento_resistente_plastico_total_yy(self):
        return (self.momento_resistente_plastico_aco_yy + self.momento_resistente_plastico_concreto_yy + self.momento_resistente_plastico_armadura_yy)
    

    # de calculo

    @property
    def momento_resistente_plastico_aco_design_xx(self):
        return self.material_aco_estrutural.resistencia_design * (self.modulo_resistente_plastico_aco_x - self.modulo_resistente_plastico_aco_x_lnp)

    @property
    def momento_resistente_plastico_aco_design_yy(self):
        return self.material_aco_estrutural.resistencia_design * (self.modulo_resistente_plastico_aco_y - self.modulo_resistente_plastico_aco_y_lnp)

    @property
    def momento_resistente_plastico_concreto_design_xx(self):
        return 0.5 * self.fcd1 * (self.modulo_resistente_plastico_concreto_x - self.modulo_resistente_plastico_concreto_x_lnp)

    @property
    def momento_resistente_plastico_concreto_design_yy(self):
        return 0.5 * self.fcd1 * (self.modulo_resistente_plastico_concreto_y - self.modulo_resistente_plastico_concreto_y_lnp)

    @property
    def momento_resistente_plastico_armadura_design_xx(self):
        if not self.material_armadura:
            return 0

        return self.material_armadura.resistencia_design * (self.modulo_resistente_plastico_armadura_x - self.modulo_resistente_plastico_armadura_x_lnp)

    @property
    def momento_resistente_plastico_armadura_design_yy(self):
        if not self.material_armadura:
            return 0

        return self.material_armadura.resistencia_design * (self.modulo_resistente_plastico_armadura_y - self.modulo_resistente_plastico_armadura_y_lnp)

    @property
    def momento_resistente_plastico_total_design_xx(self):
        return (self.momento_resistente_plastico_aco_design_xx + self.momento_resistente_plastico_concreto_design_xx + self.momento_resistente_plastico_armadura_design_xx)

    @property
    def momento_resistente_plastico_total_design_yy(self):
        return (self.momento_resistente_plastico_aco_design_yy + self.momento_resistente_plastico_concreto_design_yy + self.momento_resistente_plastico_armadura_design_yy)
    

    # --- Capacidades de flexão máxima ---
    # nominal

    @property
    def momento_resistente_maximo_plastico_aco_xx(self):
        return self.material_aco_estrutural.fy * (self.modulo_resistente_plastico_aco_x )

    @property
    def momento_resistente_maximo_plastico_aco_yy(self):
        return self.material_aco_estrutural.fy * (self.modulo_resistente_plastico_aco_y )

    @property
    def momento_resistente_maximo_plastico_concreto_xx(self):
        return 0.5 * self.material_concreto.fck * (self.modulo_resistente_plastico_concreto_x)

    @property
    def momento_resistente_maximo_plastico_concreto_yy(self):
        return 0.5 * self.material_concreto.fck * (self.modulo_resistente_plastico_concreto_y)

    @property
    def momento_resistente_maximo_plastico_armadura_xx(self):
        if not self.material_armadura:
            return 0

        return self.material_armadura.fy * (self.modulo_resistente_plastico_armadura_x )

    @property
    def momento_resistente_maximo_plastico_armadura_yy(self):
        if not self.material_armadura:
            return 0

        return self.material_armadura.fy * (self.modulo_resistente_plastico_armadura_y )

    @property
    def momento_resistente_maximo_plastico_total_xx(self):
        return (self.momento_resistente_maximo_plastico_aco_xx + self.momento_resistente_maximo_plastico_concreto_xx + self.momento_resistente_maximo_plastico_armadura_xx)

    @property
    def momento_resistente_maximo_plastico_total_yy(self):
        return (self.momento_resistente_maximo_plastico_aco_yy + self.momento_resistente_maximo_plastico_concreto_yy + self.momento_resistente_maximo_plastico_armadura_yy)
    

    # de calculo

    @property
    def momento_resistente_maximo_plastico_aco_design_xx(self):
        return self.material_aco_estrutural.resistencia_design * (self.modulo_resistente_plastico_aco_x)

    @property
    def momento_resistente_maximo_plastico_aco_design_yy(self):
        return self.material_aco_estrutural.resistencia_design * (self.modulo_resistente_plastico_aco_y)

    @property
    def momento_resistente_maximo_plastico_concreto_design_xx(self):
        return 0.5 * self.fcd1 * (self.modulo_resistente_plastico_concreto_x)

    @property
    def momento_resistente_maximo_plastico_concreto_design_yy(self):
        return 0.5 * self.fcd1 * (self.modulo_resistente_plastico_concreto_y)

    @property
    def momento_resistente_maximo_plastico_armadura_design_xx(self):
        if not self.material_armadura:
            return 0

        return self.material_armadura.resistencia_design * (self.modulo_resistente_plastico_armadura_x)

    @property
    def momento_resistente_maximo_plastico_armadura_design_yy(self):
        if not self.material_armadura:
            return 0

        return self.material_armadura.resistencia_design * (self.modulo_resistente_plastico_armadura_y)

    @property
    def momento_resistente_maximo_plastico_total_design_xx(self):
        return (self.momento_resistente_maximo_plastico_aco_design_xx + self.momento_resistente_maximo_plastico_concreto_design_xx + self.momento_resistente_maximo_plastico_armadura_design_xx)

    @property
    def momento_resistente_maximo_plastico_total_design_yy(self):
        return (self.momento_resistente_maximo_plastico_aco_design_yy + self.momento_resistente_maximo_plastico_concreto_design_yy + self.momento_resistente_maximo_plastico_armadura_design_yy)





    