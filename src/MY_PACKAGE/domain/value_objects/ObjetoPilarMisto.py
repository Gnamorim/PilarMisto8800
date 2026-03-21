from abc import ABC, abstractmethod

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
            cobrimento:float
        ):

        self.material_aco_estrutural = material_aco_estrutural
        self.material_concreto = material_concreto
        self.material_armadura = material_armadura
        self.diametro_armadura_longitudinal = diametro_armadura_longitudinal
        self.numero_armadura_longitudinal = numero_armadura_longitudinal
        self.diametro_armadura_transversal = diametro_armadura_transversal
        self.espacamento_armadura_transversal = espacamento_armadura_transversal
        self.cobrimento = cobrimento

        

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

        if not isinstance(self.diametro_armadura_transversal, (int, float)) or isinstance(self.diametro_armadura_longitudinal, bool):
            raise TypeError("diametro_armadura_transversal deve ser numérico")

        if not isinstance(self.numero_armadura_longitudinal, (int, float)):
            raise TypeError("numero_armadura_longitudinal deve ser numerico")

        if not isinstance(self.espacamento_armadura_transversal, int):
            raise TypeError("espacamento_armadura_transversal deve ser inteiro")

        if not isinstance(self.cobrimento, (int, float)) or isinstance(self.cobrimento, bool):
            raise TypeError("cobrimento deve ser numérico")
        
        # Valores físicos

        if self.diametro_armadura_longitudinal < 0:
            raise ValueError("diametro_armadura_longitudinal deve ser positivo")

        if self.numero_armadura_longitudinal < 0:
            raise ValueError("numero_armadura_longitudinal deve ser > 0")

        if self.diametro_armadura_transversal < 0:
            raise ValueError("diametro_armadura_transversal deve ser positivo")

        if self.espacamento_armadura_transversal < 0:
            raise ValueError("espacamento_armadura_transversal deve ser > 0")
        
        if self.diametro_armadura_longitudinal > 50:
            raise ValueError("diametro_armadura_longitudinal deve > 50 mm")

        if self.numero_armadura_longitudinal > 30:
            raise ValueError("numero_armadura_longitudinal deve ser < 30")  # upper number aleatorio - definir algo que faca mais sentido

        if self.diametro_armadura_transversal > 50:
            raise ValueError("diametro_armadura_transversal deve ser > 50 mm")

        if self.espacamento_armadura_transversal > 1000:
            raise ValueError("espacamento_armadura_transversal deve ser < 1000 mm") # upper number aleatorio - definir algo que faca mais sentido

        if self.cobrimento < 0:
            raise ValueError("cobrimento deve ser positivo")
        


    @abstractmethod
    def _limite_escopo(self):
        pass

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

    # # momento de inercia

    # @abstractmethod
    # def momento_inercia_aco_x(self):
    #     pass

    # @abstractmethod
    # def momento_inercia_concreto_x(self):
    #     pass
    
    # @abstractmethod
    # def momento_inercia_armadura_x(self):
    #     pass

    # @abstractmethod
    # def momento_inercia_aco_y(self):
    #     pass

    # @abstractmethod
    # def momento_inercia_concreto_y(self):
    #     pass
    
    # @abstractmethod
    # def momento_inercia_armadura_y(self):
    #     pass    

    # @abstractmethod
    # def esbeltez_perfil(self):
    #     pass

    # # modulo resistente plastico

    # @abstractmethod
    # def modulo_resistente_plastico_aco_x(self):
    #     pass

    # @abstractmethod
    # def modulo_resistente_plastico_concreto_x(self):
    #     pass

    # @abstractmethod
    # def modulo_resistente_plastico_armadura_x(self):
    #     pass

    # @abstractmethod
    # def modulo_resistente_plastico_aco_y(self):
    #     pass

    # @abstractmethod
    # def modulo_resistente_plastico_concreto_y(self):
    #     pass

    # @abstractmethod
    # def modulo_resistente_plastico_armadura_y(self):
    #     pass


    # # CARACTERISTICAS DE MATERIAL

    # @abstractmethod
    # def resistencia_nominal_aco(self):
    #     pass

    # @abstractmethod
    # def resistencia_nominal_concreto(self):
    #     pass

    # @abstractmethod
    # def resistencia_nominal_armadura(self):
    #     pass

    # # CAPACIDADES RESISTENTES 

    # #axial

    # @abstractmethod
    # def capacidade_resistente_nominal_axial_aco(self):
    #     pass

    # @abstractmethod
    # def capacidade_resistente_nominal_axial_concreto(self):
    #     pass

    # @abstractmethod
    # def capacidade_resistente_nominal_axial_armadura(self):
    #     pass

    # @abstractmethod
    # def capacidade_resistente_nominal_axial(self):
    #     pass

    # @abstractmethod
    # def capacidade_resistente_design_axial_aco(self):
    #     pass

    # @abstractmethod
    # def capacidade_resistente_design_axial_concreto(self):
    #     pass

    # @abstractmethod
    # def capacidade_resistente_design_axial_armadura(self):
    #     pass

    # @abstractmethod
    # def capacidade_resistente_design_axial(self):
    #     pass

    # # momento fletor

    