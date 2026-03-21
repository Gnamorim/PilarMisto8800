import pytest
import numpy as np

from MY_PACKAGE.domain.value_objects.pilar_misto_circular import PilarCircularPreenchido
from MY_PACKAGE.domain.value_objects.ObjetoConcreto import ConcretoNormal
from MY_PACKAGE.domain.value_objects.ObjetoAco import AcoEstrutural, AcoArmadura


# -------------------------
# Fixtures (objetos base)
# -------------------------

@pytest.fixture
def concreto():
    return ConcretoNormal(fck=30)

@pytest.fixture
def aco_estrutural():
    return AcoEstrutural(fy=355)

@pytest.fixture
def aco_armadura():
    return AcoArmadura(fy=500)


# -------------------------
# Casos válidos
# -------------------------

def test_criacao_sem_armadura(concreto, aco_estrutural):
    pilar = PilarCircularPreenchido(
        diametro_tubo=0.3,
        espessura_tubo=0.01,
        material_aco_estrutural=aco_estrutural,
        material_concreto=concreto,
        material_armadura=None
    )

    assert pilar.material_armadura is None
    assert pilar.numero_armadura_longitudinal == 0