from abc import ABC, abstractmethod
from typing import Sequence, Tuple
from math import e

from MY_PACKAGE.domain.value_objects.ObjetoPilarMisto import ObjetoPilarMisto

class MetodoBase(ABC):
    """
    Classe stateless: não armazena estado interno.
    Apenas processa dados recebidos.

    Considera [[Nsd; Msd,x; Msd,y]]
    """

    def _validar_carregamento(self, dados: Sequence[Tuple[float, float, float]]):
        for i, grupo in enumerate(dados):
            if len(grupo) != 3:
                raise ValueError(f"Grupo {i} não tem 3 valores: {grupo}")
            
    
    def _calcular_momento_adicional_x(
        self,
        objeto_pilar_misto: ObjetoPilarMisto,
        carregamento: Sequence[Tuple[float, float, float]]
    ):
        self._validar_carregamento(carregamento)

        mcc_list = []

        for caso in carregamento:
            if objeto_pilar_misto._incluir_momento_adicional:
                
                Nsd = caso[0]
                m_n = caso[1]/caso[0]
                # m = phi * 0.45 / ((Ne,x/ Nsd) - 0.45)
                m = objeto_pilar_misto.coeficiente_fluencia * 0.45 / ((objeto_pilar_misto._carga_flambagem_elastica_x/Nsd) - 0.45)

                # considerando que a equação leva L como centímetro e minhas equações são milímetro {L/3000}
                l_eq = objeto_pilar_misto.comprimento_pilar_destravado / 3000

                ecc = ((e ** m) - 1) * (m_n + l_eq)

                Mcc = Nsd * ecc

                mcc_list.append(Mcc)
            else:
                mcc_list.append(0.0)

        return mcc_list
    
    def _calcular_momento_adicional_y(
        self,
        objeto_pilar_misto: ObjetoPilarMisto,
        carregamento: Sequence[Tuple[float, float, float]]
    ):
        self._validar_carregamento(carregamento)

        mcc_list = []

        for caso in carregamento:
            if objeto_pilar_misto._incluir_momento_adicional:
                
                Nsd = caso[0]
                m_n = caso[2]/caso[0]
                # m = phi * 0.45 / ((Ne,x/ Nsd) - 0.45)
                m = objeto_pilar_misto.coeficiente_fluencia * 0.45 / ((objeto_pilar_misto._carga_flambagem_elastica_y/Nsd) - 0.45)

                # considerando que a equação leva L como centímetro e minhas equações são milímetro {L/3000}
                l_eq = objeto_pilar_misto.comprimento_pilar_destravado / 3000

                ecc = ((e ** m) - 1) * (m_n + l_eq)

                Mcc = Nsd * ecc

                mcc_list.append(Mcc)
            else:
                mcc_list.append(0.0)

        return mcc_list
             




