from typing import Sequence, Tuple

from MY_PACKAGE.domain.value_objects.ObjetoPilarMisto import ObjetoPilarMisto
from MY_PACKAGE.domain.services._flexo_compressao import MetodoBase

class MetodoI(MetodoBase):

    """
    Implementa o Método de Calculo I conforme M.5.2

    valido para todos os tipos de pilares
    """

    def comparar_solicitacao(
        self,
        objeto_pilar_misto: ObjetoPilarMisto,
        carregamento: Sequence[Tuple[float, float, float]],
        design: bool = True
    ) -> list[bool]:
        
        """
        Retorna uma lista de valores booleanos comparando a solicitação resistente com solicitante.
        True -> passou
        False -> não passou
        """
        
        return_list = []
        
        mcc_x = self._calcular_momento_adicional_x(objeto_pilar_misto,carregamento)
        mcc_y = self._calcular_momento_adicional_y(objeto_pilar_misto,carregamento)

        for indice, caso in enumerate(carregamento):
            if design:
                verificador = caso[0] / objeto_pilar_misto.capacidade_axial_resistente_pilar_design
                mx = objeto_pilar_misto.momento_resistente_plastico_total_design_xx
                my = objeto_pilar_misto.momento_resistente_plastico_total_design_yy
            else:
                verificador = caso[0] / objeto_pilar_misto.capacidade_axial_resistente_pilar_nominal
                mx = objeto_pilar_misto.momento_resistente_plastico_total_xx
                my = objeto_pilar_misto.momento_resistente_plastico_total_yy 
            
            msx = mcc_x[indice] + caso[1]
            msy = mcc_y[indice] + caso[2]
            
            if verificador >= 0.2:
                result = verificador + (8 / 9) * ((msx / mx) + (msy / my))
            else:
                result = (verificador / 2) + ((msx / mx) + (msy / my))

            if result <= 1.0:
                return_list.append(True)
            else:
                return_list.append(False)
            
        return return_list
    

    



