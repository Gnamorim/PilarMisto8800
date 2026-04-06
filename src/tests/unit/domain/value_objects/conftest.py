import pytest

from MY_PACKAGE.domain.value_objects.ObjetoConcreto import ConcretoNormal
from MY_PACKAGE.domain.value_objects.ObjetoAco import AcoEstrutural, AcoArmadura


@pytest.fixture
def concreto():
    return ConcretoNormal(fck=40)


@pytest.fixture
def aco_estrutural():
    return AcoEstrutural(fy=345)


@pytest.fixture
def aco_armadura():
    return AcoArmadura(fy=500)
