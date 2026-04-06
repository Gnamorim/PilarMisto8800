from typing import Sequence, Tuple

from MY_PACKAGE.domain.value_objects.ObjetoPilarMisto import ObjetoPilarMisto
from MY_PACKAGE.domain.services._flexo_compressao import MetodoBase
from MY_PACKAGE.domain.value_objects._classe_secao import Secao

class MetodoII(MetodoBase):

    """
    Implementa o Método de Calculo II conforme M.5.3

    valido apenas para pilares compactos.
    Verifica a compacidade antes de aplicar seus metodos.
    """
    def _verificar_compacidade(self,
        objeto_pilar_misto: ObjetoPilarMisto
    ) -> None:
        
        if objeto_pilar_misto.esbeltez_flexao != Secao.COMPACTO:
            raise TypeError("Método II não suporta pilares não-compactos")


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

        Valido apenas para pilares compactos (verificados na flexão)
        """
        
        return_list = []
        
        # verifica se precisa ser adicionado um momento devido à fluencia
        mcc_x = self._calcular_momento_adicional_x(objeto_pilar_misto,carregamento)
        mcc_y = self._calcular_momento_adicional_y(objeto_pilar_misto,carregamento)

        for caso in carregamento:
            if design:
                n = objeto_pilar_misto.capacidade_axial_resistente_pilar_design
                npl = objeto_pilar_misto.capacidade_axial_plastico_design()
                nc = objeto_pilar_misto.capacidade_axial_plastico_concreto_design()
                mx = objeto_pilar_misto.momento_resistente_plastico_total_design_xx
                my = objeto_pilar_misto.momento_resistente_plastico_total_design_yy
                mx_max = objeto_pilar_misto.momento_resistente_maximo_plastico_total_design_xx
                my_max = objeto_pilar_misto.momento_resistente_maximo_plastico_total_design_yy
            else:
                n = objeto_pilar_misto.capacidade_axial_resistente_pilar_nominal
                npl = objeto_pilar_misto.capacidade_axial_plastico()
                nc = objeto_pilar_misto.capacidade_axial_plastico_concreto()
                mx = objeto_pilar_misto.momento_resistente_plastico_total_xx
                my = objeto_pilar_misto.momento_resistente_plastico_total_yy
                mx_max = objeto_pilar_misto.momento_resistente_maximo_plastico_total_xx
                my_max = objeto_pilar_misto.momento_resistente_maximo_plastico_total_yy

            # cria as variaveis a serem usadas 
            ns = caso[0]
            ms_x = caso[1] + mcc_x
            ms_y = caso[2] + mcc_y
            mx_max_red = 0.8 * mx_max
            my_max_red = 0.8 * my_max

            # redução do momento resistente em função de fy
            if objeto_pilar_misto.material_aco_estrutural.fy <= 350.0:
                mx_red = 0.9 * mx
                my_red = 0.9 * my
            else:
                mx_red = 0.8 * mx
                my_red = 0.8 * my

            # se o momento maximo reduzido for menor que o momento plastico reduzido, iguala-se ao momento plastico
            if mx_max_red < mx_red:
                mx_max_red = mx_red

            if my_max_red < my_red:
                my_max_red = my_red

            
            # verificação Nsd e Nrd
            if ns > n:
                v1 = False
            elif ns >= nc:
                v1 = True
                mu_x = 1 - ((ns - nc) / (npl - nc))
                mu_y = 1 - ((ns - nc) / (npl - nc))
            elif ns >= nc/2:
                v1 = True
                mu_x = ((1 - (mx_max_red / mx_red)) * (2 * (ns / npl) - 1) + (mx_max_red / mx_red))
                mu_y = ((1 - (my_max_red / my_red)) * (2 * (ns / npl) - 1) + (my_max_red / my_red))
            else:
                v1 = True
                mu_x = 1 + (2 * (ns/ nc) * ((mx_max_red / mx_red) - 1))
                mu_y = 1 + (2 * (ns/ nc) * ((my_max_red / my_red) - 1))

            # verificação dos momentos fletores 
            inequacao = ((ms_x / (mu_x * mx_red)) + (ms_y / (mu_y * my_red)))

            if inequacao <= 1.0:
                v2 = True
            else: 
                v2 = False

            # True se ambas as verificações passarem
            return_list.append(v1 and v2)
        
        return return_list

            


