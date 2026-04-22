import numpy as np
import warnings

class CircularCFST:
    
    tube_diameter: float
    thickness: float
    fyk : float
    steel_modulus : float
    gamma_a: float
    fsk: float
    bar_diameter: float
    bar_number: int
    reinforcement_modulus: int
    gamma_s: float
    concrete_cover: float
    fck: float
    concrete_modulus: float
    gamma_c: float
    stirrup_diameter: float
    internal_diameter:float
    theta: float
    hn_z_axis: float
    z_axis_asn: float
    hn_y_axis: float
    y_axis_asn: float



    def __init__(self, tube_diameter: float, thickness: float, fyk: float, fck: float, concrete_cover:float = 25, concrete_modulus: float = 30000., steel_modulus: float = 200000., reinforcement_modulus: float = 210000, fsk:float = 0.0, bar_diameter: float = 0.0, bar_number: int = 0, stirrup_diameter:float = 0.0, gamma_a: float = 1.1, gamma_s: float = 1.15, gamma_c: float = 1.4):
        self.tube_diameter = tube_diameter
        self.thickness = thickness
        self.fyk = fyk
        self.steel_modulus = steel_modulus
        self.fsk = fsk
        self.bar_diameter = bar_diameter
        self.bar_number = bar_number
        self.reinforcement_modulus = reinforcement_modulus
        self.concrete_cover = concrete_cover
        self.fck = fck
        self.concrete_modulus = concrete_modulus
        self.gamma_a = gamma_a
        self.gamma_s = gamma_s
        self.gamma_c = gamma_c
        self.stirrup_diameter = stirrup_diameter
        self.validate()  # must be before any internal calculation
        self.internal_diameter = tube_diameter - 2 * thickness
        self.theta = self.theta_calc()

        hnz, Asnz = self.z_axis_properties()
        hny, Asny = self.y_axis_properties()
        self.hn_z_axis = hnz
        self.z_axis_asn = Asnz
        self.hn_y_axis = hny
        self.y_axis_asn = Asny



    def validate(self) -> None:
        if not hasattr(self, "tube_diameter"):
            raise AttributeError("Attribute 'tube_diameter' is missing.")
        if not isinstance(self.tube_diameter,(float, int)) or isinstance(self.tube_diameter, bool):
            raise TypeError('tube diameter must be a float or an integer')

        if not hasattr(self, "thickness"):
            raise AttributeError("Attribute 'thickness' is missing.")
        if not isinstance(self.thickness,(float, int))or isinstance(self.thickness, bool):
            raise TypeError('thickness must be a float or an integer')
        
        if not hasattr(self, "fyk"):
            raise AttributeError("Attribute 'fyk' is missing.")
        if not isinstance(self.fyk,(float, int))or isinstance(self.fyk, bool):
            raise TypeError('fyk must be a float or an integer')

        if not hasattr(self, "fsk"):
            raise AttributeError("Attribute 'fsk' is missing.")
        if not isinstance(self.fsk,(float, int))or isinstance(self.fsk, bool):
            raise TypeError('fsk must be a float or an integer')

        if not hasattr(self, "fck"):
            raise AttributeError("Attribute 'fck' is missing.")
        if not isinstance(self.fck,(float, int))or isinstance(self.fck, bool):
            raise TypeError('fck must be a float or an integer')
        
        if not hasattr(self, "concrete_cover"):
            raise AttributeError("Attribute 'concrete_cover' is missing.")
        if not isinstance(self.concrete_cover,(float, int))or isinstance(self.concrete_cover, bool):
            raise TypeError('concrete cover must be a float or an integer')
        
        if not hasattr(self, "steel_modulus"):
            raise AttributeError("Attribute 'steel_modulus' is missing.")
        if not isinstance(self.steel_modulus,(float, int))or isinstance(self.steel_modulus, bool):
            raise TypeError('steel_modulus must be a float or an integer')
        
        if not hasattr(self, "reinforcement_modulus"):
            raise AttributeError("Attribute 'reinforcement_modulus' is missing.")
        if not isinstance(self.reinforcement_modulus,(float, int))or isinstance(self.reinforcement_modulus, bool):
            raise TypeError('reinforcement_modulus must be a float or an integer')

        if not hasattr(self, "concrete_modulus"):
            raise AttributeError("Attribute 'concrete_modulus' is missing.")
        if not isinstance(self.concrete_modulus,(float, int))or isinstance(self.concrete_modulus, bool):
            raise TypeError('concrete_modulus must be a float or an integer')
        
        if not hasattr(self, "bar_number"):
            raise AttributeError("Attribute 'bar_number' is missing.")
        if not isinstance(self.bar_number,int)or isinstance(self.bar_number, bool):
            raise TypeError('the number of bars must be an integer')

        if not hasattr(self, "bar_diameter"):
            raise AttributeError("Attribute 'bar_diameter' is missing.")
        if not isinstance(self.bar_diameter,(float, int))or isinstance(self.bar_diameter, bool):
            raise TypeError('bar diameter must be a float or an integer')
        
        if not hasattr(self, "stirrup_diameter"):
            raise AttributeError("Attribute 'stirrup_diameter' is missing.")
        if not isinstance(self.stirrup_diameter,(float, int))or isinstance(self.stirrup_diameter, bool):
            raise TypeError('stirrup diameter must be a float or an integer')
        
        if not hasattr(self, "gamma_a"):
            raise AttributeError("Attribute 'gamma_a' is missing.")
        if not isinstance(self.gamma_a,float)or isinstance(self.gamma_a, bool):
            raise TypeError('Gamma A must be a float')
        
        if not hasattr(self, "gamma_s"):
            raise AttributeError("Attribute 'gamma_s' is missing.")
        if not isinstance(self.gamma_s,float)or isinstance(self.gamma_s, bool):
            raise TypeError('Gamma S must be a float')
        
        if not hasattr(self, "gamma_c"):
            raise AttributeError("Attribute gamma_c' is missing.")
        if not isinstance(self.gamma_c,float)or isinstance(self.gamma_c, bool):
            raise TypeError('Gamma C must be a float')
        
        if any(value == 0 for value in [self.fsk, self.bar_diameter, self.bar_number]):
            self.bar_number = 0
            self.bar_diameter = 0
            self.fsk = 0
            warnings.warn('reinforcement diameter, the number of the bars or the reinforcement strength is defined as 0. the reinforcements will not be considered', UserWarning)
            print('reinforcement diameter, the number of the bars or the reinforcement strength is defined as 0. the reinforcements will not be considered')
            

        

    # geometric characteristics    

    def theta_calc(self):
        if self.bar_number == 0:
            return 0
        return ( 2 * np.pi ) / self.bar_number

    def steel_area(self):
        return ( ( np.pi * ( (self.tube_diameter ** 2) - (self.internal_diameter ** 2 ) ) ) / 4)
    
    def reinforcement_area(self):
        return ( ( np.pi * ( self.bar_diameter ** 2 ) * self.bar_number ) / 4)
    
    def concrete_area(self):
        return ( ( np.pi * ( self.internal_diameter ** 2 ) ) / 4) - self.reinforcement_area()
    
    def _reinforcement_radius(self):
        return (self.tube_diameter - (2 * self.thickness) - (2 * self.concrete_cover) - self.bar_diameter - (2 * self.stirrup_diameter)) / 2

    def steel_inertia_z(self):
        return ( ( np.pi / 64 ) * ( ( self.tube_diameter ** 4 ) - ( self.internal_diameter ** 4 ) ) )

    def steel_inertia_y(self):
        resp = self.steel_inertia_z() 
        return resp
    
    def reinforcement_inertia_z(self):
        
        # defined for circular reiforcements
        if self.bar_number <= 0:
            return 0.0

        iz = np.pi * ( self.bar_diameter ** 4 ) / 64
        iz_tot = 0.0

        for i in range(0, self.bar_number):

            a = np.pi * ( ( self.bar_diameter ** 2 ) / 4 ) * ( ( self._reinforcement_radius() * ( np.abs( np.sin( i * self.theta ) ) ) ) ** 2 )
            iz_tot = iz_tot + iz + a

        return iz_tot

    def reinforcement_inertia_y(self):
        
        # defined for circular reiforcements
        if self.bar_number <= 0:
            return 0.0

        iy = np.pi * ( self.bar_diameter ** 4 ) / 64
        iy_tot = 0.0

        for i in range(0, self.bar_number):

            a = np.pi * ( ( self.bar_diameter ** 2 ) / 4 ) * ( ( self._reinforcement_radius() * ( np.abs( np.cos( i * self.theta ) ) ) ) ** 2 )
            iy_tot = iy_tot + iy + a

        return iy_tot
    
    def concrete_inertia_z(self):
        return ( ( np.pi * ( self.internal_diameter ** 4 ) ) / 64 ) - self.reinforcement_inertia_z()
    
    def concrete_inertia_y(self):
        return ( ( np.pi * ( self.internal_diameter ** 4 ) ) / 64 ) - self.reinforcement_inertia_y()
    
    # material design strengths

    def fyd(self) -> float:
        return self.fyk / self.gamma_a

    def fsd(self):
        return  self.fsk / self.gamma_s 
    
    def fcd(self):
        return  self.fck / self.gamma_c
    
    def fcd1(self):
        return 0.95 * self.fcd()

    
    # axial strengths

    def steel_axial_strength(self):
        return self.steel_area() * self.fyd()
    
    def reinforcement_axial_strength(self):
        return self.reinforcement_area() * self.fcd1() * (self.reinforcement_modulus / self.concrete_modulus)
    
    def concrete_axial_strength(self):
        return self.concrete_area() * self.fcd1()
    
    def section_axial_strength(self):
        return self.steel_axial_strength() + self.reinforcement_axial_strength() + self.concrete_axial_strength()
    

    # plastic modulus

    def steel_plastic_modulus_z(self):
        return (1 / 6) * ((self.tube_diameter ** 3) - (self.internal_diameter ** 3))

    def steel_plastic_modulus_y(self):
        resp = self.steel_plastic_modulus_z()
        return resp
    
    def reinforcement_plastic_modulus_z(self):
        if self.bar_number == 0:
            return 0
        return sum( abs((np.pi / 4) * (self.bar_diameter ** 2) * np.sin(n *self.theta) * self._reinforcement_radius()) for n in range(0,self.bar_number))
    
    def reinforcement_plastic_modulus_y(self):
        if self.bar_number == 0:
            return 0        
        return sum( abs((np.pi / 4) * (self.bar_diameter ** 2) * np.cos(n * self.theta) * self._reinforcement_radius()) for n in range(0,self.bar_number))
    
    def concrete_plastic_modulus_z(self):
        return ((self.internal_diameter ** 3) / 4) - (2 / 3) * (((self.tube_diameter / 2) - self.thickness) ** 3) - self.reinforcement_plastic_modulus_z()

    def concrete_plastic_modulus_y(self):
        return ((self.internal_diameter ** 3) / 4) - (2 / 3) * (((self.tube_diameter / 2) - self.thickness) ** 3) - self.reinforcement_plastic_modulus_y()   
    
    def z_axis_properties(self):
        Asn = 0

        if self.bar_number == 0:
            hn =((self.concrete_area() * self.fcd1() - Asn * (2 * self.fsd() - self.fcd1())) / (2 * self.tube_diameter * self.fcd1() + 4 * self.thickness * (2 * self.fyd() - self.fcd1())))
            return hn, Asn

        for i in range(5):
            hn =((self.concrete_area() * self.fcd1() - Asn * (2 * self.fsd() - self.fcd1())) / (2 * self.tube_diameter * self.fcd1() + 4 * self.thickness * (2 * self.fyd() - self.fcd1())))
            Asn1 = sum((np.pi / 4) * (self.bar_diameter ** 2) for n in range(0,self.bar_number) if abs(np.sin(n * self.theta) * self._reinforcement_radius()) <= hn)

            if abs(Asn1 - Asn) < 0.1:
                return hn, Asn1

            Asn = Asn1
        return hn, Asn

    def y_axis_properties(self):
        Asn = 0

        if self.bar_number == 0:
            hn =((self.concrete_area() * self.fcd1() - Asn * (2 * self.fsd() - self.fcd1())) / (2 * self.tube_diameter * self.fcd1() + 4 * self.thickness * (2 * self.fyd() - self.fcd1())))
            return hn, Asn

        for i in range(5):
            hn =((self.concrete_area() * self.fcd1() - Asn * (2 * self.fsd() - self.fcd1())) / (2 * self.tube_diameter * self.fcd1() + 4 * self.thickness * (2 * self.fyd() - self.fcd1())))
            Asn1 = sum((np.pi / 4) * (self.bar_diameter ** 2) for n in range(0,self.bar_number) if abs(np.cos(n * self.theta) * self._reinforcement_radius()) <= hn)

            if abs(Asn1 - Asn) < 0.01:
                return hn, Asn1 

            Asn = Asn1
        return hn, Asn
    
    def reinforcement_hn_plastic_modulus_z(self):
        if self.bar_number == 0:
            return 0

        return sum((np.pi / 4) * (self.bar_diameter ** 2) * abs(np.sin(n * self.theta) * self._reinforcement_radius()) for n in range(0,self.bar_number) if abs(np.sin(n * self.theta) * self._reinforcement_radius()) <= self.hn_z_axis)
    
    def reinforcement_hn_plastic_modulus_y(self):
        if self.bar_number == 0:
            return 0

        return sum((np.pi / 4) * (self.bar_diameter ** 2) * abs(np.cos(n * self.theta) * self._reinforcement_radius()) for n in range(0,self.bar_number) if abs(np.cos(n * self.theta) * self._reinforcement_radius()) <= self.hn_y_axis)
    
    def concrete_hn_plastic_modulus_z(self):
        return self.internal_diameter * (self.hn_z_axis ** 2) - self.reinforcement_hn_plastic_modulus_z()
    
    def concrete_hn_plastic_modulus_y(self):
        return self.internal_diameter * (self.hn_y_axis ** 2) - self.reinforcement_hn_plastic_modulus_y()
    
    def steel_hn_plastic_modulus_z(self):
        return self.tube_diameter * (self.hn_z_axis ** 2) - self.concrete_hn_plastic_modulus_z() - self.reinforcement_hn_plastic_modulus_z()

    def steel_hn_plastic_modulus_y(self):
        return self.tube_diameter * (self.hn_y_axis ** 2) - self.concrete_hn_plastic_modulus_y() - self.reinforcement_hn_plastic_modulus_y()
    

    # plastic bending moment

    def plastic_bending_moment_z(self):
        return self.fyd() * (self.steel_plastic_modulus_z() - self.steel_hn_plastic_modulus_z()) + 0.5 * self.fcd1() * (self.concrete_plastic_modulus_z() - self.concrete_hn_plastic_modulus_z()) + self.fsd() * (self.reinforcement_plastic_modulus_z() - self.reinforcement_hn_plastic_modulus_z()) 

    def plastic_bending_moment_y(self):
        return self.fyd() * (self.steel_plastic_modulus_y() - self.steel_hn_plastic_modulus_y()) + 0.5 * self.fcd1() * (self.concrete_plastic_modulus_y() - self.concrete_hn_plastic_modulus_y()) + self.fsd() * (self.reinforcement_plastic_modulus_y() - self.reinforcement_hn_plastic_modulus_y()) 

    def maximum_plastic_bending_moment_z(self):
        return self.fyd() * (self.steel_plastic_modulus_z()) + 0.5 * self.fcd1() * (self.concrete_plastic_modulus_z()) + self.fsd() * (self.reinforcement_plastic_modulus_z()) 

    def maximum_plastic_bending_moment_y(self):
        return self.fyd() * (self.steel_plastic_modulus_y()) + 0.5 * self.fcd1() * (self.concrete_plastic_modulus_y()) + self.fsd() * (self.reinforcement_plastic_modulus_y()) 
    
    def calculate_tube_width_thickness_ratio(self):
        return self.tube_diameter / self.thickness
    
    def calculate_compression_width_thickness_ratio_limit(self):
        return ( 0.15 * self.steel_modulus / self.fyk )
    
    def calculate_compression_width_thickness_ratio_residual(self):
        return ( 0.19 * self.steel_modulus / self.fyk )

    def calculate_bending_width_thickness_ratio_limit(self):
        return ( 0.09 * self.steel_modulus / self.fyk )

    def calculate_bending_width_thickness_ratio_residual(self):
        return ( 0.31 * self.steel_modulus / self.fyk )
    
    def verify_tube_compression_ratio(self):
        if self.calculate_tube_width_thickness_ratio() <= self.calculate_compression_width_thickness_ratio_limit():
            return 'COMPACT'
        elif self.calculate_tube_width_thickness_ratio() <= self.calculate_compression_width_thickness_ratio_residual():
            return 'NON-COMPACT'
        elif self.calculate_tube_width_thickness_ratio() <= self.calculate_bending_width_thickness_ratio_residual():
            return 'SLENDER'
        else:
            return 'OUTSIDE OF CODE SCOPE'
        
    def verify_tube_bending_ratio(self):
        if self.calculate_tube_width_thickness_ratio() <= self.calculate_bending_width_thickness_ratio_limit():
            return 'COMPACT'
        elif self.calculate_tube_width_thickness_ratio() <= self.calculate_bending_width_thickness_ratio_residual():
            return 'NON-COMPACT'
        else:
            return 'OUTSIDE OF CODE SCOPE'