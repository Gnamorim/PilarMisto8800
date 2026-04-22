from domain.sections.circular_cfst import CircularCFST
from math import isclose
import pytest


class TestCircularCFST:

    # TESTE PARA CONSTRUIR A CLASSE CIRCULAR CFST:
    def test_circular_cfst_initialization(self):

        # variable definition
        tube_diameter = 100.0 # mm
        thickness = 1.0 # mm
        fyk = 300 # MPa
        gama_a = 1.1
        bar_diameter = 10. # mm
        bar_number = 6
        stirrup = 5 
        fsk = 500 # MPa
        gama_s = 1.15
        cover = 25.0 # mm
        fck = 30 # MPa
        gama_c = 1.4 
        moe_c = 30000
        moe_s = 200000
        moe_rs = 210000
        
        # creating instance
        cfst = CircularCFST(tube_diameter=tube_diameter, thickness=thickness, fyk=fyk, gamma_a = gama_a, fsk=fsk, bar_diameter=bar_diameter, stirrup_diameter=stirrup, bar_number=bar_number, gamma_s=gama_s, concrete_cover=cover, fck=fck,gamma_c=gama_c, concrete_modulus = moe_c, steel_modulus = moe_s, reinforcement_modulus = moe_rs)
        cfst1 = CircularCFST(tube_diameter=tube_diameter, thickness=thickness, fyk=fyk, fck=fck)

        assert cfst.tube_diameter == tube_diameter
        assert cfst.thickness == thickness  
        assert cfst.fyk == fyk
        assert cfst.gamma_a == gama_a
        assert cfst.fsk == fsk
        assert cfst.bar_diameter == bar_diameter
        assert cfst.bar_number == bar_number
        assert cfst.stirrup_diameter == stirrup
        assert cfst.gamma_s == gama_s
        assert cfst.concrete_cover == cover
        assert cfst.fck == fck
        assert cfst.gamma_c == gama_c
        assert cfst.concrete_modulus == moe_c
        assert cfst.steel_modulus == moe_s
        assert cfst.reinforcement_modulus == moe_rs
        assert cfst.internal_diameter == tube_diameter-2*thickness

        assert cfst1.tube_diameter == tube_diameter
        assert cfst1.thickness == thickness  
        assert cfst1.fyk == fyk
        assert cfst1.gamma_a == 1.1
        assert cfst1.bar_diameter == 0
        assert cfst1.bar_number == 0
        assert cfst1.stirrup_diameter == 0
        assert cfst1.gamma_s == 1.15
        assert cfst1.concrete_cover == 25.
        assert cfst1.fck == fck
        assert cfst1.gamma_c == 1.4
        assert cfst1.concrete_modulus == 30000
        assert cfst1.steel_modulus == 200000
        assert cfst1.reinforcement_modulus == 210000
        assert cfst1.internal_diameter == tube_diameter-2*thickness

    def test_tube_validation(self):
                
        # variable definition
        tube_diameter =  'a'# mm
        thickness = 1 # mm
        fyk = 300 # MPa
        fck = 30 # MPa
        with pytest.raises(TypeError, match= 'tube diameter must be a float or an integer'):
            CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, fck=fck)


    def test_thickness_validation(self):
                
        # variable definition
        tube_diameter =  100 # mm
        thickness ='a' # mm
        fyk = 300 # MPa
        fck = 30 # MPa
        with pytest.raises(TypeError, match= 'thickness must be a float or an integer'):
            CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, fck=fck)
    
    def test_fyk_validation(self):
                
        # variable definition
        tube_diameter =  100 # mm
        thickness = 1 # mm
        fyk = 'a' # MPa
        fck = 30 # MPa
        with pytest.raises(TypeError, match= 'fyk must be a float or an integer'):
            CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, fck=fck)

    def test_concrete_cover_validation(self):
                
        # variable definition
        tube_diameter =  100 # mm
        thickness = 1 # mm
        fyk = 100 # MPa
        cover = True # mm
        fck = 30 # MPa
        with pytest.raises(TypeError, match= 'concrete cover must be a float or an integer'):
            CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, concrete_cover = cover, fck=fck)

    def test_fck_validation(self):
                
        # variable definition
        tube_diameter =  100 # mm
        thickness = 1 # mm
        fyk = 100 # MPa
        fck = False # MPa
        with pytest.raises(TypeError, match= 'fck must be a float or an integer'):
            CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, fck=fck)

    def test_fsk_validation(self):
                
        # variable definition
        tube_diameter =  100 # mm
        thickness = 1 # mm
        fyk = 100 # MPa
        fck = 50 # MPa
        fsk = False
        with pytest.raises(TypeError, match= 'fsk must be a float or an integer'):
            CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, fck=fck, fsk = fsk)

    def test_steel_modulus_validation(self):
                
        # variable definition
        tube_diameter =  100 # mm
        thickness = 1 # mm
        fyk = 100 # MPa
        fck = 30 # MPa
        moe = 'a'
        with pytest.raises(TypeError, match= 'steel_modulus must be a float or an integer'):
            CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, fck=fck, steel_modulus=moe)

    def test_concrete_modulus_validation(self):
                
        # variable definition
        tube_diameter =  100 # mm
        thickness = 1 # mm
        fyk = 100 # MPa
        fck = 30 # MPa
        moe = 'a'
        with pytest.raises(TypeError, match= 'concrete_modulus must be a float or an integer'):
            CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, fck=fck, concrete_modulus=moe)

    def test_reinforcement_modulus_validation(self):
                
        # variable definition
        tube_diameter =  100 # mm
        thickness = 1 # mm
        fyk = 100 # MPa
        fck = 30 # MPa
        moe = True
        with pytest.raises(TypeError, match= 'reinforcement_modulus must be a float or an integer'):
            CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, fck=fck, reinforcement_modulus= moe)

            
    def test_bar_number_validation(self):
                
        # variable definition
        tube_diameter =  100 # mm
        thickness = 1 # mm
        fyk = 100 # MPa
        fck = 30 # MPa
        bar_number = 'a'
        with pytest.raises(TypeError, match= 'the number of bars must be an integer'):
            CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, fck=fck, bar_number=bar_number)

    def test_bar_diameter_validation(self):
                
        # variable definition
        tube_diameter =  100 # mm
        thickness = 1 # mm
        fyk = 100 # MPa
        fck = 30 # MPa
        bar_diameter = 'a'
        with pytest.raises(TypeError, match= 'bar diameter must be a float or an integer'):
            CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, fck=fck, bar_diameter = bar_diameter)

    def test_stirrup_diameter_validation(self):
                
        # variable definition
        tube_diameter =  100 # mm
        thickness = 1 # mm
        fyk = 100 # MPa
        fck = 30 # MPa
        stirrup = False
        with pytest.raises(TypeError, match= 'stirrup diameter must be a float or an integer'):
            CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, fck=fck, stirrup_diameter=stirrup)

    def test_gamma_a_validation(self):
                
        # variable definition
        tube_diameter =  100 # mm
        thickness = 1 # mm
        fyk = 100 # MPa
        fck = 30 # MPa
        gama_a = 1
        with pytest.raises(TypeError, match= 'Gamma A must be a float'):
            CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, fck=fck, gamma_a = gama_a)

    def test_gamma_s_validation(self):
                
        # variable definition
        tube_diameter =  100 # mm
        thickness = 1 # mm
        fyk = 100 # MPa
        fck = 30 # MPa
        gama_a = 1
        with pytest.raises(TypeError, match= 'Gamma S must be a float'):
            CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, fck=fck, gamma_s = gama_a)

    def test_gamma_c_validation(self):
                
        # variable definition
        tube_diameter =  100 # mm
        thickness = 1 # mm
        fyk = 100 # MPa
        fck = 30 # MPa
        gama_a = 1
        with pytest.raises(TypeError, match= 'Gamma C must be a float'):
            CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, fck=fck, gamma_c = gama_a)

    def test_confliction_info_on_longitudinal_reinforcement(self):

        # variable definition
        tube_diameter =  100 # mm
        thickness = 1 # mm
        fyk = 100 # MPa
        fck = 30 # MPa
        bar_number = 0
        bar_diameter = 10
        fsk = 10

        Asr = 0
        with pytest.warns(UserWarning, match= 'reinforcement diameter, the number of the bars or the reinforcement strength is defined as 0. the reinforcements will not be considered'):
            CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, fck=fck, bar_number= bar_number, bar_diameter= bar_diameter, fsk = fsk)

        cfst = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, fck=fck, bar_number= bar_number, bar_diameter= bar_diameter, fsk = fsk) 
        tol = 1e-1
        assert isclose(cfst.reinforcement_area(), Asr, rel_tol=tol)
        assert isclose(cfst.reinforcement_inertia_y(), 0, rel_tol=tol)


    def test_cfst_geometric_characteristics(self):
                        
        # variable definition
        tube_diameter =  95 # mm
        thickness = 12.5 # mm
        fyk = 100 # MPa
        cover = 25 # mm
        fck = 30 # MPa
        bar_diameter = 10
        bar_number = 4
        fsk = 500
        As = 3239.77
        Asr = 0
        Ac = 3848.45
        Isz = 2.82 * 1e6
        Isy = Isz
        Isrz = 0
        Isry = 0
        Icz = 1.18 * 1e6
        Icy = Icz

        #test with reinforcements 
        As1 = 3239.77
        Asr1 = 314.1593
        Ac1 = 3534.29
        Isz1 = 2.82 * 1e6
        Isy1 = Isz1
        Isrz1 = 5890.4862
        Isry1 = 5890.4862
        Icz1 = 1.172697 * 1e6
        Icy1 = Icz1


        cfst = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, concrete_cover = cover, fck=fck)

        cfst1 = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk,
                             fck=fck, bar_diameter=bar_diameter, bar_number=bar_number, fsk = fsk)

        tol = 1e-2
        assert isclose(cfst.steel_area(), As, rel_tol=tol)
        #assert cfst.steel_area() == pytest.approx(As, rel=1e-9)
        assert isclose(cfst.reinforcement_area(), Asr, rel_tol=tol)
        assert isclose(cfst.concrete_area(), Ac, rel_tol=tol)
        assert isclose(cfst.steel_inertia_z(), Isz, rel_tol=tol)
        assert isclose(cfst.steel_inertia_y(), Isy, rel_tol=tol)
        assert isclose(cfst.reinforcement_inertia_z(), Isrz, rel_tol=tol)
        assert isclose(cfst.reinforcement_inertia_y(), Isry, rel_tol=tol)
        assert isclose(cfst.concrete_inertia_z(), Icz, rel_tol=tol)
        assert isclose(cfst.concrete_inertia_y(), Icy, rel_tol=tol)

        # relative to cfst1
        assert isclose(cfst1.steel_area(), As1, rel_tol=tol)
        #assert cfst1.steel_area() == pytest.approx(As, rel=1e-9)
        assert isclose(cfst1.reinforcement_area(), Asr1, rel_tol=tol)
        assert isclose(cfst1.concrete_area(), Ac1, rel_tol=tol)
        assert isclose(cfst1.steel_inertia_z(), Isz1, rel_tol=tol)
        assert isclose(cfst1.steel_inertia_y(), Isy1, rel_tol=tol)
        assert isclose(cfst1.reinforcement_inertia_z(), Isrz1, rel_tol=tol)
        assert isclose(cfst1.reinforcement_inertia_y(), Isry1, rel_tol=tol)
        assert isclose(cfst1.concrete_inertia_z(), Icz1, rel_tol=tol)
        assert isclose(cfst1.concrete_inertia_y(), Icy1, rel_tol=tol)


    def test_cfst_material_design_strength(self):
                        
        # variable definition
        tube_diameter =  600 # mm
        thickness = 9.5 # mm
        fyk = 345 # MPa
        cover = 25 # mm
        fck = 40 # MPa
        fsk = 500
        bar_diameter = 20.0
        bar_number = 10
        stirrup = 5
        fyd = fyk/1.1
        fcd = fck/1.4
        fsd = fsk/1.15
        gc = 1.5
        fcd_test2 = fck/gc
        fcd1 = 0.95 * fcd


        cfst = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fsk = fsk, fyk= fyk, concrete_cover = cover, fck=fck, bar_diameter=bar_diameter, bar_number=bar_number,stirrup_diameter=stirrup)

        # altering the concrete gamma to 1.5
        cfst1 = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, concrete_cover = cover, fck=fck, bar_diameter=bar_diameter, bar_number=bar_number,stirrup_diameter=stirrup, gamma_c= gc)

        tol = 1e-9
        assert isclose(cfst.fyd(), fyd, rel_tol=tol)
        assert isclose(cfst.fcd(), fcd, rel_tol=tol)
        assert isclose(cfst.fcd1(), fcd1, rel_tol=tol)
        assert isclose(cfst.fsd(), fsd, rel_tol=tol)

        assert isclose(cfst1.fcd(), fcd_test2, rel_tol=tol)

    def test_cfst_design_strength(self):
                        
        # variable definition
        tube_diameter =  600 # mm
        thickness = 9.5 # mm
        fyk = 345 # MPa
        cover = 25 # mm
        fck = 40 # MPa
        bar_diameter = 20.0
        bar_number = 10
        stirrup = 5
        fsk = 500
        moe_c = 30000
        moe_rs = 210000
        nplrds = 5.5274e6
        nplrdrs = 5.969e5
        nplrdc = 7.1108e6
        nplrd = 1.33204e7
        nplrdc2 = 7.1961e6
        nplrds2 = 5.5274e6
        nplrd2 = nplrdc2 + nplrds2


        cfst = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, concrete_cover = cover, fck=fck, bar_diameter=bar_diameter, bar_number=bar_number,stirrup_diameter=stirrup, reinforcement_modulus= moe_rs, concrete_modulus= moe_c, fsk = fsk)

        # not considering reinforcement in the test
        cfst1 = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, concrete_cover = cover, fck=fck, stirrup_diameter=stirrup, reinforcement_modulus= moe_rs, concrete_modulus= moe_c)

        tol = 1e-2
        assert isclose(cfst.steel_axial_strength(), nplrds, rel_tol=tol)
        assert isclose(cfst.reinforcement_axial_strength(), nplrdrs, rel_tol=tol)
        assert isclose(cfst.concrete_axial_strength(), nplrdc, rel_tol=tol)
        assert isclose(cfst.section_axial_strength(), nplrd, rel_tol=tol)

        # relative to cfst1
        assert isclose(cfst1.steel_axial_strength(), nplrds2, rel_tol=tol)
        assert isclose(cfst1.reinforcement_axial_strength(), 0, rel_tol=tol)
        assert isclose(cfst1.concrete_axial_strength(), nplrdc2, rel_tol=tol)
        assert isclose(cfst1.section_axial_strength(), nplrd2, rel_tol=tol)

    def test_plastic_modulus(self):
                        
        # variable definition
        tube_diameter =  600 # mm
        thickness = 9.5 # mm
        fyk = 345 # MPa
        cover = 25 # mm
        fck = 40 # MPa
        bar_diameter = 20.0
        bar_number = 10
        stirrup = 5
        fsk = 500
        moe_c = 30000
        moe_rs = 210000

        Zaz = 3.3121e6
        Zay = Zaz
        Zsz = 4.8441e5
        Zsy = 5.0934e5
        Zcz = 3.2203e7
        Zcy = 3.2178e7

        Zsz1 = 0
        Zsy1 = 0
        Zcz1 = 3.2687e7
        Zcy1 = Zcz1

        cfst = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, concrete_cover = cover, fck=fck, bar_diameter=bar_diameter, bar_number=bar_number,stirrup_diameter=stirrup, reinforcement_modulus= moe_rs, concrete_modulus= moe_c, fsk = fsk)

        # not considering reinforcement in the test
        cfst1 = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, concrete_cover = cover, fck=fck, stirrup_diameter=stirrup, reinforcement_modulus= moe_rs, concrete_modulus= moe_c)

        tol = 1e-2
        assert isclose(cfst.steel_plastic_modulus_z(), Zaz, rel_tol=tol)
        assert isclose(cfst.steel_plastic_modulus_y(), Zay, rel_tol=tol)
        assert isclose(cfst.reinforcement_plastic_modulus_z(), Zsz, rel_tol=tol)
        assert isclose(cfst.reinforcement_plastic_modulus_y(), Zsy, rel_tol=tol)
        assert isclose(cfst.concrete_plastic_modulus_z(), Zcz, rel_tol=tol)
        assert isclose(cfst.concrete_plastic_modulus_y(), Zcy, rel_tol=tol)

        # considering cfst1
        assert isclose(cfst1.reinforcement_plastic_modulus_z(), Zsz1, rel_tol=tol)
        assert isclose(cfst1.reinforcement_plastic_modulus_y(), Zsy1, rel_tol=tol)
        assert isclose(cfst1.concrete_plastic_modulus_z(), Zcz1, rel_tol=tol)
        assert isclose(cfst1.concrete_plastic_modulus_y(), Zcy1, rel_tol=tol)

    def test_plastic_modulus2(self):

        # variable definition
        tube_diameter =  600 # mm
        thickness = 9.5 # mm
        fyk = 345 # MPa
        cover = 25 # mm
        fck = 40 # MPa
        bar_diameter = 20.0
        bar_number = 10
        stirrup = 5
        fsk = 500
        moe_c = 30000
        moe_rs = 210000

        hnz = 118.8508
        Asnz = 628.3185
        hny = 109.2924
        Asny = 1256.6371


        Zsnz = 0
        Zsny = 97274.713
        Zcnz = 8.2069e6
        Zcny = 6.8427e6
        Zanz = 2.6838e5
        Zany = 2.2695e5

        hnz1 = 129.9491
        hny1 = 129.9491

        Zsnz1 = 0
        Zsny1 = 0
        Zcnz1 = 9.8112e6
        Zcny1 = 9.8112e6
        Zanz1 = 3.2085e5
        Zany1 = 3.2085e5

        cfst = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, concrete_cover = cover, fck=fck, bar_diameter=bar_diameter, bar_number=bar_number,stirrup_diameter=stirrup, reinforcement_modulus= moe_rs, concrete_modulus= moe_c, fsk = fsk)

        # not considering reinforcement in the test
        cfst1 = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, concrete_cover = cover, fck=fck, stirrup_diameter=stirrup, reinforcement_modulus= moe_rs, concrete_modulus= moe_c)

        tol = 1e-2
        
        assert isclose(cfst.hn_z_axis, hnz, rel_tol= tol)
        assert isclose(cfst.z_axis_asn, Asnz, rel_tol= tol)
        assert isclose(cfst.hn_y_axis, hny, rel_tol= tol)
        assert isclose(cfst.y_axis_asn, Asny, rel_tol= tol)
        
        assert isclose(cfst.reinforcement_hn_plastic_modulus_z(), Zsnz, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst.reinforcement_hn_plastic_modulus_y(), Zsny, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst.concrete_hn_plastic_modulus_z(), Zcnz, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst.concrete_hn_plastic_modulus_y(), Zcny, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst.steel_hn_plastic_modulus_z(), Zanz, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst.steel_hn_plastic_modulus_y(), Zany, abs_tol=tol, rel_tol= tol)

        # considering cfst1
        assert isclose(cfst1.hn_z_axis, hnz1, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst1.z_axis_asn, 0, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst1.hn_y_axis, hny1, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst1.y_axis_asn, 0, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst1.y_axis_asn, 0, abs_tol=tol, rel_tol= tol)
        
        assert isclose(cfst1.reinforcement_hn_plastic_modulus_z(), Zsnz1, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst1.reinforcement_hn_plastic_modulus_y(), Zsny1, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst1.concrete_hn_plastic_modulus_z(), Zcnz1, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst1.concrete_hn_plastic_modulus_y(), Zcny1, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst1.steel_hn_plastic_modulus_z(), Zanz1, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst1.steel_hn_plastic_modulus_y(), Zany1, abs_tol=tol, rel_tol= tol)

    def test_plastic_moment_z(self):

        # variable definition
        tube_diameter =  600 # mm
        thickness = 9.5 # mm
        fyk = 345 # MPa
        cover = 25 # mm
        fck = 40 # MPa
        bar_diameter = 20.0
        bar_number = 10
        stirrup = 5
        fsk = 500
        moe_c = 30000
        moe_rs = 210000

        Mpl = 1.4911e9
        Mmax = 1.6867e9

        Mpl1 = 1.2489e9
        Mmax1 = 1.4826e9

        cfst = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, concrete_cover = cover, fck=fck, bar_diameter=bar_diameter, bar_number=bar_number,stirrup_diameter=stirrup, reinforcement_modulus= moe_rs, concrete_modulus= moe_c, fsk = fsk)

        # not considering reinforcement in the test
        cfst1 = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, concrete_cover = cover, fck=fck, stirrup_diameter=stirrup, reinforcement_modulus= moe_rs, concrete_modulus= moe_c)

        tol = 1e-2

        assert isclose(cfst.plastic_bending_moment_z(), Mpl, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst.maximum_plastic_bending_moment_z(), Mmax, abs_tol=tol, rel_tol= tol)

        # considering cfst1
        assert isclose(cfst1.plastic_bending_moment_z(), Mpl1, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst1.maximum_plastic_bending_moment_z(), Mmax1, abs_tol=tol, rel_tol= tol)

    def test_plastic_moment_y(self):

        # variable definition
        tube_diameter =  600 # mm
        thickness = 9.5 # mm
        fyk = 345 # MPa
        cover = 25 # mm
        fck = 40 # MPa
        bar_diameter = 20.0
        bar_number = 10
        stirrup = 5
        fsk = 500
        moe_c = 30000
        moe_rs = 210000

        Mpl = 1.4908e9
        Mmax = 1.6972e9

        Mpl1 = 1.2489e9
        Mmax1 = 1.4826e9

        cfst = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, concrete_cover = cover, fck=fck, bar_diameter=bar_diameter, bar_number=bar_number,stirrup_diameter=stirrup, reinforcement_modulus= moe_rs, concrete_modulus= moe_c, fsk = fsk)

        # not considering reinforcement in the test
        cfst1 = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, concrete_cover = cover, fck=fck, stirrup_diameter=stirrup, reinforcement_modulus= moe_rs, concrete_modulus= moe_c)

        tol = 1e-2

        assert isclose(cfst.plastic_bending_moment_y(), Mpl, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst.maximum_plastic_bending_moment_y(), Mmax, abs_tol=tol, rel_tol= tol)

        # considering cfst1
        assert isclose(cfst1.plastic_bending_moment_y(), Mpl1, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst1.maximum_plastic_bending_moment_y(), Mmax1, abs_tol=tol, rel_tol= tol)

    def test_tube_width_thickness_ratio(self):
        # variable definition
        tube_diameter =  600 # mm
        thickness = 9.5 # mm
        fyk = 345 # MPa
        cover = 25 # mm
        fck = 40 # MPa
        bar_diameter = 20.0
        bar_number = 10
        stirrup = 5
        fsk = 500
        moe_c = 30000
        moe_rs = 210000
        moe_s = 200000

        compl = 86.9565
        compr = 110.1449
        moml = 52.1739
        momr = 179.7101

        cfst = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, concrete_cover = cover, steel_modulus=moe_s, fck=fck, bar_diameter=bar_diameter, bar_number=bar_number,stirrup_diameter=stirrup, reinforcement_modulus= moe_rs, concrete_modulus= moe_c, fsk = fsk)

        tol =1e-2
        assert isclose(cfst.calculate_tube_width_thickness_ratio(), tube_diameter/thickness, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst.calculate_compression_width_thickness_ratio_limit(), compl, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst.calculate_compression_width_thickness_ratio_residual(), compr, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst.calculate_bending_width_thickness_ratio_limit(), moml, abs_tol=tol, rel_tol= tol)
        assert isclose(cfst.calculate_bending_width_thickness_ratio_residual(), momr, abs_tol=tol, rel_tol= tol)
        
        
    def test_compact_verification(self):

        # variable definition
        tube_diameter =  600 # mm
        thickness = 9.5 # mm
        fyk = 345 # MPa
        cover = 25 # mm
        fck = 40 # MPa
        bar_diameter = 20.0
        bar_number = 10
        stirrup = 5
        fsk = 500
        moe_c = 30000
        moe_rs = 210000
        moe_s = 200000

        cfst = CircularCFST(tube_diameter=tube_diameter, thickness= thickness, fyk= fyk, concrete_cover = cover, steel_modulus=moe_s, fck=fck, bar_diameter=bar_diameter, bar_number=bar_number,stirrup_diameter=stirrup, reinforcement_modulus= moe_rs, concrete_modulus= moe_c, fsk = fsk)

        assert cfst.verify_tube_compression_ratio() == 'COMPACT'
        assert cfst.verify_tube_bending_ratio() == 'NON-COMPACT'