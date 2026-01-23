from abc import ABC, abstractmethod

class ObjetoPilarMisto(ABC):


    # FUNÇÕES DE VALIDAÇÃO

    @abstractmethod
    def _validate(self):
        pass

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

    