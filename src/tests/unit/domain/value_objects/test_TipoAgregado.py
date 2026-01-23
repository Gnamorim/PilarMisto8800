from MY_PACKAGE.domain.value_objects.ObjetoConcreto import TipoAgregado
from enum import Enum
import pytest

class TestTipoAgregadoBasico:
    """Testes básicos da enumeração TipoAgregado"""
    
    def test_tipo_enum(self):
        """Verifica que TipoAgregado é uma subclasse de Enum"""
        assert issubclass(TipoAgregado, Enum)
    
    def test_membros_enum(self):
        """Verifica que todos os membros estão definidos"""
        assert hasattr(TipoAgregado, 'BASALTO')
        assert hasattr(TipoAgregado, 'DIABASIO')
        assert hasattr(TipoAgregado, 'GRANITO')
        assert hasattr(TipoAgregado, 'GNAISSE')
        assert hasattr(TipoAgregado, 'CALCARIO')
        assert hasattr(TipoAgregado, 'ARENITO')
    
    def test_valores_corretos(self):
        """Testa valores numéricos de cada tipo de agregado"""
        # Teste específico para cada valor
        assert TipoAgregado.BASALTO.value == 1.2
        assert TipoAgregado.DIABASIO.value == 1.2
        assert TipoAgregado.GRANITO.value == 1.0
        assert TipoAgregado.GNAISSE.value == 1.0
        assert TipoAgregado.CALCARIO.value == 0.9
        assert TipoAgregado.ARENITO.value == 0.7
    
    def test_nomes_corretos(self):
        """Testa nomes dos membros da enumeração"""
        assert TipoAgregado.BASALTO.name == "BASALTO"
        assert TipoAgregado.DIABASIO.name == "BASALTO" # caracterista do enum Basalto = Diabasio = 1.2
        assert TipoAgregado.GRANITO.name == "GRANITO"
        assert TipoAgregado.GNAISSE.name == "GRANITO" # caracterista do enum Granito = Gnaisse = 1.0
        assert TipoAgregado.CALCARIO.name == "CALCARIO"
        assert TipoAgregado.ARENITO.name == "ARENITO"

    def test_valor_invalido(self):
        """Testa que valor não existente levanta exceção"""
        with pytest.raises(ValueError):
            TipoAgregado(2.0)  # Valor não existente
    
    def test_nome_invalido(self):
        """Testa que nome não existente levanta exceção"""
        with pytest.raises(KeyError):
            TipoAgregado['INEXISTENTE']